import re

from eye_extractor.nlp.negate.negation import is_negated
from eye_extractor.laterality import build_laterality_table, create_new_variable, Laterality

# Old pattern, too greedy.
# CMT_VALUE_PAT = re.compile(
#     r'\b('
#     r'(?:OD\W*|OS\W*|CMT\s*|central macular thickness[ :]*)(?P<digit>\d{3,4})(?!/|\.|\W*mmhg)(um)?'
#     r')\b',
#     re.I
# )

CMT_VALUE_PAT = re.compile(
    r'\b('
    r'(CMT|central macular thickness:?)\s+'
    r'(OD:?\s*(?P<od_value>\d{3}))?\s?'
    r'(OS:?\s*(?P<os_value>\d{3}))?'
    r'(?P<unk_value>\d{3})?'
    r')\b',
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
    for match in CMT_VALUE_PAT.finditer(text):
        negated = is_negated(match, text, word_window=1)
        # CMT_VALUE_PAT will match to text without values, like 'CMT '.
        # Create new variable only if a value is captured.
        if match['od_value']:
            yield create_new_variable(text, match, lateralities, 'dmacedema_cmt',
                                      {
                                          'value': 0 if negated else int(match['od_value']),
                                          'term': match.group(),
                                          'label': f'No CMT value' if negated else 'CMT value',
                                          'negated': negated,
                                          'regex': 'CMT_VALUE_PAT',
                                          'source': source,
                                      },
                                      known_laterality=Laterality.OD)
        if match['os_value']:
            yield create_new_variable(text, match, lateralities, 'dmacedema_cmt',
                                      {
                                          'value': 0 if negated else int(match['os_value']),
                                          'term': match.group(),
                                          'label': f'No CMT value' if negated else 'CMT value',
                                          'negated': negated,
                                          'regex': 'CMT_VALUE_PAT',
                                          'source': source,
                                      },
                                      known_laterality=Laterality.OS)
        if match['unk_value']:
            yield create_new_variable(text, match, lateralities, 'dmacedema_cmt',
                                      {
                                          'value': 0 if negated else int(match['unk_value']),
                                          'term': match.group(),
                                          'label': f'No CMT value' if negated else 'CMT value',
                                          'negated': negated,
                                          'regex': 'CMT_VALUE_PAT',
                                          'source': source,
                                      },
                                      known_laterality=Laterality.UNKNOWN)
