import re

from eye_extractor.common.negation import is_negated, NEGWORDS
from eye_extractor.laterality import build_laterality_table, create_new_variable


CMT_VALUE_PAT = re.compile(
    r'\b(?:OD\W*|OS\W*|CMT\s*|central macular thickness\W*)(?P<digit>\d+)(um)?\b',
    re.I
)


def get_cmt_value(text: str, *, headers=None, lateralities=None) -> list:
    if not lateralities:
        lateralities = build_laterality_table(text)
    data = []
    for new_var in _get_cmt_value(text, lateralities, 'ALL'):
        data.append(new_var)
    if headers:
        pass

    return data


def _get_cmt_value(text: str, lateralities, source: str) -> dict:
    for m in CMT_VALUE_PAT.finditer(text):
        negated = is_negated(m, text, NEGWORDS, word_window=1)
        yield create_new_variable(text, m, lateralities, 'dmacedema_cmt', {
            'value': 0 if negated else int(m.group('digit')),
            'term': m.group(),
            'label': f'No CMT value' if negated else 'CMT value',
            'negated': negated,
            'regex': 'CMT_VALUE_PAT',
            'source': source,
        })
