import json

import pytest

from eye_extractor.amd.scar import extract_subret_fibrous, SCAR_PAT, MACULAR_SCAR_PAT, SUBRET_SCAR_PAT, \
    DISCIFORM_SCAR_PAT
from eye_extractor.headers import Headers
from eye_extractor.output.amd import build_subret_fibrous


@pytest.mark.parametrize('pat, text, exp', [
    (SCAR_PAT, 'scar', True),
    (MACULAR_SCAR_PAT, 'macular scar', True),
    (SUBRET_SCAR_PAT, 'sub ret scar', True),
    (SUBRET_SCAR_PAT, 'subretinal scar', True),
    (DISCIFORM_SCAR_PAT, 'disciform scar', True),
])
def test_scar_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) is exp


@pytest.mark.parametrize('text, headers, exp_subret_fibrous_re, exp_subret_fibrous_le, exp_subret_fibrous_unk', [
        ('', {'MACULA': 'scar'}, 'UNKNOWN', 'UNKNOWN', 'YES'),
    ])
def test_scar_extract_build(text, headers, exp_subret_fibrous_re, exp_subret_fibrous_le, exp_subret_fibrous_unk):
    pre_json = extract_subret_fibrous(text, headers=Headers(headers))
    post_json = json.loads(json.dumps(pre_json))
    result = build_subret_fibrous(post_json)
    assert result['subret_fibrous_re'] == exp_subret_fibrous_re
    assert result['subret_fibrous_le'] == exp_subret_fibrous_le
    assert result['subret_fibrous_unk'] == exp_subret_fibrous_unk
