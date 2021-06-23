"""Intraocular Pressure (IOP)"""
import re

IOP_PATTERN_RE = re.compile(
    r'\b(?:tonometry|tappl|tapp|ta|iops?|intraocular pressures?|t?nct|pressure):?\W*'
    r'(?:(?:Method|with|by):?\W+(?P<METHOD>\w+)\W*)?'
    r'(?:(?P<METHOD2>applanation|tappl|flouress|tnct)\W*)?'
    r'(?:(?:@|at)\s*\d+:\d+\s*(?:AM|PM)\W*)?'
    r'(?:(?:O\.?D\.?|R\.?E\.?)\W*(?P<OD>\d+(?:\.\d+)?|nt)\W*(mm?hg)?\W*)'
    r'(?:(?:and)\W*)?'
    r'(?:(?:O\.?S\.?|L\.?E\.?)\W*(?P<OS>\d+(?:\.\d+)?|nt)\W*(mm?hg)?)?',
    re.I
)

IOP_PATTERN_LE = re.compile(
    r'\b(?:tonometry|tappl|tapp|ta|iops?|intraocular pressures?|t?nct|pressure):?\W*'
    r'(?:(?:Method|with|by):?\W+(?P<METHOD>\w+)\W*)?'
    r'(?:(?P<METHOD2>applanation|tappl|flouress|tnct)\W*)?'
    r'(?:(?:@|at)\s*\d+:\d+\s*(?:AM|PM)\W*)?'
    r'(?:(?:O\.?D\.?|R\.?E\.?)\W*(?P<OD>\d+(?:\.\d+)?|nt)\W*(mm?hg)?\W*)?'
    r'(?:(?:and)\W*)?'
    r'(?:(?:O\.?S\.?|L\.?E\.?)\W*(?P<OS>\d+(?:\.\d+)?|nt)\W*(mm?hg)?)',
    re.I
)

IOP_PATTERN_RE_POST = re.compile(
    r'\b(?:tonometry|tappl|tapp|ta|iops?|intraocular pressures?|t?nct|pressure):?\W*'
    r'(?:(?:Method|with|by):?\W+(?P<METHOD>\w+)\W*)?'
    r'(?:(?P<METHOD2>applanation|tappl|flouress|tnct)\W*)?'
    r'(?:(?:@|at)\s*\d+:\d+\s*(?:AM|PM)\W*)?'
    r'(?:(?P<OD>\d+(?:\.\d+)?|nt)\W*(mm?hg)?\W*(?:O\.?D\.?|R\.?E\.?)\W*)'
    r'(?:(?:and)\W*)?'
    r'(?:(?P<OS>\d+(?:\.\d+)?|nt)\W*(mm?hg)?\W*(?:O\.?S\.?|L\.?E\.?))?',
    re.I
)

IOP_PATTERN_LE_POST = re.compile(
    r'\b(?:tonometry|tappl|tapp|ta|iops?|intraocular pressures?|t?nct|pressure):?\W*'
    r'(?:(?:Method|with|by):?\W+(?P<METHOD>\w+)\W*)?'
    r'(?:(?P<METHOD2>applanation|tappl|flouress|tnct)\W*)?'
    r'(?:(?:@|at)\s*\d+:\d+\s*(?:AM|PM)\W*)?'
    r'(?:(?P<OD>\d+(?:\.\d+)?|nt)\W*(mm?hg)?\W*(?:O\.?D\.?|R\.?E\.?)\W*)?'
    r'(?:(?:and)\W*)?'
    r'(?:(?P<OS>\d+(?:\.\d+)?|nt)\W*(mm?hg)?\W*(?:O\.?S\.?|L\.?E\.?))',
    re.I
)

IOP_PATTERN2 = re.compile(
    r'\b(?:ta|iops?):?\s*(?P<OD>\d+(?:\.\d+)?)'
    r'(?:\s*[,/]\s*(?P<OS>\d+(?:\.\d+)?))?',
    re.I
)


def convert_iop_value(value):
    try:
        return float(value)
    except ValueError:
        return 0  # nt


def get_iop(text):
    for iop_pattern in (IOP_PATTERN_LE, IOP_PATTERN_RE, IOP_PATTERN_LE_POST, IOP_PATTERN_RE_POST):
        for m in iop_pattern.finditer(text):
            curr = {}
            d = m.groupdict()
            if val := d.get('OD', None):
                curr['iop_measurement_re'] = {
                    'value': convert_iop_value(val)
                }
            if val := d.get('OS', None):
                curr['iop_measurement_le'] = {
                    'value': convert_iop_value(val)
                }
            if curr:
                yield curr

    for m in IOP_PATTERN2.finditer(text):
        curr = {}
        d = m.groupdict()
        if val := d.get('OS', None):
            curr['iop_measurement_le'] = {
                'value': convert_iop_value(val)
            }
            if val := d.get('OD', None):
                curr['iop_measurement_re'] = {
                    'value': convert_iop_value(val)
                }
        elif val := d.get('OD', None):
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
