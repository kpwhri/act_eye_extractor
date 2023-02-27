import re

from eye_extractor.nlp.negate.negation import is_negated
from eye_extractor.common.severity import extract_severity, Severity
from eye_extractor.laterality import build_laterality_table, create_new_variable

VEN_BEADING_PAT = re.compile(
    r'\b('
    r'venous beading|vb'
    r')\b',
    re.I
)


def get_ven_beading(text: str, *, headers=None, lateralities=None) -> list:
    data = []
    # Extract matches from sections / headers.
    if headers:
        for section_header, section_text in headers.iterate('MACULA', 'VESSELS'):
            lateralities = build_laterality_table(section_text, search_negated_list=True)
            for new_var in _get_ven_beading(section_text, lateralities, section_header):
                data.append(new_var)
    # Extract matches from full text. Split into snippets on ';' (isolates lateralities).
    for snippet in text.split(';'):
        lateralities = build_laterality_table(snippet, search_negated_list=True)
        for new_var in _get_ven_beading(snippet, lateralities, 'ALL'):
            data.append(new_var)

    return data


def _get_ven_beading(text: str, lateralities, source: str) -> dict:
    for m in VEN_BEADING_PAT.finditer(text):
        negated = (
            is_negated(m, text, word_window=3)
            or is_negated(m, text, terms={'no'}, word_window=7)
        )
        context = f'{text[max(0, m.start() - 100): m.start()]} {text[m.end():min(len(text), m.end() + 100)]}'
        severities = extract_severity(context)
        if severities:  # With severity quantifier.
            for sev in severities:
                yield create_new_variable(text, m, lateralities, 'venbeading', {
                    'value': Severity.NONE if negated else sev,
                    'term': m.group(),
                    'label': 'Venous beading',
                    'negated': negated,
                    'regex': 'VEN_BEADING_PAT',
                    'source': source,
                })
        else:  # Without severity quantifier.
            yield create_new_variable(text, m, lateralities, 'venbeading', {
                'value': Severity.NONE if negated else Severity.MILD,
                'term': m.group(),
                'label': f'{"No v" if negated else "V"}enous beading',
                'negated': negated,
                'regex': 'VEN_BEADING_PAT',
                'source': source,
            })
