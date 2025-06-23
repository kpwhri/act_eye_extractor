import re

from eye_extractor.nlp.negate.negation import is_negated, is_post_negated, has_after
from eye_extractor.laterality import build_laterality_table, create_new_variable
from eye_extractor.sections.document import Document
from eye_extractor.sections.patterns import SectionName

CWS_PAT = re.compile(
    r'\b('
    r'cotton\W?wool\W?spots?|cws?|soft\s+exudates?'
    r')\b',
    re.I
)


def get_cottonwspot(doc: Document) -> list:
    data = []
    # Extract matches from sections / headers.
    for section in doc.iter_sections(SectionName.MACULA):
        for snippet in section.text.split(';'):  # TODO: this might make sense for separating lateralities
            for new_var in _get_cottonwspot(snippet, None, section.name):
                data.append(new_var)
    # Extract matches from full text. Split into snippets on ';' (isolates lateralities).
    for snippet in doc.text.split(';'):  # TODO: this doesn't make sense for separating lateralities across entire note
        for new_var in _get_cottonwspot(snippet, None, 'ALL'):
            data.append(new_var)

    return data


def _get_cottonwspot(text: str, lateralities, source: str) -> dict:
    for m in CWS_PAT.finditer(text):
        negated = (
            is_negated(m, text, word_window=3)
            or is_negated(m, text, terms={'no'}, word_window=5)
        )
        # for the snippet view of `text.split(';')`, let's calculate only after a match
        lateralities = lateralities or build_laterality_table(text, search_negated_list=True)

        yield create_new_variable(text, m, lateralities, 'cottonwspot', {
            'value': 0 if negated else 1,
            'term': m.group(),
            'label': f'{"No c" if negated else "C"}otton wool spot.',
            'negated': negated,
            'regex': 'CWS_PAT',
            'source': source,
        })
