import json
import pytest

from eye_extractor.dr.irma import IRMA_PAT
# from eye_extractor.output.dr import build_irma

# Test pattern.
_pattern_cases = [
    (IRMA_PAT, 'IRMA', True),
    (IRMA_PAT, 'intraretinal microvascular abnormality', True),
]


def _get_pattern_cases():
    return [(x[0], x[1], x[2]) for x in _pattern_cases]


@pytest.mark.parametrize('pat, text, exp', _get_pattern_cases())
def test_irma_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) == exp


# Test extract and build.
_irma_extract_and_build_cases = [
    ('OD: area of IRMA just nasal to disc', {}, 'MILD', 'UNKNOWN', 'UNKNOWN'),
    ('mild IRMA OU', {}, 'MILD', 'MILD', 'UNKNOWN'),
    ('Mild - moderate IRMA OD', {}, 'MODERATE', 'UNKNOWN', 'UNKNOWN'),
    ('no intraretinal microvascular abnormality ou', {}, 'NONE', 'NONE', 'UNKNOWN'),
    ('moderate IRMA OS', {}, 'UNKNOWN', 'MODERATE', 'UNKNOWN'),
    ('severe intraretinal microvascular abnormality', {}, 'UNKNOWN', 'UNKNOWN', 'SEVERE'),
    ('IRMA severity=3Q OS', {}, 'UNKNOWN', 'Q3', 'UNKNOWN'),
    ('IRMA temporal and inferior quadrant OD', {}, 'Q2', 'UNKNOWN', 'UNKNOWN'),
    ('nasal quadrant, IRMA', {}, 'UNKNOWN', 'UNKNOWN', 'Q1'),
    ('IRMA in all quadrants ou', {}, 'Q4', 'Q4', 'UNKNOWN'),
]


# @pytest.mark.parametrize('text, headers, exp_venbeading_re, exp_venbeading_le, exp_venbeading_unk',
#                          _ven_beading_extract_and_build_cases)
# def test_ven_beading_extract_and_build(text,
#                                        headers,
#                                        exp_venbeading_re,
#                                        exp_venbeading_le,
#                                        exp_venbeading_unk):
#     pre_json = get_ven_beading(text)
#     post_json = json.loads(json.dumps(pre_json))
#     result = build_ven_beading(post_json)
#     assert result['venbeading_re'] == exp_venbeading_re
#     assert result['venbeading_le'] == exp_venbeading_le
#     assert result['venbeading_unk'] == exp_venbeading_unk
