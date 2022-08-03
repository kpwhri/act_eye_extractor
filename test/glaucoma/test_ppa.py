import json

import pytest

from eye_extractor.glaucoma.ppa import PPA_PAT, extract_ppa
from eye_extractor.output.glaucoma import build_ppa


@pytest.mark.parametrize('pat, text, exp', [
    (PPA_PAT, 'peri-papillary atrophy', True),
    (PPA_PAT, ' ppa ', True),
])
def test_ppa_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) == exp


@pytest.mark.parametrize('text, headers, exp_ppa_re, exp_ppa_le, exp_ppa_unk', [
    ('ppa', None, -1, -1, 1),
    ('peri-papillary atrophy OU', None, 1, 1, -1),
    ('no X; with peripapillary atrophy', None, -1, -1, 1),
    ('no ppa', None, -1, -1, 0),
])
def test_tilted_extract_and_build(text, headers, exp_ppa_re, exp_ppa_le, exp_ppa_unk):
    pre_json = extract_ppa(text, headers=headers, lateralities=None)
    post_json = json.loads(json.dumps(pre_json))
    result = build_ppa(post_json)
    assert result['ppa_re'] == exp_ppa_re
    assert result['ppa_le'] == exp_ppa_le
    assert result['ppa_unk'] == exp_ppa_unk
