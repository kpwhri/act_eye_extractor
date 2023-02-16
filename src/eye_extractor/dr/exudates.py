import re

from eye_extractor.nlp.negate.negation import is_negated, is_post_negated, has_after
from eye_extractor.laterality import build_laterality_table, create_new_variable

EXUDATES_PAT = re.compile(
    r'(?<!(hard|soft)\s)exud(ate)?s?',
    re.I
)
HARD_EXUDATES_PAT = re.compile(
    r'\b('
    r'hard\s+exud(ate)?s?'
    r')\b',
    re.I
)
# Separate pattern to capture uppercase abbreviations.
HARD_EXUDATES_ABBR_PAT = re.compile(
    r'\b('
    r'HE'
    r')\b',
)


def get_exudates(text: str, *, headers=None, lateralities=None) -> list:
    pass


# def get_laser_scar_type(text: str, *, headers=None, lateralities=None) -> list:
#     data = []
#     if headers:
#         if macula_text := headers.get('MACULA', None):
#             lateralities = build_laterality_table(macula_text)
#             for new_var in _get_lsr_macular_header(macula_text, lateralities):
#                 data.append(new_var)
#             for new_var in _get_laser_scar_type(macula_text, lateralities, 'MACULA'):
#                 data.append(new_var)
#
#     if not lateralities:
#         lateralities = build_laterality_table(text)
#     for new_var in _get_laser_scar_type(text, lateralities, 'ALL'):
#         data.append(new_var)
#     return data
#
#
# def _get_laser_scar_type(text: str, lateralities, source: str) -> dict:
#     for pat_label, pat, variable in [
#         ('FOCAL_PAT', FOCAL_PAT, 'focal_dr_laser_scar_type'),
#         ('GRID_PAT', GRID_PAT, 'grid_dr_laser_scar_type'),
#         ('MACULAR_PAT', MACULAR_PAT, 'macular_dr_laser_scar_type'),
#     ]:
#         for m in pat.finditer(text):
#             negword = (
#                 is_negated(m, text, word_window=3)
#                 and not has_before(m if isinstance(m, int) else m.start(), text, terms={'few'}, word_window=1)
#             )
#             yield create_new_variable(text, m, lateralities, variable, {
#                 'value': 0 if negword else 1,
#                 'term': m.group(),
#                 'label': 'no' if negword else 'yes',
#                 'negated': negword,
#                 'regex': pat_label,
#                 'source': source,
#             })


# def _get_cottonwspot(text: str, lateralities, source: str) -> dict:
#     for m in CWS_PAT.finditer(text):
#         negated = (
#             is_negated(m, text, word_window=3)
#             or is_negated(m, text, terms={'no'}, word_window=5)
#         )
#         yield create_new_variable(text, m, lateralities, 'cottonwspot', {
#             'value': 0 if negated else 1,
#             'term': m.group(),
#             'label': f'{"No c" if negated else "C"}otton wool spot.',
#             'negated': negated,
#             'regex': 'CWS_PAT',
#             'source': source,
#         })