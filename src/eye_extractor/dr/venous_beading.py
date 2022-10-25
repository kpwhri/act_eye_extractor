import re

from eye_extractor.common.negation import is_negated
from eye_extractor.common.severity import extract_severity, Severity
from eye_extractor.laterality import build_laterality_table, create_new_variable

VEN_BEADING_PAT = re.compile(
    r'\b('
    r'venous beading|vb'
    r')\b',
    re.I
)


def get_ven_beading(text: str, *, headers=None, lateralities=None) -> list:
    if not lateralities:
        lateralities = build_laterality_table(text)
    data = []
    for new_var in _get_ven_beading(text, lateralities, 'ALL'):
        data.append(new_var)
    if headers:
        pass

    return data


def _get_ven_beading(text: str, lateralities, source: str) -> dict:
    for m in VEN_BEADING_PAT.finditer(text):
        negated = is_negated(m, text, word_window=3)
        context = f'{text[max(0, m.start() - 100): m.start()]} {text[m.end():min(len(text), m.end() + 100)]}'
        severities = extract_severity(context)
        if severities:
            for sev in severities:
                yield create_new_variable(text, m, lateralities, 'venbeading', {
                    'value': sev,
                    'term': m.group(),
                    'label': 'Venous beading',
                    'negated': negated,
                    'regex': 'VEN_BEADING_PAT',
                    'source': source,
                })
        elif negated:
            yield create_new_variable(text, m, lateralities, 'venbeading', {
                'value': Severity.NONE,
                'term': m.group(),
                'label': 'No venous beading',
                'negated': negated,
                'regex': 'VEN_BEADING_PAT',
                'source': source,
            })
        else:  # Affirmative without severity quantifier.
            yield create_new_variable(text, m, lateralities, 'venbeading', {
                'value': Severity.MILD,
                'term': m.group(),
                'label': 'Venous beading',
                'negated': negated,
                'regex': 'VEN_BEADING_PAT',
                'source': source,
            })
