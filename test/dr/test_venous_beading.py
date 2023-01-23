import json
import pytest

from eye_extractor.dr.venous_beading import get_ven_beading, VEN_BEADING_PAT
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


# Test extract and build.
_ven_beading_extract_and_build_cases = [
    ('venous beading ou', {}, 'MILD', 'MILD', 'UNKNOWN'),
    ('mild VB OU', {}, 'MILD', 'MILD', 'UNKNOWN'),
    ('Mild - moderate venous beading OD', {}, 'MODERATE', 'UNKNOWN', 'UNKNOWN'),
    ('no venous beading ou', {}, 'NONE', 'NONE', 'UNKNOWN'),
    ('moderate VB OS', {}, 'UNKNOWN', 'MODERATE', 'UNKNOWN'),
    ('severe venous beading', {}, 'UNKNOWN', 'UNKNOWN', 'SEVERE'),
    ('VB severity=3Q OS', {}, 'UNKNOWN', 'Q3', 'UNKNOWN'),
    ('venous beading temporal and inferior quadrant OD', {}, 'Q2', 'UNKNOWN', 'UNKNOWN'),
    ('nasal quadrant, VB', {}, 'UNKNOWN', 'UNKNOWN', 'Q1'),
    ('VB in all quadrants ou', {}, 'Q4', 'Q4', 'UNKNOWN'),
    ('(-)heme, MA, HE, CWS, VB, IRMA, NVE OU', {}, 'NONE', 'NONE', 'UNKNOWN'),
    # Incorrectly grabbing OD from 'Macula' section. Ideas: control context
    pytest.param('¶Macula: no CSME mild ERM OD ¶Vessels: good caliber and crossings; no venous beading; no plaques or '
                 'emboli', {}, 'UNKNOWN', 'UNKNOWN', 'NONE', marks=pytest.mark.skip()),
]


@pytest.mark.parametrize('text, headers, exp_venbeading_re, exp_venbeading_le, exp_venbeading_unk',
                         _ven_beading_extract_and_build_cases)
def test_ven_beading_extract_and_build(text,
                                       headers,
                                       exp_venbeading_re,
                                       exp_venbeading_le,
                                       exp_venbeading_unk):
    pre_json = get_ven_beading(text)
    post_json = json.loads(json.dumps(pre_json))
    result = build_ven_beading(post_json)
    assert result['venbeading_re'] == exp_venbeading_re
    assert result['venbeading_le'] == exp_venbeading_le
    assert result['venbeading_unk'] == exp_venbeading_unk
