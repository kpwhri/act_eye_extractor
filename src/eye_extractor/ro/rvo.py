import enum
import re
from typing import Match

from eye_extractor.nlp.negate.negation import is_negated
from eye_extractor.laterality import create_new_variable
from eye_extractor.sections.document import Document


class RvoType(enum.IntEnum):
    UNKNOWN = -1
    NONE = 0
    RVO = 1
    BRVO = 2
    CRVO = 3


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


def get_rvo_kind(m: Match):
    """Determine if rvo is branch, central, or unspecified"""
    target = m.group().lower().strip()
    kind = RvoType.RVO
    if target.startswith('b'):
        kind = RvoType.BRVO
    elif target.startswith('c'):
        kind = RvoType.CRVO
    return kind


def extract_rvo(doc: Document):
    lateralities = doc.get_lateralities()
    text = doc.get_text()
    data = []
    for m in RVO_PAT.finditer(text):
        negword = is_negated(m, text)
        data.append(
            create_new_variable(text, m, lateralities, 'rvo_yesno', {
                'value': 0 if negword else 1,
                'term': m.group(),
                'label': 'no' if negword else 'yes',
                'negated': negword,
                'regex': 'RVO_PAT', 'source': 'ALL',
                'kind': get_rvo_kind(m),
            })
        )
    return data
