import pytest

from eye_extractor.glaucoma.disc_hemorrhage import DH_PAT


@pytest.mark.parametrize('pat, text, exp', [
    (DH_PAT, 'no dh', True),
])
def test_dh_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) == exp
