import re

from dateutil.parser import parse

from eye_extractor.laterality import build_laterality_table, get_previous_laterality_from_table, LATERALITY

iol_models = '|'.join([
    'sn60wf', 'ma60ac', 'sn6at5', r'mta\W*400\W*ac'
])

power = r'[+-]?\d{1,2}\.?[05]*'
diopter = r'd(iopter)?'

IOL_TYPE_PAT = re.compile(
    rf'(?P<model>{iol_models})\W*'
    rf'(?:'
    rf'(?P<power>{power})\W*{diopter}'
    rf'|{diopter} with (?P<power2>{power})'
    rf')',
    re.I
)

LATERALITY_PAT = re.compile(
    rf'('
    rf'which side\W*(?P<lat>left|right)'
    rf')',
    re.I
)


SURGERY_DATE_PAT = re.compile(
    r'(?:'
    r'surgery date: (?P<date>.*?\d{4})'
    r')',
    re.I
)

DATE_PAT = re.compile(
    r'(?:date: (?P<date>.*?\d{4}))',
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
    date_str = re.sub(r'\W', ' ', m.group('date'))
    return parse(date_str, fuzzy=True)


def get_iol_type(text):
    lat_table = build_laterality_table(text)
    for m in IOL_TYPE_PAT.finditer(text):
        data = {
            'model': m.group('model'),
            'power': float(m.group('power') or m.group('power2')),
            'laterality': get_previous_laterality_from_table(lat_table, m.start())
        }
        prev = text[max(0, m.start() - 25): m.start()].lower()
        if 'primary iol' in prev:
            yield {**data, 'text': 'primary iol'}
        elif 'secondary iol' in prev:
            yield {**data, 'text': 'secondary iol'}
        else:
            yield {**data, 'text': prev}
