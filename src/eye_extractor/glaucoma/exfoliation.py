"""
Exfoliation, but not glaucoma.
"""
import enum
import re

from eye_extractor.common.negation import has_before, has_after, is_negated, NEGWORDS
from eye_extractor.laterality import build_laterality_table, create_new_variable


class Exfoliation(enum.IntEnum):
    UNKNOWN = -1
    NO = 0
    YES = 1


EXFOLIATION_PAT = re.compile(
    rf'(?:'
    rf'\b(?:p[de]x|pxf|xfs)\b'
    rf'|'
    rf'capsulare'
    rf'|'
    rf'(?:pseudo\W*)?exfoll?iat\w*'
    rf')',
    re.I
)


def extract_exfoliation(text, *, headers=None, lateralities=None):
    lateralities = lateralities or build_laterality_table(text)
    data = []
    for m in EXFOLIATION_PAT.finditer(text):
        matchedtext = m.group()
        # cannot include glaucoma
        if has_before(m.start(), text, {'glauc', 'gl', 'glaucoma'},
                      word_window=3, skip_n_boundary_chars=1):
            continue
        elif has_after(m.end(), text, {'glauc', 'gl', 'glaucoma'},
                       word_window=3):
            continue
        negword = is_negated(m, text, NEGWORDS)
        data.append(
            create_new_variable(text, m, lateralities, 'exfoliation', {
                'value': Exfoliation.NO if negword else Exfoliation.YES,
                'term': matchedtext,
                'label': 'no' if negword else 'yes',
                'negated': negword,
                'regex': 'EXFOLIATION_PAT',
                'source': 'ALL',
            })
        )
    return data
