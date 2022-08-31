import json
import pytest

from eye_extractor.common.severity import Severity
from eye_extractor.dr.dr_type import (
    DrType,
    get_dr_type,
    NPDR_PAT,
    PDR_PAT
)
from eye_extractor.output.dr import build_dr_type, build_npdr_severity, build_pdr_severity

# Test pattern.
_dr_type_pattern_cases = [
    (NPDR_PAT, 'NPDR', True),
    (NPDR_PAT, 'non-proliferative diabetic retinopathy', True),
    (NPDR_PAT, 'Nonproliferative diabetic retinopathy', True),
    (NPDR_PAT, 'Non proliferative diabetic retinopathy', True),
    (NPDR_PAT, 'NONPROLIFERATIVE DIABETIC RETINOPATHY', True),
    (NPDR_PAT, 'BDR', True),
    (NPDR_PAT, 'non-proliferative DR)', True),
    (PDR_PAT, 'PDR', True),
    (PDR_PAT, 'Proliferative Diabetic Retinopathy', True),
    (PDR_PAT, 'proliferative diabetic retinopathy', True),
    (PDR_PAT, 'PROLIFERATIVE DIABETIC RETINOPATHY', True),
]


def _get_pattern_cases(cases):
    return [(x[0], x[1], x[2]) for x in cases]


@pytest.mark.parametrize('pat, text, exp', _get_pattern_cases(_dr_type_pattern_cases))
def test_dr_type_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) == exp


# Test extract and build.
_dr_type_extract_and_build_cases = [
    ('Type II DM with mild - moderate NPDR ou', {}, DrType.NPDR, DrType.NPDR, DrType.UNKNOWN),
    ('DM w/out NPDR OU', {}, DrType.NONE, DrType.NONE, DrType.UNKNOWN),
    ('no NPDR', {}, DrType.UNKNOWN, DrType.UNKNOWN, DrType.NONE),
    ('MODERATE NONPROLIFERATIVE DIABETIC RETINOPATHY OD', {}, DrType.NPDR, DrType.UNKNOWN, DrType.UNKNOWN),
    ('proliferative Diabetic Retinopathy: YES, MILD OU', {}, DrType.PDR, DrType.PDR, DrType.UNKNOWN),
    ('Proliferative diabetic retinopathy OS', {}, DrType.UNKNOWN, DrType.PDR, DrType.UNKNOWN),
    ('Hx of pdr od', {}, DrType.PDR, DrType.UNKNOWN, DrType.UNKNOWN),
    ('Uncontrolled Proliferative Diabetic Retinopathy', {}, DrType.UNKNOWN, DrType.UNKNOWN, DrType.PDR),
]

_npdr_severity_extract_and_build_cases = [
    ('mild BDR OU', {}, 'MILD', 'MILD', 'UNKNOWN'),
    ('Mild - moderate non-proliferative DR OD', {}, 'MODERATE', 'UNKNOWN', 'UNKNOWN'),
    ('no NPDR ou', {}, 'NONE', 'NONE', 'UNKNOWN'),
    ('moderate background diabetic retinopathy OS', {}, 'UNKNOWN', 'MODERATE', 'UNKNOWN'),
    ('severe NPDR', {}, 'UNKNOWN', 'UNKNOWN', 'SEVERE')
]

_pdr_severity_extract_and_build_cases = [
    ('mild PDR OU', {}, 'MILD', 'MILD', 'UNKNOWN'),
    ('Mild - moderate proliferative DR OD', {}, 'MODERATE', 'UNKNOWN', 'UNKNOWN'),
    ('no PDR ou', {}, 'NONE', 'NONE', 'UNKNOWN'),
    ('moderate proliferative diabetic retinopathy OS', {}, 'UNKNOWN', 'MODERATE', 'UNKNOWN'),
    ('severe proliferative DR', {}, 'UNKNOWN', 'UNKNOWN', 'SEVERE')
]


@pytest.mark.parametrize('text, headers, exp_diabretinop_type_re, exp_diabretinop_type_le, '
                         'exp_diabretinop_type_unk',
                         _dr_type_extract_and_build_cases)
def test_dr_type_extract_and_build(text,
                                   headers,
                                   exp_diabretinop_type_re,
                                   exp_diabretinop_type_le,
                                   exp_diabretinop_type_unk):
    pre_json = get_dr_type(text)
    post_json = json.loads(json.dumps(pre_json))
    result = build_dr_type(post_json)
    assert result['diabretinop_type_re'] == exp_diabretinop_type_re
    assert result['diabretinop_type_le'] == exp_diabretinop_type_le
    assert result['diabretinop_type_unk'] == exp_diabretinop_type_unk


@pytest.mark.parametrize('text, headers, exp_nonprolifdr_re, exp_nonprolifdr_le, '
                         'exp_nonprolifdr_unk',
                         _npdr_severity_extract_and_build_cases)
def test_npdr_severity_extract_and_build(text,
                                         headers,
                                         exp_nonprolifdr_re,
                                         exp_nonprolifdr_le,
                                         exp_nonprolifdr_unk):
    pre_json = get_dr_type(text)
    post_json = json.loads(json.dumps(pre_json))
    result = build_npdr_severity(post_json)
    assert result['nonprolifdr_re'] == exp_nonprolifdr_re
    assert result['nonprolifdr_le'] == exp_nonprolifdr_le
    assert result['nonprolifdr_unk'] == exp_nonprolifdr_unk


@pytest.mark.parametrize('text, headers, exp_prolifdr_re, exp_prolifdr_le, '
                         'exp_prolifdr_unk',
                         _pdr_severity_extract_and_build_cases)
def test_pdr_severity_extract_and_build(text,
                                        headers,
                                        exp_prolifdr_re,
                                        exp_prolifdr_le,
                                        exp_prolifdr_unk):
    pre_json = get_dr_type(text)
    post_json = json.loads(json.dumps(pre_json))
    result = build_pdr_severity(post_json)
    assert result['prolifdr_re'] == exp_prolifdr_re
    assert result['prolifdr_le'] == exp_prolifdr_le
    assert result['prolifdr_unk'] == exp_prolifdr_unk
