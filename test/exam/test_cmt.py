import pytest

from eye_extractor.exam.cmt import CMT_PAT


@pytest.mark.parametrize('pat, text, exp', [
    (CMT_PAT, 'CMT OD:300 sub-foveal drusen; OS 300 sub-foveal drusen', True),
])
def test_cmt_patterns(pat, text, exp):
    assert bool(pat.search(text)) == exp
