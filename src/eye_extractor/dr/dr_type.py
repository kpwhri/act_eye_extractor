import enum
import re

from eye_extractor.dr.dr_yesno import DR_YESNO_PAT
from eye_extractor.nlp.negate.negation import has_before, has_after, is_negated, is_post_negated
from eye_extractor.common.severity import extract_risk, extract_severity, Risk, Severity
from eye_extractor.laterality import build_laterality_table, create_new_variable


class DrType(enum.IntEnum):
    UNKNOWN = -1
    NONE = 0
    YES_NOS = 1
    NPDR = 2
    PDR = 3


NPDR_PAT = re.compile(
    r'\b('
    r'npdr'
    r'|(background|non(\W*)?proliferative)\s+(diabetic\s+retinopathy|dr)'
    r'|bg?dr'
    r')\b',
    re.I
)
PDR_PAT = re.compile(
    r'\b('
    r'pdr|proliferative\s+(diabetic\s+retinopathy|dr)'
    r')\b',
    re.I
)
DR_NOS_PAT = re.compile(
    r'\b('
    r'diabetic\s+retinopathy'
    r')\b',
    re.I
)
# Separate pattern to capture case-sensitive abbreviations.
DR_NOS_ABBR_PAT = re.compile(
    r'\b('
    r'DR|dr'
    r')\b',
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
        ('PDR_PAT', PDR_PAT, DrType.PDR, 'proliferative diabetic retinopathy', None),
        ('DR_NOS_PAT', DR_NOS_PAT, DrType.YES_NOS, 'diabetic retinopathy', None),
        ('DR_NOS_ABBR_PAT', DR_NOS_ABBR_PAT, DrType.YES_NOS, 'diabetic retinopathy', None),
    ]:

        for m in pat.finditer(text):
            if has_before(m if isinstance(m, int) else m.start(),
                          text,
                          terms={'confirm'},
                          word_window=2):
                break
            if dr_type is DrType.YES_NOS:
                if has_before(m if isinstance(m, int) else m.start(),
                              text,
                              terms={'confirm', 'surgeon', 'tablet', 'exam'},
                              word_window=2,
                              boundary_chars='¶'):
                    break
                elif has_after(m if isinstance(m, int) else m.start(),
                               text,
                               terms={'exam'},
                               word_window=6):
                    break
            negated = (
                is_negated(m, text, word_window=3)
                or is_post_negated(m, text, terms={'no'}, word_window=3)
            )
            context = f'{text[max(0, m.start() - 100): m.start()]} {text[m.end():min(len(text), m.end() + 100)]}'
            severities = extract_severity(context)
            if sev_var:
                # Severity found & positive instance.
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
                # Severity found & negative instance.
                elif negated:
                    yield create_new_variable(text, m, lateralities, sev_var, {
                        'value': Severity.NONE,
                        'term': m.group(),
                        'label': f'No {dr_label}',
                        'negated': negated,
                        'regex': pat_label,
                        'source': source,
                    })
                # Affirmative without severity quantifier.
                else:
                    yield create_new_variable(text, m, lateralities, sev_var, {
                        'value': Severity.YES_NOS,
                        'term': m.group(),
                        'label': dr_label,
                        'negated': negated,
                        'regex': pat_label,
                        'source': source,
                    })
            # Severity not found and negative instance.
            if negated:
                yield create_new_variable(text, m, lateralities, 'diabretinop_type', {
                    'value': DrType.NONE,
                    'term': m.group(),
                    'label': f'No {dr_label}' if negated else dr_label,
                    'negated': negated,
                    'regex': pat_label,
                    'source': source,
                })
            # Severity not found, positive instance.
            else:
                yield create_new_variable(text, m, lateralities, 'diabretinop_type', {
                    'value': dr_type,
                    'term': m.group(),
                    'label': dr_label,
                    'negated': negated,
                    'regex': pat_label,
                    'source': source,
                })


def get_pdr(text: str, *, headers=None, lateralities=None) -> list:
    if not lateralities:
        lateralities = build_laterality_table(text)
    data = []
    for new_var in _get_pdr(text, lateralities, 'ALL'):
        data.append(new_var)
    if headers:
        pass

    return data


# TODO: Create factory class for `get_<variable>` functions.
def _get_pdr(text: str, lateralities, source: str) -> dict:
    for m in PDR_PAT.finditer(text):
        negated = (
            is_negated(m, text, word_window=3)
            or is_post_negated(m, text, terms={'no'}, word_window=3)
        )
        context = f'{text[max(0, m.start() - 100): m.start()]} {text[m.end():min(len(text), m.end() + 100)]}'
        risks = extract_risk(context)
        if has_before(m if isinstance(m, int) else m.start(),
                      text,
                      terms={'confirm'},
                      word_window=2):
            break
        if risks:
            for risk in risks:
                yield create_new_variable(text, m, lateralities, 'prolifdr', {
                    'value': risk,
                    'term': m.group(),
                    'label': 'proliferative diabetic retinopathy',
                    'negated': negated,
                    'regex': 'PDR_PAT',
                    'source': source,
                })
        elif negated:
            yield create_new_variable(text, m, lateralities, 'prolifdr', {
                'value': Risk.NONE,
                'term': m.group(),
                'label': 'No proliferative diabetic retinopathy',
                'negated': negated,
                'regex': 'PDR_PAT',
                'source': source,
            })
        else:  # Affirmative without severity quantifier.
            yield create_new_variable(text, m, lateralities, 'prolifdr', {
                'value': Risk.YES_NOS,
                'term': m.group(),
                'label': 'proliferative diabetic retinopathy',
                'negated': negated,
                'regex': 'PDR_PAT',
                'source': source,
            })
