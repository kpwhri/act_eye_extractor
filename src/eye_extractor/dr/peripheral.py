import enum
import re

from eye_extractor.common.negation import is_negated
from eye_extractor.dr.hemorrhage_type import heme
from eye_extractor.laterality import build_laterality_table, create_new_variable

PERI_HEME_PAT = re.compile(
        rf'\b('
        rf'peripheral\s*{heme}'
        rf'|{heme}\s*peripheral'
        rf')\b'
)

PRP_SCARS_PAT = re.compile(
    rf'\b(?:'
    rf'prp(\W*laser)?\W+scars?'
    rf'|laser\s+panretinal photo\W?coagulation\W+scars?'
    rf'|scatter photo\W?coagulation\W+scars?'
    rf')\b',
    re.I
)
