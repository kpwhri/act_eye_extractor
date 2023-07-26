import re

from eye_extractor.nlp.negate.negation import is_negated, is_post_negated
from eye_extractor.laterality import build_laterality_table, create_new_variable

DME_YESNO_PAT = re.compile(
    r'\b('
    r'(cs|d)me'
    r'|diabetic\s+macular\s+edema'
    r'|diabetic\s+retinopathy\s+(?:\w*\s+)+macular\s+edema'
    r')\b',
    re.I
)
