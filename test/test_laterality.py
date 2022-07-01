import pytest

from eye_extractor.laterality import Laterality, get_laterality_by_index, build_laterality_table


@pytest.mark.parametrize('text, start_index, exp', [
    ('IOL OD: 1+ PCO IOL OS: tr pco', 9, Laterality.OD),
    ('IOL OD: 1+ PCO IOL OS: tr pco', 23, Laterality.OS)
])
def test_laterality_by_index(text, start_index, exp):
    lateralities = build_laterality_table(text)
    res = get_laterality_by_index(lateralities, start_index, text)
    assert res == exp
