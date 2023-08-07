import re

from eye_extractor.common.get_variable import get_variable
from eye_extractor.nlp.negate.negation import has_before, is_negated
from eye_extractor.laterality import create_new_variable

RET_MICRO_PAT = re.compile(
    r'\b('
    r'mas?'
    r'|retinal mas?'
    r'|retinal micro\W?aneurysms?'
    r')\b',
    re.I
)
