import re

from eye_extractor.common.negation import is_negated
from eye_extractor.laterality import build_laterality_table, create_new_variable

SRH_PAT = re.compile(
    r'('
    r'subretinal\W*(hem\w+|\bhg\b)'
    r'|\bsrh'
    r')',
    re.IGNORECASE
)

SRH_IN_MACULA_PAT = re.compile(
    r'('
    r'\bheme?s?\b'
    r'|hemorrhage'
    r')'
)


def get_subretinal_hemorrhage(text, *, headers=None, lateralities=None):
    if not lateralities:
        lateralities = build_laterality_table(text)

    data = []
    # everywhere
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
    # macula text only
    if headers:
        if macula_text := headers.get('MACULA', None):
            lateralities = build_laterality_table(macula_text)
            for m in SRH_IN_MACULA_PAT.finditer(text):
                # exclusion words (wrong heme)
                if is_negated(m, text, {'intraretinal', 'retinal'}):
                    continue
                negword = is_negated(m, text, {'no', 'or', 'without'})
                data.append(
                    create_new_variable(text, m, lateralities, 'subretinal_hem', {
                        'value': 0 if negword else 1,
                        'term': m.group(),
                        'label': 'no' if negword else 'yes',
                        'negated': negword,
                        'regex': 'SRH_IN_MACULA_PAT',
                        'source': 'MACULA',
                    })
                )
    return data
