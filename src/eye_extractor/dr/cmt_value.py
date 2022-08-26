import re

from eye_extractor.common.negation import is_negated
from eye_extractor.laterality import build_laterality_table, create_new_variable

CMT_VALUE_PAT = re.compile(
    r'\b('
    r'CMT\W*(OD\W{0,2}\d+)?(\W*\w+){0,6}(OS\W{0,2}\d+)?'
    r'|CMT\W*(OS\W{0,2}\d+)?(\W*\w+){0,6}(OD\W{0,2}\d+)?'
    r'|CMT\W*\d+'
    r'|central macular thickness\W*\d+(um)?'
    r')\b',
    re.I
)

#(\W*\w+){0,3}