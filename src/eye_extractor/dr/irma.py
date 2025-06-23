import re

from eye_extractor.common.shared_patterns import retinal, abnormality, microvascular
from eye_extractor.nlp.negate.negation import is_negated, is_post_negated
from eye_extractor.common.severity import extract_severity, Severity
from eye_extractor.laterality import build_laterality_table, create_new_variable, OtherLateralityName
from eye_extractor.sections.document import Document
from eye_extractor.sections.patterns import SectionName

IRMA_PAT = re.compile(
    rf'\b('
    rf'irma'
    rf'|intra{retinal}\s+{microvascular}\s+{abnormality}'
    rf')\b',
    re.I
)


def get_irma(doc: Document) -> list:
    data = []
    # Extract matches from sections / headers.
    for section in doc.iter_sections(SectionName.MACULA):
        for new_var in _get_irma(
                section.text,
                section.get_other_lateralities(OtherLateralityName.SEARCH_NEGATED_LIST),
                section.name,
        ):
            data.append(new_var)
    # Extract matches from full text. Split into snippets on ';' (isolates lateralities).
    for snippet in doc.text.split(';'):  # TODO: this doesn't make sense: split across sections?!
        for new_var in _get_irma(snippet, None, 'ALL'):
            data.append(new_var)

    return data


def _get_irma(text: str, lateralities, source: str) -> dict:
    for m in IRMA_PAT.finditer(text):
        if is_post_negated(m, text, terms={'csn'}):
            continue  # consumer number for name
        negated = (
                is_negated(m, text, word_window=4)
                or is_negated(m, text, terms={'no'}, word_window=6)
        )
        context = f'{text[max(0, m.start() - 100): m.start()]} {text[m.end():min(len(text), m.end() + 100)]}'
        severities = extract_severity(context)
        # for the snippet view of `text.split(';')`, let's calculate only after a match
        lateralities = lateralities or build_laterality_table(text, search_negated_list=True)

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
                'value': Severity.YES_NOS,
                'term': m.group(),
                'label': 'IRMA',
                'negated': negated,
                'regex': 'IRMA_PAT',
                'source': source,
            })
