import json

import pytest

from eye_extractor.glaucoma.disc_pallor import DISC_PALLOR_PAT, extract_disc_pallor, DISC_ATROPHY_PAT
from eye_extractor.headers import Headers
from eye_extractor.output.glaucoma import build_disc_pallor


@pytest.mark.parametrize('pat, text, exp', [
    (DISC_PALLOR_PAT, 'disc pallor', True),
    (DISC_PALLOR_PAT, 'mild pallor', True),
    (DISC_ATROPHY_PAT, 'optic disc atrophy', True),
])
def test_pallor_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) == exp


@pytest.mark.parametrize('text, headers, exp_disc_pallor_re, exp_disc_pallor_le, exp_disc_pallor_unk', [
    ('', {'OPTIC NERVE': 'no disc pallor'}, -1, -1, 0),
    ('', {'OPTIC NERVE': 'pallor OU'}, 1, 1, -1),
    ('optic disc atrophy os', {}, -1, 1, -1),
])
def test_pallor_extract_and_build(text, headers, exp_disc_pallor_re, exp_disc_pallor_le, exp_disc_pallor_unk):
    pre_json = extract_disc_pallor(text, headers=Headers(headers), lateralities=None)
    post_json = json.loads(json.dumps(pre_json))
    result = build_disc_pallor(post_json)
    assert result['disc_pallor_glaucoma_re'] == exp_disc_pallor_re
    assert result['disc_pallor_glaucoma_le'] == exp_disc_pallor_le
    assert result['disc_pallor_glaucoma_unk'] == exp_disc_pallor_unk
