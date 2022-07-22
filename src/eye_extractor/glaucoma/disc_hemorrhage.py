import re

from eye_extractor.common.negation import is_negated
from eye_extractor.laterality import build_laterality_table, create_new_variable

DH_PAT = re.compile(
    fr'\b(?:'
    fr'dh|dis[ck]\W*hem\w*'
    fr')\b',
    re.I
)


def extract_disc_hem(text, *, headers=None, lateralities=None):
    """
    Extract disc hemorrhage into binary variable: 1=yes, 0=no, -1=unknown (default in builder)
    :param text:
    :param headers:
    :param lateralities:
    :return:
    """
    lateralities = lateralities or build_laterality_table(text)
    data = []

    for m in DH_PAT.finditer(text):
        negword = is_negated(m, text, {'no', 'or', 'without', 'not'})
        data.append(
            create_new_variable(text, m, lateralities, 'disc_hem', {
                'value': 0 if negword else 1,
                'term': m.group(),
                'label': 'no' if negword else 'yes',
                'negated': negword,
                'regex': 'DH_PAT',
                'source': 'ALL',
            })
        )
    return data
