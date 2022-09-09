import enum
import re

from eye_extractor.common.negation import is_negated
from eye_extractor.dr.hemorrhage_type import heme
from eye_extractor.laterality import build_laterality_table, create_new_variable

PERI_HEME_PAT = re.compile(
        rf'\b('
        rf'peripheral\s*{heme}'
        rf'|{heme}\s*peripheral'
        rf')\b'
)
PERI_HEADER_HEME_PAT = re.compile(
    rf'\b('
    rf'{heme}'
    rf')\b',
    re.I
)
PERI_HEADER_LASER_SCARS_PAT = re.compile(
    r'\b('
    r'(laser\W*)?scars'
    r')\b',
    re.I
)
PRP_SCARS_PAT = re.compile(
    rf'\b(?:'
    rf'prp(\W*laser)?(\W+\w+)?\W+scars?'
    rf'|(\W*laser\s+)?panretinal photo\W?coagulation\W+scars?'
    rf')\b',
    re.I
)


def get_peripheral(text: str, *, headers=None, lateralities=None) -> list:
    data = []
    if headers:
        if peripheral_text := headers.get('PERIPHERAL', None):
            lateralities = build_laterality_table(peripheral_text)
            for new_var in _get_peripheral_header(peripheral_text, lateralities):
                data.append(new_var)
            for new_var in _get_peripheral(peripheral_text, lateralities, 'PERIPHERAL'):
                data.append(new_var)
    else:
        if not lateralities:
            lateralities = build_laterality_table(text)
        for new_var in _get_peripheral(text, lateralities, 'ALL'):
            data.append(new_var)
    return data


def _get_peripheral(text: str, lateralities, source: str) -> dict:
    for pat_label, pat, variable in [
        ('PERI_HEME_PAT', PERI_HEME_PAT, 'peripheral_heme'),
        ('PRP_SCARS_PAT', PRP_SCARS_PAT, 'prp_laser_scar'),
    ]:
        for m in pat.finditer(text):
            negwords = {'no', 'or', 'neg', 'without', 'w/out', '(-)'}
            negword = is_negated(m, text, negwords, word_window=3)
            yield create_new_variable(text, m, lateralities, variable, {
                'value': 0 if negword else 1,
                'term': m.group(),
                'label': 'no' if negword else 'yes',
                'negated': negword,
                'regex': pat_label,
                'source': source,
            })


def _get_peripheral_header(text: str, lateralities) -> dict:
    for pat_label, pat, variable in [
        ('PERI_HEADER_HEME_PAT', PERI_HEADER_HEME_PAT, 'peripheral_heme'),
        ('PERI_HEADER_LASER_SCARS_PAT', PERI_HEADER_LASER_SCARS_PAT, 'prp_laser_scar'),
    ]:
        for m in pat.finditer(text):
            negwords = {'no', 'or', 'neg', 'without', 'w/out', '(-)'}
            negword = is_negated(m, text, negwords, word_window=3)
            yield create_new_variable(text, m, lateralities, variable, {
                'value': 0 if negword else 1,
                'term': m.group(),
                'label': 'no' if negword else 'yes',
                'negated': negword,
                'regex': pat_label,
                'source': 'PERIPHERAL',
            })