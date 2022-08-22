import pytest

from eye_extractor.dr import dr_type as drt

# Test pattern.
_pattern_cases = [
    (drt.NPDR_PAT, 'NPDR', True),
    (drt.NPDR_PAT, 'non-proliferative diabetic retinopathy', True),
    (drt.NPDR_PAT, 'Nonproliferative diabetic retinopathy', True),
    (drt.NPDR_PAT, 'NONPROLIFERATIVE DIABETIC RETINOPAHTY', True),
    (drt.PDR_PAT, 'PDR', True),
    (drt.PDR_PAT, 'Proliferative Diabetic Retinopathy', True),
    (drt.PDR_PAT, 'proliferative diabetic retinopathy', True),
    (drt.PDR_PAT, 'PROLIFERATIVE DIABETIC RETINOPATHY', True),
]


def _get_pattern_cases():
    return [(x[0], x[1], x[2]) for x in _pattern_cases]


@pytest.mark.parametrize('pat, text, exp', _get_pattern_cases())
def test_dr_type_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) == exp
