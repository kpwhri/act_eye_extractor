import re

from eye_extractor.common.negation import is_negated
from eye_extractor.laterality import build_laterality_table, create_new_variable

tilt = r'(?:tilt\w*)'

TILTED_PAT = re.compile(
    fr'(?:'
    fr'(?:myop\w*|dis[ck]s?)\W*{tilt}\b'
    fr'|'
    fr'\b{tilt}\W*(?:dis[ck]s?|myop\w*)'
    fr')',
    re.I
)


def extract_tilted_disc(text, headers=None, lateralities=None):
    """

    :param text:
    :param headers:
    :param lateralities:
    :return:
    """
    lateralities = lateralities or build_laterality_table(text)
    data = []

    for m in NOTCH_PAT.finditer(text):
        negword = is_negated(m, text, {'no', 'or', 'without', 'not'})
        data.append(
            create_new_variable(text, m, lateralities, 'disc_notch', {
                'value': 0 if negword else 1,
                'term': m.group(),
                'label': 'no' if negword else 'yes',
                'negated': negword,
                'regex': 'NOTCH_PAT',
                'source': 'ALL',
            })
        )
    return data
