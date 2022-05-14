import re

from eye_extractor.common.negation import is_negated
from eye_extractor.laterality import build_laterality_table, create_new_variable

CATARACT_PAT = re.compile(
    r'(?:'
    r'(need|require)s?\W*cataract\W*surgery'
    r'|(significant|cortical|nuclear)\W*cataract'
    r''
    r')',
    re.I
)


def get_cataract(text, *, headers=None, lateralities=None):
    if not lateralities:
        lateralities = build_laterality_table(text)
    data = []
    for m in CATARACT_PAT.finditer(text):
        negword = is_negated(m, text, {'no', 'or'})
        data.append(
            create_new_variable(text, m, lateralities, 'cataract_yesno', {
                'value': 0 if negword else 1,
                'term': m.group(),
                'label': 'no' if negword else 'yes',
                'negated': negword,
                'regex': 'CATARACT_PAT', 'source': 'ALL',
            })
        )
    if headers:
        pass
    return data
