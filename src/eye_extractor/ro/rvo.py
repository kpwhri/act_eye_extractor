import re

from eye_extractor.common.negation import is_negated
from eye_extractor.laterality import build_laterality_table, create_new_variable

# RVO, retinal vein occlusion, RvasO (retinal vascular occlusion - can be vein or artery),
# CRVO (central retinal vein occlusion), BRVO (branch retinal vein occlusion)
RVO_PAT = re.compile(
    r'(?:'
    r'\b[cb]?rvo\b'
    r'|\brvas[o0]\b'
    r'|(?:(?:branch|central)\W*)?retinal\W*(vein(al)?)?\W*occlu\w+'
    r''
    r')',
    re.I
)


def get_rvo(text, *, headers=None, lateralities=None):
    if not lateralities:
        lateralities = build_laterality_table(text)
    data = []
    for m in RVO_PAT.finditer(text):
        negword = is_negated(m, text, {'no', 'or'})
        data.append(
            create_new_variable(text, m, lateralities, 'rvo_yesno', {
                'value': 0 if negword else 1,
                'term': m.group(),
                'label': 'no' if negword else 'yes',
                'negated': negword,
                'regex': 'RVO_PAT', 'source': 'ALL',
            })
        )
    if headers:
        pass
    return data
