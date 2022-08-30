import enum
import re

from eye_extractor.common.negation import is_negated
from eye_extractor.laterality import build_laterality_table, create_new_variable


class Severity(enum.IntEnum):
    UNKNOWN = -1
    Q1 = 1
    Q2 = 2
    Q3 = 3
    Q4 = 4
    MILD = 5
    MODERATE = 6
    SEVERE = 7


MILD_PAT = re.compile(
    r'\b('
    r'mild'
    r')\b',
    re.I
)

MODERATE_PAT = re.compile(
    r'\b('
    r'moderate'
    r')\b',
    re.I
)

SEVERE_PAT = re.compile(
    r'\b('
    r'severe'
    r')\b',
    re.I
)

SEVERITY_PAT = re.compile(
    r'\b('
    r'severity=(?P<q_value>\dQ)'
    r')\b',
    re.I
)

ONE_QUADRANT = re.compile(
    r'\b('
    r'\w+\s+quadrant'
    r')\b',
    re.I
)

TWO_QUADRANT = re.compile(
    r'\b('
    r'\w+(\s+and|,)\s+\w+\s+quadrant(s)?'
    r')\b',
    re.I
)

THREE_QUADRANT = re.compile(
    r'\b('
    r'\w+\s*,\s+\w+(\s+and|,)\s+\w+\s+quadrant(s)?'
    r')\b',
    re.I
)

FOUR_QUADRANT = re.compile(
    r'\b('
    r'all\s+quadrant(s)?'
    r')\b',
    re.I
)

