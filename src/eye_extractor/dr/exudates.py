import re

from eye_extractor.nlp.negate.negation import is_negated, is_post_negated, has_after
from eye_extractor.laterality import build_laterality_table, create_new_variable

EXUDATES_PAT = re.compile(
    r'(?<!(hard|soft)\s)exud(ate)?s?',
    re.I
)
HARD_EXUDATES_PAT = re.compile(
    r'\b('
    r'hard\s+exud(ate)?s?'
    r')\b',
    re.I
)
# Separate pattern to capture uppercase abbreviations.
HARD_EXUDATES_ABBR_PAT = re.compile(
    r'\b('
    r'HE'
    r')\b',
)


def get_exudates(text: str, *, headers=None, lateralities=None) -> list:
    data = []
    # Extract matches from sections / headers.
    if headers:
        pass
    # Extract matches from full text.
    if not lateralities:
        lateralities = build_laterality_table(text, search_negated_list=True)
    for new_var in _get_exudates(text, lateralities, 'ALL'):
        data.append(new_var)
    return data


def _get_exudates(text: str, lateralities, source: str) -> dict:
    for pat_label, pat, variable in [
        ('EXUDATES_PAT', EXUDATES_PAT, 'exudates'),
        ('HARD_EXUDATES_PAT', HARD_EXUDATES_PAT, 'hardexudates'),
        ('HARD_EXUDATES_ABBR_PAT', HARD_EXUDATES_ABBR_PAT, 'hardexudates'),
    ]:
        for m in pat.finditer(text):
            negated = (
                is_negated(m, text, word_window=3)
                or is_negated(m, text, terms={'no'}, word_window=5)
            )
            yield create_new_variable(text, m, lateralities, variable, {
                'value': 0 if negated else 1,
                'term': m.group(),
                'label': 'No' if negated else 'Yes',
                'negated': negated,
                'regex': pat_label,
                'source': source,
            })
