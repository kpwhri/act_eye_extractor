import re
from collections import defaultdict

from dateutil.parser import parse, ParserError
from loguru import logger

from eye_extractor.laterality import build_laterality_table, LATERALITY, \
    get_immediate_next_or_prev_laterality_from_table, Laterality, laterality_finder, simplify_lateralities
from eye_extractor.notes.operative import OperativeReport
from eye_extractor.sections.document import Document

iol_models = '|'.join([
    'sn60wf', 'ma60ac', r'sn6at\d', r'mta\W*400\W*ac',
    'mc50bm', 'au00t0', r'mn6ad3', 'mta4uo', 'cz70bd',
    'ma0ac', 'ma06ac', 'ma06c', 'ma60c', 'mc505bm',
    'mc50bm', 'mc60bm', 'mn60ac', 'mn60ma', r'mn6ad\d',
    'mta4uo', 'n60ac', 'sa60at', 'sa60wf', 'sn60at', r'sn60ad\d',
    'sn60t5', 'sn6wf', 'sv25t3', 'mta', 'zcb00'
])

iol_kind = '|'.join([
    r'pc\W*iol', r's\W*iol', r'ac\W*iol',
    'multifocal', 'sulcus', 'toric',
])

power = r'[+-]?\d{1,2}\.?[05]*'
diopter = r'd(iopter)?'

IOL_KIND_PAT = re.compile(
    rf'(?:'
    rf'\b{iol_kind}\b'
    rf')',
    re.I
)

IOL_TYPE_PAT = re.compile(
    rf'(?P<model>\b{iol_models})\W*'
    rf'(?:'
    rf'(?P<power>{power})\W*{diopter}'
    rf'|{diopter} with (?P<power2>{power})'
    rf')',
    re.I
)

LATERALITY_PAT = re.compile(
    rf'('
    rf'which (?:side|eye)\W*(?P<lat>left|right)'
    rf')',
    re.I
)

SURGERY_DATE_PAT = re.compile(
    r'(?:'
    r'surgery date: (?P<date>.{,20}\d{4})'
    r')',
    re.I
)

DATE_PAT = re.compile(
    r'(?:date: (?P<date>.{,20}\d{4}))',
    re.I
)

IS_CATSURG_PAT = re.compile(
    r'(?:preoperative\W*diagnosis:.{0,50}cataract|operative\W*report\W*ophthalmology cataract)',
    re.I
)


def get_cataract_laterality(text):
    for m in LATERALITY_PAT.finditer(text):
        yield {
            'laterality': LATERALITY[m.group('lat').upper()],
            'start': m.start(),
        }


def get_surgery_date(text):
    m = SURGERY_DATE_PAT.search(text)
    if not m:
        m = DATE_PAT.search(text)
        if not m:
            return None
    date_str = re.sub(r',', ' ', m.group('date'))
    try:
        return parse(date_str, fuzzy=True)
    except ParserError as e:
        logger.warning(f'Failed to parse date for surgery date: {date_str}')


def get_iol_type(text, get_kind=True):
    lat_table = build_laterality_table(text)
    for m in IOL_TYPE_PAT.finditer(text):
        data = {
            'model': m.group('model'),
            'power': float(m.group('power') or m.group('power2')),
            'laterality': get_immediate_next_or_prev_laterality_from_table(lat_table, m.start())[0]
        }
        prev = text[max(0, m.start() - 25): m.start()].lower()
        if 'primary iol' in prev:
            yield {**data, 'text': 'primary'}
        elif 'secondary iol' in prev:
            yield {**data, 'text': 'secondary'}
        else:
            yield {**data, 'text': prev}
    if not get_kind:
        return
    for m in re.finditer(r'\biol:', text, flags=re.I):
        target = text[m.end(): m.end() + 30]
        m2 = IOL_KIND_PAT.search(target)
        if not m2:
            continue
        context = text[max(0, m.start() - 10): m2.end() + 10].lower()
        yield {
            'type': m2.group(),
            'start': m2.start(),
            'end': m2.end(),
            'context': context,
        }


def cataractsurg_ioltype(text):
    """
    First iol is primary

    :return list of (model, power, laterality)
    """
    results = get_iol_type(text, get_kind=False)
    lat = list(get_cataract_laterality(text))
    lat = lat[0] if lat else None

    iols = defaultdict(list)
    for res in results:
        curr_lat = res.get('laterality', None)
        if not curr_lat and lat:
            curr_lat = lat.get('laterality', None)
        if res['text'] == 'primary':
            iols[curr_lat].insert(0, {
                'model': res['model'],
                'power': res['power'],
                'primary': True,
            })
        elif res['text'] == 'secondary':
            iols[curr_lat].append({
                'model': res['model'],
                'power': res['power'],
                'primary': False,
            })
        else:
            iols[curr_lat].append({
                'model': res['model'],
                'power': res['power'],
                'primary': False,
            })
    return iols


def get_cataractsurg_laterality(doc: OperativeReport):
    text = doc.get_preop() or doc.get_postop()
    if not text:
        return Laterality.UNKNOWN
    return simplify_lateralities(laterality_finder(text))


def get_cataractsurg_complications(doc: OperativeReport, text):
    complications = doc.get_complications()
    if not complications:
        if 'no complications' in text.lower():
            return {'text': 'no complications', 'value': 0}
        else:
            return {'text': '', 'value': -1}
    if 'none' in complications.lower():
        return {'text': complications[:20], 'value': 0}
    else:
        return {'text': complications[:20], 'value': 1, 'complication': complications[:30]}


def get_cataract_surgery(doc: Document):
    if not doc.is_cataract_surgery:
        return {}
    op_doc = OperativeReport.build_operative_report(doc.text)
    return {
        'cataractsurg_lat': get_cataractsurg_laterality(op_doc),
        'cataractsurg_ioltype': list(cataractsurg_ioltype(doc.text)),
        'cataractsurg_dt': get_surgery_date(op_doc.get_opdate()),
        'catsurg_comp': get_cataractsurg_complications(op_doc, doc.text)
    }
