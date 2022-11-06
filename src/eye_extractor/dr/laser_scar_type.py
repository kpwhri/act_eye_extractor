import re

from eye_extractor.nlp.negate.negation import is_negated
from eye_extractor.laterality import build_laterality_table, create_new_variable

FOCAL_PAT = re.compile(
    r'\b('
    r'focal(\W*\w+){0,3}\W*(laser\W*)?scars'
    r'|(laser\W*)?scars(\W*\w+){0,3}\W*focal'
    r')\b',
    re.I
)
GRID_PAT = re.compile(
    r'\b('
    r'grid(\W*\w+){0,3}\W*(laser\W*)?scars'
    r'|(laser\W*)?scars(\W*\w+){0,3}\W*grid'
    r')\b',
    re.I
)
MACULAR_PAT = re.compile(
    r'\b('
    r'((macula(r)?)|MACULA:)(\W*\w+){0,3}\W*(laser\W*)?(scars)?'
    r'|(laser\W*)?scars(\W*\w+){0,3}\W*macula(r)?'
    r')\b',
    re.I
)
MACULAR_HEADER_PAT = re.compile(
    r'\b('
    r'(\W*\w+){0,3}\W*(laser\W*)?scars'
    r'|(laser\W*)?scars(\W*\w+){0,3}'
    r')\b',
    re.I
)


def get_laser_scar_type(text: str, *, headers=None, lateralities=None) -> list:
    data = []
    if headers:
        if macula_text := headers.get('MACULA', None):
            lateralities = build_laterality_table(macula_text)
            for new_var in _get_lsr_macular_header(macula_text, lateralities):
                data.append(new_var)
            for new_var in _get_laser_scar_type(macula_text, lateralities, 'MACULA'):
                data.append(new_var)
    else:
        if not lateralities:
            lateralities = build_laterality_table(text)
        for new_var in _get_laser_scar_type(text, lateralities, 'ALL'):
            data.append(new_var)
    return data


def _get_laser_scar_type(text: str, lateralities, source: str) -> dict:
    for pat_label, pat, variable in [
        ('FOCAL_PAT', FOCAL_PAT, 'focal_dr_laser_scar_type'),
        ('GRID_PAT', GRID_PAT, 'grid_dr_laser_scar_type'),
        ('MACULAR_PAT', MACULAR_PAT, 'macular_dr_laser_scar_type'),
    ]:
        for m in pat.finditer(text):
            negword = is_negated(m, text, word_window=3)
            yield create_new_variable(text, m, lateralities, variable, {
                'value': 0 if negword else 1,
                'term': m.group(),
                'label': 'no' if negword else 'yes',
                'negated': negword,
                'regex': pat_label,
                'source': source,
            })


def _get_lsr_macular_header(text: str, lateralities) -> dict:
    for m in MACULAR_HEADER_PAT.finditer(text):
        negword = is_negated(m, text, word_window=3)
        yield create_new_variable(text, m, lateralities, 'macular_dr_laser_scar_type', {
            'value': 0 if negword else 1,
            'term': m.group(),
            'label': 'no' if negword else 'yes',
            'negated': negword,
            'regex': 'MACULAR_HEADER_PAT',
            'source': 'MACULA',
        })
