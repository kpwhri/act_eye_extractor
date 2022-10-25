import re

from eye_extractor.common.negation import is_negated
from eye_extractor.laterality import build_laterality_table, create_new_variable

NEW_PAT = re.compile(
    r'(?:'
    r''
    r')',
    re.I
)

NEW_SECTION_PAT = re.compile(
    r'(?:'
    r''
    r')',
    re.I
)


def get_newvar(text, *, headers=None, lateralities=None):
    if not lateralities:
        lateralities = build_laterality_table(text)
    varname = 'newvar'
    data = []
    for m in NEW_PAT.finditer(text):
        negword = is_negated(m, text)
        data.append(
            create_new_variable(text, m, lateralities, varname, {
                'value': 0 if negword else 1,
                'term': m.group(),
                'label': 'no' if negword else 'yes',
                'negated': negword,
                'regex': 'NEW_PAT',
                'source': 'ALL',
            })
        )
    if headers:
        if section_text := headers.get('SECTION', None):
            lateralities = build_laterality_table(section_text)
            for m in NEW_SECTION_PAT.finditer(text):
                if is_negated(m, text, {'corneal'}):  # negation words to skip: not relevant
                    continue
                negword = is_negated(m, text)  # use pre-defined list
                data.append(
                    create_new_variable(text, m, lateralities, varname, {
                        'value': 0 if negword else 1,
                        'term': m.group(),
                        'label': 'no' if negword else 'yes',
                        'negated': negword,
                        'regex': 'NEW_SECTION_PAT',
                        'source': 'SECTION',
                    })
                )
    return data
