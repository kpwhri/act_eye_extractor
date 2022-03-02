import re

from eye_extractor.common.negation import is_negated
from eye_extractor.laterality import build_laterality_table, create_new_variable

SRH_PAT = re.compile(
    r'('
    r'subretinal\s*hem\w+'
    r'|\bsrh'
    r')',
    re.IGNORECASE
)


def get_subretinal_hemorrhage(text, *, headers=None, lateralities=None):
    if not lateralities:
        lateralities = build_laterality_table(text)

    data = []
    for m in SRH_PAT.finditer(text):
        negword = is_negated(m, text, {'no', 'or'})
        data.append(
            create_new_variable(text, m, lateralities, 'subretinal_hem', {
                'value': 0 if negword else 1,
                'term': m.group(),
                'label': 'no' if negword else 'yes',
                'negated': negword,
                'regex': 'SRH_PAT', 'source': 'ALL',
            })
        )
    return data
