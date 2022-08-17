import enum
import re

from eye_extractor.common.negation import is_negated
from eye_extractor.laterality import build_laterality_table, create_new_variable

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
MACULAR_PAT = re.compile(
    r'\b('
    r'((macula(r)?)|MACULA:)(\W*\w+){0,3}\W*(laser\W*)?scars'
    r'|(laser\W*)?scars(\W*\w+){0,3}\W*macula(r)?'
    r')\b'
)


def get_laser_scar_type(text, *, headers=None, lateralities=None):
    if not lateralities:
        lateralities = build_laterality_table(text)
    data = []
    for pat_label, pat, variable in [
        ('FOCAL_PAT', FOCAL_PAT, 'focal_dr_laser_scar_type'),
        ('GRID_PAT', GRID_PAT, 'grid_dr_laser_scar_type'),
        ('MACULAR_PAT', MACULAR_PAT, 'macular_dr_laser_scar_type'),
    ]:
        if headers:
            for sect_name, sect_text in headers.iterate('MACULA'):
                for m in pat.finditer(sect_text):
                    negword = is_negated(m, text, {'no', 'or', 'neg', 'without'}, word_window=3)
                    data.append(
                        create_new_variable(text, m, lateralities, variable, {
                            'value': 0 if negword else 1,
                            'term': m.group(),
                            'label': 'no' if negword else 'yes',
                            'negated': negword,
                            'regex': pat_label,
                            'source': sect_name,
                        })
                    )
        else:
            for m in pat.finditer(text):
                negword = is_negated(m, text, {'no', 'or', 'neg', 'without'}, word_window=3)
                data.append(
                    create_new_variable(text, m, lateralities, variable, {
                        'value': 0 if negword else 1,
                        'term': m.group(),
                        'label': 'no' if negword else 'yes',
                        'negated': negword,
                        'regex': pat_label,
                        'source': 'ALL',
                    })
                )
    return data
