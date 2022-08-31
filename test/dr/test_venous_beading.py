import json
import pytest

from eye_extractor.dr.venous_beading import VEN_BEADING_PAT
from eye_extractor.output.dr import build_ven_beading

# Test pattern.
_pattern_cases = [
    (VEN_BEADING_PAT, 'Venous beading', True),
    (VEN_BEADING_PAT, 'VB', True),
    (VEN_BEADING_PAT, 'venous beading;', True),
]


def _get_pattern_cases():
    return [(x[0], x[1], x[2]) for x in _pattern_cases]


@pytest.mark.parametrize('pat, text, exp', _get_pattern_cases())
def test_ven_beading_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) == exp
