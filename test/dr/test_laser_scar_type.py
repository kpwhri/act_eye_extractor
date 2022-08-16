import pytest

from eye_extractor.dr.laser_scar_type as lst
from eye_extractor.output.dr import build_laser_scar_type

_pattern_cases = [
    (lst.PANRETINAL_PAT, 'panretinal laser scars', True),
    (lst.PANRETINAL_PAT, 'PRP scars', True),
    (lst.FOCAL_PAT, 'focal laser scars', True),
    (lst.FOCAL_PAT, 'focal tx scars', True),
    (lst.GRID_PAT, 'focal (grid) scars', True),
    (lst.GRID_PAT, 'grid laser scars', True),
    (lst.MACULAR_PAT, 'macular scars', True),
    (lst.MACULAR_PAT, 'MACULA: laser scars', True),
]

# _extract_and_build_cases = [
#     ('', {'ASSESSMENT': 'laser therapy od'}, 1, -1, -1),
#     ('', {'ASSESSMENT': 'OS: Photodynamic therapy'}, -1, 2, -1),
#     ('', {'ASSESSMENT': 'thermal laser'}, -1, -1, 3),
# ]


def _get_pattern_cases():
    return [(x[0], x[1], x[2]) for x in _pattern_cases]


@pytest.mark.parametrize('pat, text, exp', _get_pattern_cases())
def test_treatment_patterns_for_lasertype(pat, text, exp):
    m = pat.search(text)
    assert bool(m) == exp