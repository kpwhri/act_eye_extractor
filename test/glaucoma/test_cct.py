import pytest


@pytest.mark.parametrize('pat, text, exp', [
    (None, 'thick cct', True),
    (None, 'Pachymetry: 565/565', True),
    (None, 'Pachymetry: 494 OD; 488 OS', True),
])
def test_cct_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) == exp
