import re

from eye_extractor.nlp.negate.negation import is_negated, is_post_negated, has_after
from eye_extractor.laterality import build_laterality_table, create_new_variable

CWS_PAT = re.compile(
    r'\b('
    r'cotton\W?wool\W?spots?|cws?|soft\s+exudates?'
    r')\b',
    re.I
)


def get_cottonwspot(text: str, *, headers=None, lateralities=None) -> list:
    data = []
    # Extract matches from sections / headers.
    if headers:
        for section_header, section_text in headers.iterate('MACULA'):
            for snippet in section_text.split(';'):
                lateralities = build_laterality_table(snippet)
                for new_var in _get_cottonwspot(snippet, lateralities, section_header):
                    data.append(new_var)
    # Extract matches from full text. Split into snippets on ';' (isolates lateralities).
    for snippet in text.split(';'):
        lateralities = build_laterality_table(snippet)
        for new_var in _get_cottonwspot(snippet, lateralities, 'ALL'):
            data.append(new_var)

    return data


def _get_cottonwspot(text: str, lateralities, source: str) -> dict:
    for m in CWS_PAT.finditer(text):
        negated = (
            is_negated(m, text, word_window=3)
            or is_negated(m, text, terms={'no'}, word_window=5)
        )
        yield create_new_variable(text, m, lateralities, 'cottonwspot', {
            'value': 0 if negated else 1,
            'term': m.group(),
            'label': f'{"No c" if negated else "C"}otton wool spot.',
            'negated': negated,
            'regex': 'CWS_PAT',
            'source': source,
        })
