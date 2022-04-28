import pytest

from eye_extractor.rao.rao import RAO_PAT


@pytest.mark.parametrize('text', [
    'retinal artery occlusion',
    'rvaso',
    'BRAO',
    'CRAO',
    'central retinal artery occlusion',
])
def test_rao_pattern(text):
    assert RAO_PAT.match(text)
