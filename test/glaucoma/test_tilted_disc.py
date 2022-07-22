import json

import pytest

from eye_extractor.glaucoma.tilted_disc import TILTED_PAT, extract_tilted_disc
from eye_extractor.output.glaucoma import build_disc_notch


@pytest.mark.parametrize('pat, text, exp', [
    (TILTED_PAT, 'myopia tilted', True),
    (TILTED_PAT, 'tilted myopic disc', True),
    (TILTED_PAT, 'discs tilted', True),
])
def test_tilted_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) == exp


@pytest.mark.parametrize('text, headers, exp_tilted_disc_re, exp_tilted_disc_le, exp_tilted_disc_unk', [
])
def test_tilted_extract_and_build(text, headers, exp_tilted_disc_re, exp_tilted_disc_le, exp_tilted_disc_unk):
    pre_json = extract_tilted_disc(text, headers=headers, lateralities=None)
    post_json = json.loads(json.dumps(pre_json))
    result = build_disc_notch(post_json)
    assert result['tilted_disc_re'] == exp_tilted_disc_re
    assert result['tilted_disc_le'] == exp_tilted_disc_le
    assert result['tilted_disc_unk'] == exp_tilted_disc_unk