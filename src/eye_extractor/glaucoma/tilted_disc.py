import re

from eye_extractor.common.negation import is_negated, has_before, has_after, NEGWORDS
from eye_extractor.laterality import build_laterality_table, create_new_variable

tilt = r'(?:tilt\w*)'

TILTED_PLUS_PAT = re.compile(
    fr'(?:'
    fr'(?:myop\w*|dis[ck]s?)\W*{tilt}\b'
    fr'|'
    fr'\b{tilt}\W*(?:dis[ck]s?|myop\w*)'
    fr')',
    re.I
)

TILTED_PAT = re.compile(
    rf'\b(?:tilt(?:ed|ing)?)\b'
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

    for m in TILTED_PLUS_PAT.finditer(text):
        negword = is_negated(m, text, NEGWORDS)
        data.append(
            create_new_variable(text, m, lateralities, 'tilted_disc', {
                'value': 0 if negword else 1,
                'term': m.group(),
                'label': 'no' if negword else 'yes',
                'negated': negword,
                'regex': 'TILTED_PLUS_PAT',
                'source': 'ALL',
            })
        )
    if not data:
        pos_terms = {'saucer', 'saucered', 'disc', 'discs', 'od', 'os'}
        for m in TILTED_PAT.finditer(text):
            negword = is_negated(m, text, NEGWORDS)
            if (
                has_before(m.start(), text, {'head', 'glasses', 'to'}, word_window=5)
                or has_after(m.end(), text, {'head', 'glasses'}, word_window=5)
            ):
                continue
            elif (
                has_before(m.start(), text, pos_terms, word_window=5, skip_n_boundary_chars=1)
                or has_after(m.end(), text, pos_terms, word_window=5, skip_n_boundary_chars=1)
            ):
                data.append(
                    create_new_variable(text, m, lateralities, 'tilted_disc', {
                        'value': 0 if negword else 1,
                        'term': m.group(),
                        'label': 'no' if negword else 'yes',
                        'negated': negword,
                        'regex': 'TILTED_PAT',
                        'source': 'ALL',
                    })
                )
    return data
