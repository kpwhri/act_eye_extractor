import re

from eye_extractor.nlp.negate.negation import is_negated
from eye_extractor.common.severity import extract_severity, Severity
from eye_extractor.laterality import build_laterality_table, create_new_variable

IRMA_PAT = re.compile(
    r'\b('
    r'irma(?!\s+\w+\s+csn:)|intraretinal\s+microvascular\s+abnormality'
    r')\b',
    re.I
)


def get_irma(text: str, *, headers=None, lateralities=None) -> list:
    data = []
    # Extract matches from sections / headers.
    if headers:
        for section_header, section_text in headers.iterate('MACULA'):
            lateralities = build_laterality_table(section_text, search_negated_list=True)
            for new_var in _get_irma(section_text, lateralities, section_header):
                data.append(new_var)
    # Extract matches from full text. Split into snippets on ';' (isolates lateralities).
    for snippet in text.split(';'):
        lateralities = build_laterality_table(snippet, search_negated_list=True)
        for new_var in _get_irma(snippet, lateralities, 'ALL'):
            data.append(new_var)

    return data


def _get_irma(text: str, lateralities, source: str) -> dict:
    for m in IRMA_PAT.finditer(text):
        negated = (
            is_negated(m, text, word_window=4)
            or is_negated(m, text, terms={'no'}, word_window=6)
        )
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
