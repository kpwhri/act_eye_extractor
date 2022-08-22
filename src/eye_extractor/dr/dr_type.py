import enum
import re


class DrType(enum.IntEnum):
    UNKNOWN = -1
    NONE = 0
    NPDR = 1
    PDR = 2


NPDR_PAT = re.compile(
    r'\b('
    r'npdr|non(-|\s*)?proliferative diabetic retinopathy'
    r')\b',
    re.I
)
PDR_PAT = re.compile(
    r'\b('
    r'pdr|proliferative diabetic retinopathy'
    r')\b',
    re.I
)


def get_dr_type(text: str, *, headers=None, lateralities=None) -> list:
    data = []
    return data
