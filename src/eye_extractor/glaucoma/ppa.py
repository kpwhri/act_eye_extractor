"""
Peripapillary atropy

Peripapillary atrophy (PPA)
    RE    ppa_re    PPA    Binary    Y/N    Glaucoma
    LE    ppa_le    PPA    Binary    Y/N    Glaucoma
"""
import re

from eye_extractor.common.negation import is_negated
from eye_extractor.laterality import build_laterality_table, create_new_variable

PPA_PAT = re.compile(
    rf'\b(?:'
    rf'peri\W*papillary\W*atrophy'
    rf'|ppa'
    rf')\b'
)


def extract_ppa(text, *, headers=None, lateralities=None):
    """
    Extract disc hemorrhage into binary variable: 1=yes, 0=no, -1=unknown (default in builder)
    :param text:
    :param headers:
    :param lateralities:
    :return:
    """
    lateralities = lateralities or build_laterality_table(text)
    data = []

    for m in PPA_PAT.finditer(text):
        negword = is_negated(m, text, boundary_chars=';:')
        data.append(
            create_new_variable(text, m, lateralities, 'ppa', {
                'value': 0 if negword else 1,
                'term': m.group(),
                'label': 'no' if negword else 'yes',
                'negated': negword,
                'regex': 'PPA_PAT',
                'source': 'ALL',
            })
        )
    return data
