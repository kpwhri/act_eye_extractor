import json
import pytest

from eye_extractor.dr.venous_beading import get_ven_beading, VEN_BEADING_PAT
from eye_extractor.headers import Headers
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
    # ('venous beading ou', {}, 'MILD', 'MILD', 'UNKNOWN'),
    # ('mild VB OU', {}, 'MILD', 'MILD', 'UNKNOWN'),
    # ('Mild - moderate venous beading OD', {}, 'MODERATE', 'UNKNOWN', 'UNKNOWN'),
    # ('no venous beading ou', {}, 'NONE', 'NONE', 'UNKNOWN'),
    # ('moderate VB OS', {}, 'UNKNOWN', 'MODERATE', 'UNKNOWN'),
    # ('severe venous beading', {}, 'UNKNOWN', 'UNKNOWN', 'SEVERE'),
    # ('VB severity=3Q OS', {}, 'UNKNOWN', 'Q3', 'UNKNOWN'),
    # ('venous beading temporal and inferior quadrant OD', {}, 'Q2', 'UNKNOWN', 'UNKNOWN'),
    # ('nasal quadrant, VB', {}, 'UNKNOWN', 'UNKNOWN', 'Q1'),
    # ('VB in all quadrants ou', {}, 'Q4', 'Q4', 'UNKNOWN'),
    # ('(-)heme, MA, HE, CWS, VB, IRMA, NVE OU', {}, 'NONE', 'NONE', 'UNKNOWN'),
    # ('OU: No Microaneurysms/hemes, cotton-wool spots, exudates, IRMA, Venous beading',
    #  {}, 'NONE', 'NONE', 'UNKNOWN'),
    # ('no venous beading;', {}, 'UNKNOWN', 'UNKNOWN', 'NONE'),
    # ('Vessels: moderate A/V crossing changes, no venous beading',
    #  {}, 'UNKNOWN', 'UNKNOWN', 'NONE'),
    # ('no CWS, MA, IRMA, VB', {}, 'UNKNOWN', 'UNKNOWN', 'NONE'),
    # ('Vessels: Normal', {}, 'UNKNOWN', 'UNKNOWN', 'UNKNOWN'),
    ('Macula: focal OU; no CSME; ERM OS Vessels: good caliber and crossings; no venous beading; no plaques or emboli',
     {
         'Macula': 'focal OU; no CSME; ERM OS',
         'Vessels': 'good caliber and crossings; no venous beading; no plaques or emboli'
     },
     'UNKNOWN', 'UNKNOWN', 'NONE'),
    ('¶Macula: no CSME mild ERM OD ¶Vessels: good caliber and crossings; no venous beading; no plaques or emboli',
     {
         'Macula': 'no CSME mild ERM OD',
         'Vessels': 'good caliber and crossings; no venous beading; no plaques or emboli'
     },
     'UNKNOWN', 'UNKNOWN', 'NONE'),
    # Incorrectly grabbing OD from 'NVE OD' which only applies to NVE.
    # `next_commas` cutoff value = 3 won't work, only two intervening commas, 1 'value' (should rename) each
    # `_get_by_index_default_helper_check_prev_lat` not called, would need equivalent for `next_lat`
    # Idea: process laterality differently in (negated)? list format
    pytest.param('(-)heme, MA, HE, CWS, VB, IRMA, NVE OD, ERM OS',
                 {}, 'UNKNOWN', 'UNKNOWN', 'NONE', marks=pytest.mark.skip()),
]


@pytest.mark.parametrize('text, headers, exp_venbeading_re, exp_venbeading_le, exp_venbeading_unk',
                         _ven_beading_extract_and_build_cases)
def test_ven_beading_extract_and_build(text,
                                       headers,
                                       exp_venbeading_re,
                                       exp_venbeading_le,
                                       exp_venbeading_unk):
    pre_json = get_ven_beading(text, headers=Headers(headers))
    post_json = json.loads(json.dumps(pre_json))
    result = build_ven_beading(post_json)
    assert result['venbeading_re'] == exp_venbeading_re
    assert result['venbeading_le'] == exp_venbeading_le
    assert result['venbeading_unk'] == exp_venbeading_unk
