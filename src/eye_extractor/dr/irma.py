import re

from eye_extractor.common.negation import is_negated
from eye_extractor.common.severity import extract_severity, Severity
from eye_extractor.laterality import build_laterality_table, create_new_variable

IRMA_PAT = re.compile(
    r'\b('
    r'irma|intraretinal\s+microvascular\s+abnormality'
    r')\b',
    re.I
)


def get_irma(text: str, *, headers=None, lateralities=None) -> list:
    if not lateralities:
        lateralities = build_laterality_table(text)
    data = []
    for new_var in _get_irma(text, lateralities, 'ALL'):
        data.append(new_var)
    if headers:
        pass

    return data


def _get_irma(text: str, lateralities, source: str) -> dict:
    for m in IRMA_PAT.finditer(text):
        negated = is_negated(m, text, word_window=3)
        context = f'{text[max(0, m.start() - 100): m.start()]} {text[m.end():min(len(text), m.end() + 100)]}'
        severities = extract_severity(context)
        if severities:
            for sev in severities:
                yield create_new_variable(text, m, lateralities, 'irma', {
                    'value': sev,
                    'term': m.group(),
                    'label': 'IRMA',
                    'negated': negated,
                    'regex': 'IRMA_PAT',
                    'source': source,
                })
        elif negated:
            yield create_new_variable(text, m, lateralities, 'irma', {
                'value': Severity.NONE,
                'term': m.group(),
                'label': 'No IRMA',
                'negated': negated,
                'regex': 'IRMA_PAT',
                'source': source,
            })
        else:  # Affirmative without severity quantifier.
            yield create_new_variable(text, m, lateralities, 'irma', {
                'value': Severity.MILD,
                'term': m.group(),
                'label': 'IRMA',
                'negated': negated,
                'regex': 'IRMA_PAT',
                'source': source,
            })
