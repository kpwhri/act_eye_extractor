import json
import pytest

from eye_extractor.common.algo.treatment import extract_treatment, FOCAL_PAT, PRP_PAT
from eye_extractor.headers import Headers
from eye_extractor.output.dr import build_dr_tx

# Test pattern.
_pattern_cases = [
    (PRP_PAT, 'prp laser', True),
    (PRP_PAT, 'PRP laser OU', True),
    (PRP_PAT, 'laser panretinal photo-coagulation', True),
    (FOCAL_PAT, 'focal laser', True),
]


def _get_pattern_cases():
    return [(x[0], x[1], x[2]) for x in _pattern_cases]


@pytest.mark.parametrize('pat, text, exp', _get_pattern_cases())
def test_dr_tx_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) == exp


# Test extract and build.
@pytest.mark.parametrize('text, headers, exp_drtreatment_re, exp_drtreatment_le, exp_drtreatment_unk', [
    ('', {'PLAN': 'observe'}, -1, -1, 1),
    ('', {'PLAN': 'PRP Laser OU'}, 2, 2, -1),
    ('injection of Avastin (Bevacizumab)', {}, -1, -1, 3),
    ('', {'PLAN': 'surgery'}, -1, -1, 4),
    ('', {'PLAN': 'focal laser'}, -1, -1, 6),
    ('', {'PLAN': 'laser'}, -1, -1, 5)
])
def test_dr_treatment_extract_and_build(text, headers, exp_drtreatment_re, exp_drtreatment_le, exp_drtreatment_unk):
    pre_json = extract_treatment(text, headers=Headers(headers), lateralities=None)
    post_json = json.loads(json.dumps(pre_json))
    result = build_dr_tx(post_json)
    assert result['drtreatment_re'] == exp_drtreatment_re
    assert result['drtreatment_le'] == exp_drtreatment_le
    assert result['drtreatment_unk'] == exp_drtreatment_unk
