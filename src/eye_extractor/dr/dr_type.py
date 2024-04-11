import enum
import re

from eye_extractor.dr.dr_yesno import DR_YESNO_PAT, DR_YESNO_ABBR_PAT, DR_YESNO_NEG_PAT, filter_dr_yesno_context
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
        ('DR_YESNO_NEG_PAT', DR_YESNO_NEG_PAT, DrType.YES_NOS, 'diabetic retinopathy', None),
        ('DR_YESNO_PAT', DR_YESNO_PAT, DrType.YES_NOS, 'diabetic retinopathy', None),
        ('DR_YESNO_ABBR_PAT', DR_YESNO_ABBR_PAT, DrType.YES_NOS, 'diabetic retinopathy', None),
    ]:
        for m in pat.finditer(text):
            if dr_type is DrType.YES_NOS:
                if filter_dr_yesno_context(m, text, pat_label=pat_label):
                    continue
                if pat_label is 'DR_YESNO_NEG_PAT':
                    yield create_new_variable(text, m, lateralities, 'diabretinop_type', {
                        'value': DrType.NONE,
                        'term': m.group(),
                        'label': 'No',
                        'negated': None,
                        'regex': pat_label,
                        'source': source,
                    })
                else:
                    negated = (
                        is_negated(m, text, word_window=4, boundary_chars=':¶)')
                        or is_post_negated(m, text,
                                           terms={'no'},
                                           word_window=1,
                                           boundary_chars=';¶',
                                           skip_n_boundary_chars=0)
                    )
            else:
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
            yield create_new_variable(text, m, lateralities, 'diabretinop_type', {
                'value': DrType.NONE if negated else dr_type,
                'term': m.group(),
                'label': f'No {dr_label}' if negated else dr_label,
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
            continue
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
