import json
import pytest


# Test pattern.
_pattern_cases = [
    # (NPDR_PAT, 'NPDR', True),
    # (NPDR_PAT, 'non-proliferative diabetic retinopathy', True),
    # (NPDR_PAT, 'Nonproliferative diabetic retinopathy', True),
    # (NPDR_PAT, 'Non proliferative diabetic retinopathy', True),
    # (NPDR_PAT, 'NONPROLIFERATIVE DIABETIC RETINOPATHY', True),
]


def _get_pattern_cases():
    return [(x[0], x[1], x[2]) for x in _pattern_cases]


@pytest.mark.parametrize('pat, text, exp', _get_pattern_cases())
def test_severity_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) == exp
