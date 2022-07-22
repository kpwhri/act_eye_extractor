import re

from eye_extractor.common.negation import is_negated
from eye_extractor.laterality import build_laterality_table, create_new_variable

NOTCH_PAT = re.compile(
    fr'\b(?:notch\w*)\b',
    re.I
)


def extract_disc_notch(text, headers=None, lateralities=None):
    pass
