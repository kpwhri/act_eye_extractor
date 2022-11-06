import re

from eye_extractor.nlp.negate.negation import is_negated
from eye_extractor.laterality import build_laterality_table, create_new_variable

NOTCH_PAT = re.compile(
    fr'\b(?:notch\w*)\b',
    re.I
)


def extract_disc_notch(text, headers=None, lateralities=None):
    """

    :param text:
    :param headers:
    :param lateralities:
    :return:
    """
    lateralities = lateralities or build_laterality_table(text)
    data = []

    for m in NOTCH_PAT.finditer(text):
        negword = is_negated(m, text)
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
