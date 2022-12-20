import pytest

from eye_extractor.laterality import Laterality, build_laterality_table, LATERALITY_PATTERN


@pytest.mark.parametrize('text, start_index, exp', [
    ('IOL OD: 1+ PCO IOL OS: tr pco', 9, Laterality.OD),
    ('IOL OD: 1+ PCO IOL OS: tr pco', 23, Laterality.OS),
    ('PCIOL od, ac iol os', 0, Laterality.OD),
    ('PCIOL od, ac iol os', 10, Laterality.OS),
    ('dot blot hemorrhage temporal and inferior quadrant OD', 0, Laterality.OD),
    ('intermediate drusen od, heavy drusen os', 0, Laterality.OD),
    ('intermediate drusen od, heavy drusen os', 30, Laterality.OS),
    ('OD: intermediate drusen OS: heavy drusen', 0, Laterality.OD),
    ('OD: intermediate drusen OS: heavy drusen', 30, Laterality.OS),
    ('AMD od > os', 3, Laterality.OU),
    ('AMD od>os', 3, Laterality.OU),
    ('AMD od  >  os', 3, Laterality.OU),
    ('Gonioscopy: right eye: no NVA left eye: no NVA', 26, Laterality.OD),
    ('Gonioscopy: right eye: no NVA left eye: no NVA', 43, Laterality.OS),
])
def test_laterality_by_index(text, start_index, exp):
    latloc = build_laterality_table(text)
    res = latloc.get_by_index(start_index, text)
    assert res == exp


@pytest.mark.parametrize('pat, text, exp_count', [
    (LATERALITY_PATTERN, 'IOL OD: 1+ PCO IOL OS: tr pco', 2),
    (LATERALITY_PATTERN, 'PCIOL od, ac iol os', 2),
])
def test_laterality_patterns(pat, text, exp_count):
    assert len(pat.findall(text)) == exp_count
