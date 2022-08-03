import json

import pytest

from eye_extractor.amd.vitamins import VITAMIN_PAT, CONTINUE_VITAMIN_PAT, extract_amd_vitamin
from eye_extractor.headers import Headers
from eye_extractor.output.amd import build_amd_vitamin


@pytest.mark.parametrize('pat, text, exp', [
    (VITAMIN_PAT, 'ocuvite', True),
    (VITAMIN_PAT, 'preservision', True),
    (CONTINUE_VITAMIN_PAT, 'continue taking preservision', True),
])
def test_vitamin_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) is exp


@pytest.mark.parametrize('text, headers, exp_amd_vitamin', [
    ('', {'EYE MEDICATIONS': 'ocuvite'}, 1),
    ('', {'MEDICATIONS': 'ocuvite'}, 1),
    ('Continue using ocuvite', None, 1),
])
def test_vitamin_extract_build(text, headers, exp_amd_vitamin):
    pre_json = extract_amd_vitamin(text, headers=Headers(headers))
    post_json = json.loads(json.dumps(pre_json))
    result = build_amd_vitamin(post_json)
    assert result['amd_vitamin'] == exp_amd_vitamin
