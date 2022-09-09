import json
import pytest

from eye_extractor.dr.peripheral import PERI_HEME_PAT, PRP_SCARS_PAT

# Test pattern.
_pattern_cases = [
    (PERI_HEME_PAT, 'peripheral hemorrhage', True),
    (PERI_HEME_PAT, 'peripheral heme', True),
    (PRP_SCARS_PAT, 'prp laser scars', True),
    (PRP_SCARS_PAT, 'PRP laser scar OU', True),
    (PRP_SCARS_PAT, 'laser panretinal photo-coagulation scars', True),
]


def _get_pattern_cases():
    return [(x[0], x[1], x[2]) for x in _pattern_cases]


@pytest.mark.parametrize('pat, text, exp', _get_pattern_cases())
def test_laser_scar_type_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) == exp
