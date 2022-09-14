import enum
import re

from eye_extractor.common.negation import is_negated, NEGWORDS
from eye_extractor.common.severity import extract_severity, Severity
from eye_extractor.laterality import build_laterality_table, create_new_variable


class DrType(enum.IntEnum):
    UNKNOWN = -1
    NONE = 0
    NPDR = 1
    PDR = 2


NPDR_PAT = re.compile(
    r'\b('
    r'npdr'
    r'|non(\W*)?proliferative\s+(diabetic\s+retinopathy|dr)'
    r'|bdr'
    r'|background\s+diabetic\s+retinopathy'
    r')\b',
    re.I
)
PDR_PAT = re.compile(
    r'\b('
    r'pdr|proliferative\s+(diabetic\s+retinopathy|dr)'
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
    for pat_label, pat, dr_type, dr_label, sev_var in [
        ('NPDR_PAT', NPDR_PAT, DrType.NPDR, 'nonproliferative diabetic retinopathy', 'nonprolifdr'),
        ('PDR_PAT', PDR_PAT, DrType.PDR, 'proliferative diabetic retinopathy', 'prolifdr'),
    ]:
        for m in pat.finditer(text):
            negated = is_negated(m, text, NEGWORDS, word_window=3)
            context = f'{text[max(0, m.start() - 100): m.start()]} {text[m.end():min(len(text), m.end() + 100)]}'
            severities = extract_severity(context)
            if severities:
                for sev in severities:
                    yield create_new_variable(text, m, lateralities, sev_var, {
                        'value': sev,
                        'term': m.group(),
                        'label': dr_label,
                        'negated': negated,
                        'regex': pat_label,
                        'source': source,
                    })
            elif negated:
                yield create_new_variable(text, m, lateralities, sev_var, {
                    'value': Severity.NONE,
                    'term': m.group(),
                    'label': f'No {dr_label}',
                    'negated': negated,
                    'regex': pat_label,
                    'source': source,
                })

            yield create_new_variable(text, m, lateralities, 'diabretinop_type', {
                'value': DrType.NONE if negated else dr_type,
                'term': m.group(),
                'label': f'No {dr_label}' if negated else dr_label,
                'negated': negated,
                'regex': pat_label,
                'source': source,
            })

