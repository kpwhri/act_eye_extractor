"""Intraocular Pressure (IOP)"""
import re

IOP_PATTERN = re.compile(
    r'(?:tonometry|tappl|ta):?\W*'
    r'(?:(?:O\.?D\.?|R\.?E\.?)\W*(?P<OD>\d+(?:\.\d+)?)\W*mmhg\W*)?'
    r'(?:(?:O\.?S\.?|L\.?E\.?)\W*(?P<OS>\d+(?:\.\d+)?)\W*mmhg\W*)?',
    re.I
)


def get_iop(text):
    for m in IOP_PATTERN.finditer(text):
        curr = {}
        d = m.groupdict()
        if val := d.get('OD', None):
            curr['iop_measurement_re'] = {
                'value': float(val)
            }
        if val := d.get('OS', None):
            curr['iop_measurement_le'] = {
                'value': float(val)
            }
        if curr:
            yield curr
