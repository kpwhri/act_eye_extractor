import json
import pytest

from eye_extractor.dr.dr_type import (
    DrType,
    get_dr_type,
    NPDR_PAT,
    PDR_PAT
)
from eye_extractor.output.dr import build_dr_type

# Test pattern.
_pattern_cases = [
    (NPDR_PAT, 'NPDR', True),
    (NPDR_PAT, 'non-proliferative diabetic retinopathy', True),
    (NPDR_PAT, 'Nonproliferative diabetic retinopathy', True),
    (NPDR_PAT, 'Non proliferative diabetic retinopathy', True),
    (NPDR_PAT, 'NONPROLIFERATIVE DIABETIC RETINOPATHY', True),
    (PDR_PAT, 'PDR', True),
    (PDR_PAT, 'Proliferative Diabetic Retinopathy', True),
    (PDR_PAT, 'proliferative diabetic retinopathy', True),
    (PDR_PAT, 'PROLIFERATIVE DIABETIC RETINOPATHY', True),
]


def _get_pattern_cases():
    return [(x[0], x[1], x[2]) for x in _pattern_cases]


@pytest.mark.parametrize('pat, text, exp', _get_pattern_cases())
def test_dr_type_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) == exp


# Test extract and build.
_dr_type_extract_and_build_cases = [
    ('Type II DM with mild - moderate ou', {}, DrType.NPDR, DrType.NPDR, DrType.UNKNOWN),
    ('DM w/out NPDR OU', {}, DrType.NONE, DrType.NONE, DrType.UNKNOWN),
    ('no NPDR', {}, DrType.UNKNOWN, DrType.UNKNOWN, DrType.NONE),
    ('MODERATE NONPROLIFERATIVE DIABETIC RETINOPATHY OD', {}, DrType.NPDR, DrType.UNKNOWN, DrType.UNKNOWN),
    ('proliferative Diabetic Retinopathy: YES, MILD OU', {}, DrType.PDR, DrType.PDR, DrType.UNKNOWN),
    ('Proliferative diabetic retinopathy OS', {}, DrType.UNKNOWN, DrType.PDR, DrType.UNKNOWN),
    ('Hx of pdr od', {}, DrType.PDR, DrType.UNKNOWN, DrType.UNKNOWN),
    ('Uncontrolled Proliferative Diabetic Retinopathy', {}, DrType.UNKNOWN, DrType.UNKNOWN, DrType.PDR),
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
