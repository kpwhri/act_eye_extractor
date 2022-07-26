import pytest

from eye_extractor.amd.ped import PED_PAT


@pytest.mark.parametrize('pat, text, exp', [
    (PED_PAT, 'pigment epithelial detachment', True),
    (PED_PAT, 'detachment of the retinal pigment epithelium', True),
    (PED_PAT, 'ped', True),
    (PED_PAT, 'PEDs', True),
])
def test_ped_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) is exp
