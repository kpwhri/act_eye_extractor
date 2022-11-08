import json

import pytest

from eye_extractor.glaucoma.disc_hemorrhage import DH_PAT, extract_disc_hem
from eye_extractor.output.glaucoma import build_disc_hem


@pytest.mark.parametrize('pat, text, exp', [
    (DH_PAT, 'no dh', True),
    (DH_PAT, 'no disc hemorrhages', True),
    (DH_PAT, 'disc heme', True),
])
def test_dh_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) == exp


@pytest.mark.parametrize('text, headers, exp_disc_hem_re, exp_disc_hem_le, exp_disc_hem_unk', [
    ('no dh', None, -1, -1, 0),
    ('dh', None, -1, -1, 1),
    ('OD: dh', None, 1, -1, -1),
    ('Optic disc hemorrhage', None, -1, -1, 1),
    ('h/o disc hemorrhage', None, -1, -1, 0),
])
def test_dh_extract_and_build(text, headers, exp_disc_hem_re, exp_disc_hem_le, exp_disc_hem_unk):
    pre_json = extract_disc_hem(text, headers=headers, lateralities=None)
    post_json = json.loads(json.dumps(pre_json))
    result = build_disc_hem(post_json)
    assert result['disc_hem_re'] == exp_disc_hem_re
    assert result['disc_hem_le'] == exp_disc_hem_le
    assert result['disc_hem_unk'] == exp_disc_hem_unk
