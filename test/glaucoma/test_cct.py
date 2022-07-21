import pytest

from eye_extractor.glaucoma.cct import CCT_OD_OS_PAT, CCT_OD_PAT, CCT_OS_PAT, CCT_OU_PAT


@pytest.mark.parametrize('pat, text, exp', [
    pytest.param(CCT_OD_OS_PAT, 'thick cct', True, marks=pytest.mark.skip()),
    (CCT_OD_OS_PAT, 'Pachymetry: 565/565', True),
    (CCT_OD_OS_PAT, 'Pachymetry: 494 OD; 488 OS', True),
    (CCT_OS_PAT, 'Pachymetry: 488 OS', True),
    (CCT_OD_PAT, 'Pachymetry: 494 OD', True),
    (CCT_OD_PAT, 'Pachymetry: OD: 494', True),
    (CCT_OS_PAT, 'Pachymetry: OS: 494', True),
    (CCT_OU_PAT, 'Pachymetry: OU: 494', True),
    (CCT_OD_OS_PAT, 'Pachymetry: OD: 494 OS: 495', True),
])
def test_cct_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) == exp
