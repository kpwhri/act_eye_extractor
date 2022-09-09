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
PERI_HEADER_HEME_PAT = re.compile(
    rf'\b('
    rf'{heme}'
    rf')\b',
    re.I
)
PERI_HEADER_LASER_SCARS_PAT = re.compile(
    r'\b('
    r'(laser\W*)?scars'
    r')\b',
    re.I
)
PRP_SCARS_PAT = re.compile(
    rf'\b(?:'
    rf'prp(\W*laser)?(\W*\w+){0,3}\W+scars?'
    rf'|(\W*laser)?\s+panretinal photo\W?coagulation\W+scars?'
    rf')\b',
    re.I
)


def get_peripheral(text: str, *, headers=None, lateralities=None) -> list:
    # data = []
    # if headers:
    #     if macula_text := headers.get('MACULA', None):
    #         lateralities = build_laterality_table(macula_text)
    #         for new_var in _get_lsr_macular_header(macula_text, lateralities):
    #             data.append(new_var)
    #         for new_var in _get_laser_scar_type(macula_text, lateralities, 'MACULA'):
    #             data.append(new_var)
    # else:
    #     if not lateralities:
    #         lateralities = build_laterality_table(text)
    #     for new_var in _get_laser_scar_type(text, lateralities, 'ALL'):
    #         data.append(new_var)
    # return data
    pass


# def _get_peripheral(text: str, lateralities, source: str) -> dict:
#     for pat_label, pat, variable in [
#         ('FOCAL_PAT', FOCAL_PAT, 'focal_dr_laser_scar_type'),
#         ('GRID_PAT', GRID_PAT, 'grid_dr_laser_scar_type'),
#         ('MACULAR_PAT', MACULAR_PAT, 'macular_dr_laser_scar_type'),
#     ]:
#         for m in pat.finditer(text):
#             negword = is_negated(m, text, {'no', 'or', 'neg', 'without'}, word_window=3)
#             yield create_new_variable(text, m, lateralities, variable, {
#                 'value': 0 if negword else 1,
#                 'term': m.group(),
#                 'label': 'no' if negword else 'yes',
#                 'negated': negword,
#                 'regex': pat_label,
#                 'source': source,
#             })
#
#
# def _get_peripheral_header(text: str, lateralities) -> dict:
#     for m in MACULAR_HEADER_PAT.finditer(text):
#         negword = is_negated(m, text, {'no', 'or', 'neg', 'without'}, word_window=3)
#         yield create_new_variable(text, m, lateralities, 'macular_dr_laser_scar_type', {
#             'value': 0 if negword else 1,
#             'term': m.group(),
#             'label': 'no' if negword else 'yes',
#             'negated': negword,
#             'regex': 'MACULAR_HEADER_PAT',
#             'source': 'MACULA',
#         })