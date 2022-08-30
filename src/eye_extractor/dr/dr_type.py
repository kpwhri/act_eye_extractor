import enum
import re

from eye_extractor.common.negation import is_negated
from eye_extractor.laterality import build_laterality_table, create_new_variable


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
    if not lateralities:
        lateralities = build_laterality_table(text)
    data = []
    for new_var in _get_dr_type(text, lateralities, 'ALL'):
        data.append(new_var)
    if headers:
        pass

    return data


# TODO: Create factory class for `get_<variable>` functions.
def _get_dr_type(text: str, lateralities, source: str) -> dict:
    for pat_label, pat, dr_type, dr_label in [
        ('NPDR_PAT', NPDR_PAT, DrType.NPDR, 'nonproliferative diabetic retinopathy'),
        ('PDR_PAT', PDR_PAT, DrType.PDR, 'proliferative diabetic retinopathy'),
    ]:
        for m in pat.finditer(text):
            negwords = {'no', 'or', 'neg', 'without', 'w/out', '(-)'}
            negated = is_negated(m, text, negwords, word_window=3)
            yield create_new_variable(text, m, lateralities, 'diabretinop_type', {
                'value': DrType.NONE if negated else dr_type,
                'term': m.group(),
                'label': f'No {dr_label}' if negated else dr_label,
                'negated': negated,
                'regex': pat_label,
                'source': source,
            })
