import enum
import re


class Severity(enum.IntEnum):
    UNKNOWN = -1
    NONE = 0
    Q1 = 1
    Q2 = 2
    Q3 = 3
    Q4 = 4
    MILD = 5
    MODERATE = 6
    SEVERE = 7
    VERY_SEVERE = 8
    NOS = 9


SEVERITY_PAT = re.compile(
    r'\b('
    r'severity=(?P<q_value>\dq)'
    r')\b',
    re.I
)
Q1_PAT = re.compile(
    r'\b('
    r'\w+\s+quadrant'
    r')\b',
    re.I
)
Q2_PAT = re.compile(
    r'\b('
    r'\w+(\s+and|,)\s+\w+\s+quadrant(s)?'
    r')\b',
    re.I
)
Q3_PAT = re.compile(
    r'\b('
    r'\w+\s*,\s+\w+(\s+and|,)\s+\w+\s+quadrant(s)?'
    r')\b',
    re.I
)
Q4_PAT = re.compile(
    r'\b('
    r'all(\s+4)?\s+quadrant(s)?'
    r')\b',
    re.I
)
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
    r'(?<!very\s)severe'  # Negative lookbehind cannot contain a quantifier.
    r')\b',
    re.I
)
VERY_SEVERE_PAT = re.compile(
    r'\b('
    r'very\s+severe'
    r')\b',
    re.I
)

SEVERITY_PATS = [
    (VERY_SEVERE_PAT, Severity.VERY_SEVERE),
    (SEVERE_PAT, Severity.SEVERE),
    (MODERATE_PAT, Severity.MODERATE),
    (MILD_PAT, Severity.MILD),
    (Q4_PAT, Severity.Q4),
    (Q3_PAT, Severity.Q3),
    (Q2_PAT, Severity.Q2),
    (Q1_PAT, Severity.Q1),
]


def extract_severity(text: str) -> list[Severity]:
    sevs = []
    for m in SEVERITY_PAT.finditer(text):
        match m.group('q_value').lower():
            case '1q':
                sevs.append(Severity.Q1)
            case '2q':
                sevs.append(Severity.Q2)
            case '3q':
                sevs.append(Severity.Q3)
            case '4q':
                sevs.append(Severity.Q4)

    for pat, severity in SEVERITY_PATS:
        for _ in pat.finditer(text):
            sevs.append(severity)

    return sevs
