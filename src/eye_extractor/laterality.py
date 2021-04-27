import enum
import re


class Laterality(enum.Enum):
    OD = 0  # right
    OS = 1  # left
    OU = 2  # both/bilateral
    UNKNOWN = 3


LATERALITY = {
    'OD': Laterality.OD,
    'O.D.': Laterality.OD,
    'RE': Laterality.OD,
    'R.E.': Laterality.OD,
    'RIGHT': Laterality.OD,
    'R': Laterality.OD,
    'L': Laterality.OS,
    'OS': Laterality.OS,
    'O.S.': Laterality.OS,
    'LE': Laterality.OS,
    'L.E.': Laterality.OS,
    'LEFT': Laterality.OS,
    'BOTH': Laterality.OU,
    'BE': Laterality.OU,
    'OU': Laterality.OU,
    'O.U.': Laterality.OU,
    'BILATERAL': Laterality.OU
}

LATERALITY_PATTERN = re.compile(
    r'\b(' + '|'.join(LATERALITY.keys()).replace('.', r'\.') + r')\b',
    re.IGNORECASE
)
