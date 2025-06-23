import re

from eye_extractor.nlp.negate.negation import is_negated
from eye_extractor.common.severity import extract_severity, Severity
from eye_extractor.laterality import build_laterality_table, create_new_variable
from eye_extractor.sections.document import Document
from eye_extractor.sections.patterns import SectionName

VEN_BEADING_PAT = re.compile(
    r'\b('
    r'venous beading|vb'
    r')\b',
    re.I
)


def get_ven_beading(doc: Document) -> list:
    data = []
    # Extract matches from sections / headers.
    for section in doc.iter_sections(SectionName.MACULA, SectionName.VESSELS):
        # Split into snippets on ';' (isolates lateralities).
        for section_snippet in section.text.split(';'):
            for new_var in _get_ven_beading(section_snippet, None, section.name):
                data.append(new_var)
    # Extract matches from full text. Split into snippets on ';' (isolates lateralities).
    for snippet in doc.get_text().split(';'):
        for new_var in _get_ven_beading(snippet, None, 'ALL'):
            data.append(new_var)

    return data


def _get_ven_beading(text: str, lateralities, source: str) -> dict:
    for m in VEN_BEADING_PAT.finditer(text):
        negated = (
                is_negated(m, text, word_window=3)
                or is_negated(m, text, terms={'no'}, word_window=7)
        )
        context = f'{text[max(0, m.start() - 100): m.start()]} {text[m.end():m.end() + 100]}'
        severities = extract_severity(context)

        # for the snippet view of `text.split(';')`, let's calculate only after a match
        lateralities = lateralities or build_laterality_table(text, search_negated_list=True)

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
                'value': Severity.NONE if negated else Severity.YES_NOS,
                'term': m.group(),
                'label': f'{"No v" if negated else "V"}enous beading',
                'negated': negated,
                'regex': 'VEN_BEADING_PAT',
                'source': source,
            })
