import enum
import re

from eye_extractor.common.negation import is_negated
from eye_extractor.laterality import build_laterality_table, create_new_variable


class HemorrhageType(enum.IntEnum):
    UNKNOWN = -1
    NONE = 0
    INTRARETINAL = 1
    DOT_BLOT = 2
    PRERETINAL = 3
    VITREOUS = 4
    SUBRETINAL = 5


INTRARETINAL_PAT = re.compile(
        r'\b('
        r'intraretinal\s*hemorrhage'
        r'|hemorrhage\s*intraretinal'
        r')\b'
)
DOT_BLOT_PAT = re.compile(
        r'\b('
        r'dot blot\s*hemorrhage'
        r'|hemorrhage\s*dot blot'
        r')\b'
)
PRERETINAL_PAT = re.compile(
        r'\b('
        r'preretinal\s*hemorrhage'
        r'|hemorrhage\s*preretinal'
        r')\b'
)
VITREOUS_PAT = re.compile(
        r'\b('
        r'vitreous\s*hemorrhage'
        r'|hemorrhage\s*vitreous'
        r')\b'
)
SUBRETINAL_PAT = re.compile(
        r'\b('
        r'subretinal\s*hemorrhage'
        r'|hemorrhage\s*subretinal'
        r')\b'
)


def get_hemorrhage_type(text, *, headers=None, lateralities=None):
    if not lateralities:
        lateralities = build_laterality_table(text)
    data = []
    for pat, hemtype, hemlabel in [
        (INTRARETINAL_PAT, HemorrhageType.INTRARETINAL, 'intraretinal'),
        (DOT_BLOT_PAT, HemorrhageType.DOT_BLOT, 'dot blot'),
        (PRERETINAL_PAT, HemorrhageType.PRERETINAL, 'preretinal'),
        (VITREOUS_PAT, HemorrhageType.VITREOUS, 'vitreous'),
        (SUBRETINAL_PAT, HemorrhageType.SUBRETINAL, 'subretinal'),
    ]:
        for m in pat.finditer(text):
            negword = is_negated(m, text, {'no', 'or', 'neg', 'without'}, word_window=3)
            data.append(
                create_new_variable(text, m, lateralities, 'hemorrhage_typ_dr', {
                    'value': HemorrhageType.NONE if negword else hemtype,
                    'term': m.group(),
                    'label': f'No {hemlabel} hemorrhage' if negword else f'{hemlabel} hemorrhage',
                    'negated': negword,
                    'regex': f'{hemlabel}_PAT',
                    'source': 'ALL',
                })
            )
    if headers:
        pass
    return data
