import pytest

from eye_extractor.exam.gonio import OPEN_PAT, CLOSED_PAT


@pytest.mark.parametrize('pat, text, exp', [
    (OPEN_PAT, 'gonio: open', True),
    (OPEN_PAT, 'gonio: opened', True),
    (CLOSED_PAT, 'gonio: closed', True),
])
def test_gonio_patterns(pat, text, exp):
    res = pat.search(text)
    assert bool(res) == exp
