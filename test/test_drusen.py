import pytest

from eye_extractor.amd.drusen import find_drusen
from eye_extractor.laterality import build_laterality_table


@pytest.mark.parametrize('text, exp_size, exp_type', [
    ('WNL OU', None, None),
])
def test_drusen(text, exp_size, exp_type):
    lats = build_laterality_table(text)
    data = find_drusen(text, lats)
    drusen_size = data.get('drusen_size', None)
    drusen_type = data.get('drusen_type', None)
    assert drusen_size == exp_size
    assert drusen_type == exp_type
