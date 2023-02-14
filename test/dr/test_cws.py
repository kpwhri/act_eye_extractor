import json
import pytest

from eye_extractor.dr.cws import CWS_PAT, get_cottonwspot
from eye_extractor.headers import Headers
from eye_extractor.output.dr import build_cottonwspot

# Test pattern.
_pattern_cases = [
    (CWS_PAT, 'CWS', True),
    (CWS_PAT, 'cotton-wool spots', True),
]


def _get_pattern_cases():
    return [(x[0], x[1], x[2]) for x in _pattern_cases]


@pytest.mark.parametrize('pat, text, exp', _get_pattern_cases())
def test_cws_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) == exp


# Test extract and build.
_cws_extract_and_build_cases = [
    ('No d/b hemes, CWS or NVE OU', {}, 0, 0, -1),
    # Unless specified, all conditions in negated list are OU.
    # Idea: process laterality differently in (negated)? list format.
    # Since no laterality specified, laterality should be OU.
    pytest.param('No Microaneurysms/hemes, cotton-wool spots, exudates, IRMA, Venous beading, NVE',
                 {}, 0, 0, -1, marks=pytest.mark.skip()),
]


@pytest.mark.parametrize('text, headers, exp_cottonwspot_re, exp_cottonwspot_le, exp_cottonwspot_unk',
                         _cws_extract_and_build_cases)
def test_cws_extract_and_build(text,
                               headers,
                               exp_cottonwspot_re,
                               exp_cottonwspot_le,
                               exp_cottonwspot_unk):
    pre_json = get_cottonwspot(text, headers=Headers(headers))
    post_json = json.loads(json.dumps(pre_json))
    result = build_cottonwspot(post_json)
    assert result['cottonwspot_re'] == exp_cottonwspot_re
    assert result['cottonwspot_le'] == exp_cottonwspot_le
    assert result['cottonwspot_unk'] == exp_cottonwspot_unk
