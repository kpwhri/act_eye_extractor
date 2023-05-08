import json
import pytest

from eye_extractor.common.severity import (
    extract_severity,
    MILD_PAT,
    MODERATE_PAT,
    Q1_PAT,
    Q2_PAT,
    Q3_PAT,
    Q4_PAT,
    SEVERE_PAT,
    Severity,
    SEVERITY_PAT,
    VERY_SEVERE_PAT,
)

# Test pattern.
_pattern_cases = [
    (MILD_PAT, 'mild', True),
    (MODERATE_PAT, 'moderate', True),
    (SEVERE_PAT, 'severe', True),
    (VERY_SEVERE_PAT, 'very severe', True),
    (SEVERITY_PAT, 'severity=1Q', True),
    (SEVERITY_PAT, 'severity=2Q', True),
    (SEVERITY_PAT, 'severity=3Q', True),
    (SEVERITY_PAT, 'severity=4Q', True),
    (Q1_PAT, 'inferior quadrant', True),
    (Q2_PAT, 'temporal and inferior quadrant', True),
    (Q3_PAT, 'temporal, inferior and nasal quadrants', True),
    (Q4_PAT, 'all quadrants', True),
]


def _get_pattern_cases():
    return [(x[0], x[1], x[2]) for x in _pattern_cases]


@pytest.mark.parametrize('pat, text, exp', _get_pattern_cases())
def test_severity_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) == exp


# Test extract and build.
_dr_severity_extract_cases = [
    ('very mild', [Severity.MILD]),
    ('mild - moderate', [Severity.MODERATE, Severity.MILD]),
    ('moderate', [Severity.MODERATE]),
    ('very severe', [Severity.VERY_SEVERE]),
    ('heme severity=3Q', [Severity.Q3]),
    ('heme temporal and inferior quadrant', [Severity.Q2, Severity.Q1]),
    ('IRMA nasal quadrant', [Severity.Q1]),
    ('heme in all quadrants', [Severity.Q4])
]


@pytest.mark.parametrize('text, labels',
                         _dr_severity_extract_cases)
def test_extract_severity(text, labels):
    severities = extract_severity(text)
    for i, sev in enumerate(severities):
        assert sev == labels[i]
