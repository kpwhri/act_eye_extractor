import json
import pytest

from eye_extractor.common.severity import (
    FOUR_QUADRANT,
    MILD_PAT,
    MODERATE_PAT,
    ONE_QUADRANT,
    SEVERE_PAT,
    SEVERITY_PAT,
    THREE_QUADRANT,
    TWO_QUADRANT,
)

# Test pattern.
_pattern_cases = [
    (MILD_PAT, 'mild', True),
    (MODERATE_PAT, 'moderate', True),
    (SEVERE_PAT, 'severe', True),
    (SEVERE_PAT, 'very severe', True),
    (SEVERITY_PAT, 'severity=1Q', True),
    (SEVERITY_PAT, 'severity=2Q', True),
    (SEVERITY_PAT, 'severity=3Q', True),
    (SEVERITY_PAT, 'severity=4Q', True),
    (ONE_QUADRANT, 'inferior quadrant', True),
    (TWO_QUADRANT, 'temporal and inferior quadrant', True),
    (THREE_QUADRANT, 'temporal, inferior and nasal quadrants', True),
    (FOUR_QUADRANT, 'all quadrants', True),
]


def _get_pattern_cases():
    return [(x[0], x[1], x[2]) for x in _pattern_cases]


@pytest.mark.parametrize('pat, text, exp', _get_pattern_cases())
def test_severity_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) == exp
