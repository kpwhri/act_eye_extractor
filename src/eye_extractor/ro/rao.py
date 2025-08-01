import re

from eye_extractor.nlp.negate.negation import is_negated
from ..laterality import create_new_variable
from ..sections.document import Document

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


def get_rao(doc: Document):
    lateralities = doc.get_lateralities()
    text = doc.get_text()
    data = []
    for m in RAO_PAT.finditer(text):
        negword = is_negated(m, text)
        data.append(
            create_new_variable(text, m, lateralities, 'rao_yesno', {
                'value': 0 if negword else 1,
                'term': m.group(),
                'label': 'no' if negword else 'yes',
                'negated': negword,
                'regex': 'RAO_PAT', 'source': 'ALL',
            })
        )
    return data
