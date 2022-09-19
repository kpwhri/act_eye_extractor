import re

from ..common.negation import is_negated, NEGWORDS
from ..laterality import build_laterality_table, create_new_variable

# RAO, retinal artery occlusion, RvasO (retinal vascular occlusion - can be vein or artery),
# BRAO, Branch retinal artery occlusion, CRAO, Central retinal artery occlusion
RAO_PAT = re.compile(
    r'(?:'
    r'\b[cb]?rao\b'
    r'|\brvas[o0]\b'
    r'|(?:(?:branch|central)\W*)?retinal\W*(arter(y|ial)|vein(al)?)?\W*occlu\w+'
    r''
    r')',
    re.I
)


def get_rao(text, *, headers=None, lateralities=None):
    if not lateralities:
        lateralities = build_laterality_table(text)
    data = []
    for m in RAO_PAT.finditer(text):
        negword = is_negated(m, text, NEGWORDS)
        data.append(
            create_new_variable(text, m, lateralities, 'rao_yesno', {
                'value': 0 if negword else 1,
                'term': m.group(),
                'label': 'no' if negword else 'yes',
                'negated': negword,
                'regex': 'RAO_PAT', 'source': 'ALL',
            })
        )
    if headers:
        pass
    return data
