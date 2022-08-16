import enum
import re

from eye_extractor.common.negation import is_negated
from eye_extractor.laterality import build_laterality_table, create_new_variable


class LaserScarType(enum.IntEnum):
    UNKNOWN = -1
    NONE = 0
    MACULAR = 1
    PANRETINAL = 2
    FOCAL = 3
    GRID = 4


MACULAR_PAT = re.compile(
        r'\b('
        r'((macula(r)?)|MACULA:)(\W*\w+){0,3}\W*(laser\W*)?scars'
        r'|(laser\W*)?scars(\W*\w+){0,3}\W*macula(r)?'
        r')\b'
)
PANRETINAL_PAT = re.compile(
        r'\b('
        r'PRP(\W*\w+){0,3}\W*(scars|marks)'
        r'|(scars|marks)(\W*\w+){0,3}\W*PRP'
        r')\b'
)
FOCAL_PAT = re.compile(
        r'\b('
        r'focal(\W*\w+){0,3}\W*(laser\W*)?scars'
        r'|(laser\W*)?scars(\W*\w+){0,3}\W*focal'
        r')\b'
)
GRID_PAT = re.compile(
        r'\b('
        r'grid(\W*\w+){0,3}\W*(laser\W*)?scars'
        r'|(laser\W*)?scars(\W*\w+){0,3}\W*grid'
        r')\b'
)


# def get_hemorrhage_type(text, *, headers=None, lateralities=None):
#     if not lateralities:
#         lateralities = build_laterality_table(text)
#     data = []
#     for pat_label, pat, value in [
#         (INTRARETINAL_PAT, HemorrhageType.INTRARETINAL, 'intraretinal'),
#         (DOT_BLOT_PAT, HemorrhageType.DOT_BLOT, 'dot blot'),
#         (PRERETINAL_PAT, HemorrhageType.PRERETINAL, 'preretinal'),
#         (VITREOUS_PAT, HemorrhageType.VITREOUS, 'vitreous'),
#         (SUBRETINAL_PAT, HemorrhageType.SUBRETINAL, 'subretinal'),
#     ]:
#         for m in pat.finditer(text):
#             negword = is_negated(m, text, {'no', 'or', 'neg', 'without'}, word_window=3)
#             data.append(
#                 create_new_variable(text, m, lateralities, 'hemorrhage_typ_dr', {
#                     'value': HemorrhageType.NONE if negword else hemtype,
#                     'term': m.group(),
#                     'label': f'No {hemlabel} hemorrhage' if negword else f'{hemlabel} hemorrhage',
#                     'negated': negword,
#                     'regex': f'{hemlabel}_PAT',
#                     'source': 'ALL',
#                 })
#             )
#     if headers:
#         pass
#     return data