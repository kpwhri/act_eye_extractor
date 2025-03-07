import re
from typing import Iterator

from eye_extractor.common.regex import expand_pattern
from eye_extractor.common.shared_patterns import retinal
from eye_extractor.nlp.negate.negation import is_negated, has_before
from eye_extractor.laterality import build_laterality_table, create_new_variable

laser = r'(?:tx|laser)'
scar = r'(?:scar(?:r?ing|s)?)'
laser_scars = rf'(?:(?:{laser}\W*)?{scar}|{laser})'
words_lte3 = r'(?:\w+\W+){0,3}'
panretinal = rf'(?:pan{retinal}|prp)'

FOCAL_PAT = re.compile(
    rf'\b('
    rf'focal\W*{words_lte3}{laser_scars}'
    rf'|{laser_scars}\W*{words_lte3}focal'
    rf')\b',
    re.I
)
MAC_FOCAL_PAT = expand_pattern(
    FOCAL_PAT,
    rf'|focal'
)
GRID_PAT = re.compile(
    rf'\b('
    rf'grid\W*{words_lte3}{laser_scars}'
    rf'|{laser_scars}\W*{words_lte3}grid'
    rf')\b',
    re.I
)
MAC_GRID_PAT = expand_pattern(
    GRID_PAT,
    rf'|grid'
)
MACULAR_PAT = re.compile(
    rf'\b('
    rf'(?:macular?|MACULA:)\W*{words_lte3}{laser_scars}'
    rf'|{laser_scars}\W*{words_lte3}macular?'
    rf')\b',
    re.I
)
MAC_MACULAR_PAT = re.compile(
    r'\b('
    rf'{laser_scars}'
    r')\b',
    re.I
)
PANRETINAL_PAT = re.compile(
    rf'\b('
    rf'{panretinal}\W*{words_lte3}{laser_scars}'
    rf'|{laser_scars}\W*{words_lte3}{panretinal}'
    rf')\b',
    re.I
)
MAC_PANRETINAL_PAT = expand_pattern(
    PANRETINAL_PAT,
    rf'|{panretinal}'
)


def get_laser_scar_type(text: str, *, headers=None, lateralities=None) -> list:
    data = []
    if headers:
        if macula_text := headers.get('MACULA', None):
            lateralities = build_laterality_table(macula_text)
            for new_var in _get_lsr_macular_header(macula_text, lateralities):
                data.append(new_var)
        if periphery_text := headers.get('PERIPHERY', None):
            lateralities = build_laterality_table(periphery_text)
            # TODO: should I look for just PRP here?
            for new_var in _get_lsr_macular_header(periphery_text, lateralities):
                data.append(new_var)


    if not lateralities:
        lateralities = build_laterality_table(text)
    for new_var in _get_laser_scar_type(text, lateralities, 'ALL'):
        data.append(new_var)
    return data


def _get_laser_scar_type(text: str, lateralities, source: str) -> Iterator[dict]:
    for pat_label, pat, variable in [
        ('FOCAL_PAT', FOCAL_PAT, 'focal_dr_laser_scar_type'),
        ('GRID_PAT', GRID_PAT, 'grid_dr_laser_scar_type'),
        ('MACULAR_PAT', MACULAR_PAT, 'macular_dr_laser_scar_type'),
        ('PANRETINAL_PAT', PANRETINAL_PAT, 'prp_dr_laser_scar_type'),
    ]:
        for m in pat.finditer(text):
            negword = (
                    is_negated(m, text, word_window=3)
                    and not has_before(m if isinstance(m, int) else m.start(), text, terms={'few'}, word_window=1)
            )
            yield create_new_variable(text, m, lateralities, variable, {
                'value': 0 if negword else 1,
                'term': m.group(),
                'label': 'no' if negword else 'yes',
                'negated': negword,
                'regex': pat_label,
                'source': source,
            })


def _get_lsr_macular_header(text: str, lateralities) -> Iterator[dict]:
    for pat_label, pat, variable in [
        ('MAC_FOCAL_PAT', MAC_FOCAL_PAT, 'focal_dr_laser_scar_type'),
        ('MAC_GRID_PAT', MAC_GRID_PAT, 'grid_dr_laser_scar_type'),
        ('MAC_MACULAR_PAT', MAC_MACULAR_PAT, 'macular_dr_laser_scar_type'),
        ('MAC_PANRETINAL_PAT', MAC_PANRETINAL_PAT, 'prp_dr_laser_scar_type'),
    ]:
        for m in pat.finditer(text):
            negword = is_negated(m, text, word_window=3)
            yield create_new_variable(text, m, lateralities, variable, {
                'value': 0 if negword else 1,
                'term': m.group(),
                'label': 'no' if negword else 'yes',
                'negated': negword,
                'regex': pat_label,
                'source': 'MACULA',
            })
