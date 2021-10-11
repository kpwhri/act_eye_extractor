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
    # 'BE': Laterality.OU,  # ambiguous
    'OU': Laterality.OU,
    'O.U.': Laterality.OU,
    'BILATERAL': Laterality.OU
}

LATERALITY_PATTERN = re.compile(
    r'\b(' + '|'.join(LATERALITY.keys()).replace('.', r'\.') + r')\b',
    re.IGNORECASE
)


def laterality_finder(text):
    for m in LATERALITY_PATTERN.finditer(text):
        yield LATERALITY[m.group().upper()]


def build_laterality_table(text):
    lats = []
    for m in LATERALITY_PATTERN.finditer(text):
        lats.append(
            (LATERALITY[m.group().upper()], m.start(), m.end())
        )
    return lats


def get_previous_laterality_from_table(table, index):
    for name, start, end in reversed(table):
        if end < index:
            return name, start, end
    return Laterality.UNKNOWN
