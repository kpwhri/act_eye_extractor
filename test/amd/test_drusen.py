import pytest

from eye_extractor.amd.drusen import find_drusen
from eye_extractor.laterality import build_laterality_table


@pytest.mark.parametrize('text, exp_size_le, exp_size_re, exp_type_le, exp_type_re', [
    ('WNL OU', None, None, None, None),
    ('drusen and RPE drop out OU', 'yes', 'yes', 'yes', 'yes'),
])
def test_drusen(text, exp_size_le, exp_size_re, exp_type_le, exp_type_re):
    lats = build_laterality_table(text)
    data = find_drusen(text, lats)
    drusen_size_le = data.get('drusen_size_le', dict())
    drusen_size_re = data.get('drusen_size_re', dict())
    drusen_type_le = data.get('drusen_type_le', dict())
    drusen_type_re = data.get('drusen_type_re', dict())
    assert drusen_size_le.get('label', None) == exp_size_le
    assert drusen_size_re.get('label', None) == exp_size_re
    assert drusen_type_le.get('label', None) == exp_type_le
    assert drusen_type_re.get('label', None) == exp_type_re
