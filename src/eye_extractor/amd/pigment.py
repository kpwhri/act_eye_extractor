import re

from eye_extractor.common.negation import is_negated
from eye_extractor.laterality import build_laterality_table, create_new_variable

change = r'(?:chang|disrupt|dispers|atrophy|abnormal|atrophy|clump|mottl|pigment)\w*'
pigment = r'(?:(?:hyper)?pigment\w*|\brpe\b)'

PIGMENTARY_PAT = re.compile(
    rf'(?:'
    rf'{pigment}\s*{change}'
    rf'|{change}\s*(\w+\s+){{0,3}}{pigment}'
    rf')',
    re.IGNORECASE
)


def get_pigmentary_changes(text, *, headers=None, lateralities=None):
    data = []
    if headers:
        if macula_text := headers.get('MACULA', None):
            lateralities = build_laterality_table(macula_text)
            data += _get_pigmentary_changes(macula_text, lateralities, source='MACULA')
    else:
        if not lateralities:
            lateralities = build_laterality_table(text)
        data += _get_pigmentary_changes(text, lateralities, source='ALL')
    return data


def _get_pigmentary_changes(text, lateralities, source):
    data = []
    for m in PIGMENTARY_PAT.finditer(text):
        negword = is_negated(m, text, {'no', 'or'}, word_window=3)
        data.append(
            create_new_variable(text, m, lateralities, 'pigmentchanges', {
                'value': 0 if negword else 1,
                'term': m.group(),
                'label': 'no' if negword else 'yes',
                'negated': negword,
                'regex': 'PIGMENTARY_PAT',
                'source': 'ALL',
            })
        )
    return data
