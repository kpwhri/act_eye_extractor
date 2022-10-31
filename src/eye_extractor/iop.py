"""Intraocular Pressure (IOP)"""
import re
from eye_extractor.va.common import right_eye, left_eye


tonometry = r'(?P<INSTRUMENT>tonometry|tappl|tapp|ta|iops?|intraocular pressures?|t?nct|pressure)'
method = r'(?:(?:Method|with|by)\W+(?P<METHOD1>[^:]*?)\W*)'
method2 = r'(?:(?P<METHOD2>applanation|tappl|flouress|t?nct|non contact method' \
          r'|goldman)\W*)'
nt = r'(n[at]|not assessed)'
at_time = r'(?:((performed|done)\W*)?(?:@|at)\s*\d+:\d+\s*(?:AM|PM)?\W*)'
fill_terms = r'(?:(?:if measured)\W*)'


IOP_PATTERN_FRACTION = re.compile(
    rf'\b({tonometry}\W*'
    rf'{method}?'
    rf'{method2}?'
    rf'(?<![/\d])'  # prevent matching on dates
    rf'(?P<OD>\d+(?:\.\d+)?|{nt})/+(?P<OS>\d+(?:\.\d+)?|{nt})\W*(mm?(hg)?)?'
    rf'(?![/\d])'  # prevent matching on dates
    rf')\b',
    re.I
)


IOP_PATTERN_RE = re.compile(
    rf'\b{tonometry}\W*'
    rf'{method}?'
    rf'{method2}?'
    rf'{at_time}?'
    rf'(?:{right_eye}\W*(?P<OD>\d+(?:\.\d+)?|{nt})\W*(mm?(hg)?)?\W*)'
    r'(?:(?:and)\W*)?'
    rf'(?:{left_eye}\W*(?P<OS>\d+(?:\.\d+)?|{nt})\W*(mm?(hg)?)?)?',
    re.I
)

IOP_PATTERN_LE = re.compile(
    rf'\b{tonometry}\W*'
    rf'{method}?'
    rf'{method2}?'
    rf'{at_time}?'
    rf'(?:{right_eye}\W*(?P<OD>\d+(?:\.\d+)?|{nt})\W*(mm?(hg)?)?\W*)?'
    r'(?:(?:and)\W*)?'
    rf'(?:{left_eye}\W*(?P<OS>\d+(?:\.\d+)?|{nt})\W*(mm?(hg)?)?)',
    re.I
)

IOP_PATTERN_RE_POST = re.compile(
    rf'\b{tonometry}\W*'
    rf'{method}?'
    rf'{method2}?'
    rf'{at_time}?'
    rf'{fill_terms}?'
    rf'(?:(?P<OD>\d+(?:\.\d+)?|{nt})\W*(mm?(hg)?)?\W*{right_eye}\W*)'
    r'(?:(?:and)\W*)?'
    rf'(?:(?P<OS>\d+(?:\.\d+)?|{nt})\W*(mm?(hg)?)?\W*{left_eye})?',
    re.I
)

IOP_PATTERN_LE_POST = re.compile(
    rf'\b{tonometry}\W*'
    rf'{method}?'
    rf'{method2}?'
    rf'{at_time}?'
    rf'{fill_terms}?'
    rf'(?:(?P<OD>\d+(?:\.\d+)?|{nt})\W*(mm?(hg)?)?\W*{right_eye}\W*)?'
    r'(?:(?:and)\W*)?'
    rf'(?:(?P<OS>\d+(?:\.\d+)?|{nt})\W*(mm?(hg)?)?\W*{left_eye})',
    re.I
)

IOP_PATTERN_OU = re.compile(
    rf'\b{tonometry}\W*'
    rf'{method}?'
    rf'{method2}?'
    rf'{at_time}?'
    rf'[\w\W]*'
    rf'(?:{right_eye}\W*(?P<OD>\d+(?:\.\d+)?|{nt})\W*(mm?(hg)?)?\W*)'
    r'(?:(?:and)\W*)?'
    rf'(?:{left_eye}\W*(?P<OS>\d+(?:\.\d+)?|{nt})\W*(mm?(hg)?)?)',
    re.I
)

IOP_PATTERN2 = re.compile(
    r'\b(?P<INSTRUMENT>ta|iops?):?\s*(?<![/\d])(?P<OD>\d+(?:\.\d+)?)'
    r'(?:\s*[,/]\s*(?P<OS>\d+(?:\.\d+)?)(?![/\d]))?',
    re.I
)


def convert_iop_value(value):
    try:
        return float(value)
    except ValueError:
        return 0  # nt


def clean_punc(text: str, pat: str = r'[¶»]') -> str:
    """Removes unnecessary punctuation from text."""
    return re.sub(pat, ' ', text)


def get_iop(text):
    text = clean_punc(text)
    for iop_pattern in (IOP_PATTERN_OU, IOP_PATTERN_LE, IOP_PATTERN_RE, IOP_PATTERN_LE_POST,
                        IOP_PATTERN_RE_POST, IOP_PATTERN_FRACTION):
        for m in iop_pattern.finditer(text):
            curr = {}
            d = m.groupdict()
            if val := d.get('OD', None):
                if convert_iop_value(val) < 100:
                    curr['iop_measurement_re'] = {
                        'value': convert_iop_value(val)
                    }
            if val := d.get('OS', None):
                if convert_iop_value(val) < 100:
                    curr['iop_measurement_le'] = {
                        'value': convert_iop_value(val)
                    }
            curr['instrument'] = d.get('INSTRUMENT', None)
            curr['method1'] = d.get('METHOD1', None)
            curr['method2'] = d.get('METHOD2', None)
            if curr:
                text = re.sub(m.string, ' ', text)
                yield curr

    for m in IOP_PATTERN2.finditer(text):
        curr = {}
        d = m.groupdict()
        curr['instrument'] = d.get('INSTRUMENT', None)
        if val := d.get('OS', None):
            if convert_iop_value(val) < 100:
                curr['iop_measurement_le'] = {
                    'value': convert_iop_value(val)
                }
            if val := d.get('OD', None):
                if convert_iop_value(val) < 100:
                    curr['iop_measurement_re'] = {
                        'value': convert_iop_value(val)
                    }
        elif val := d.get('OD', None):
            if convert_iop_value(val) < 100:
                curr['iop_measurement_re'] = {
                    'value': convert_iop_value(val)
                }
                curr['iop_measurement_le'] = {
                    'value': convert_iop_value(val)
                }
        if curr:
            yield curr


def iop_measurement_le(text):
    measure = [x.get('iop_measurement_le', {}).get('value', 0) for x in get_iop(text)]
    if not measure or max(measure) == 0:
        return '0'
    return str(max(measure))


def iop_measurement_re(text):
    measure = [x.get('iop_measurement_re', {}).get('value', 0) for x in get_iop(text)]
    # if 'refer to above notation' in text:
    #     print(text)
    if not measure or max(measure) == 0:
        return '0'
    return str(max(measure))
