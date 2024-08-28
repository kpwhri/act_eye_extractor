import pytest

from eye_extractor.laterality import Laterality, build_laterality_table, LATERALITY_PATTERN


@pytest.mark.parametrize('text, match_span, exp', [
    ('IOL OD: 1+ PCO IOL OS: tr pco', (9, 18), Laterality.OD),
    ('IOL OD: 1+ PCO IOL OS: tr pco', (23, 29), Laterality.OS),
    ('PCIOL od, ac iol os', (0, 6), Laterality.OD),
    ('PCIOL od, ac iol os', (10, 16), Laterality.OS),
    ('dot blot hemorrhage temporal and inferior quadrant OD', (0, 19), Laterality.OD),
    ('intermediate drusen od, heavy drusen os', (0, 22), Laterality.OD),
    ('intermediate drusen od, heavy drusen os', (24, 36), Laterality.OS),
    ('OD: intermediate drusen OS: heavy drusen', (4, 23), Laterality.OD),
    ('OD: intermediate drusen OS: heavy drusen', (28, 40), Laterality.OS),
    ('AMD od > os', (0, 3), Laterality.OU),
    ('AMD od>os', (0, 3), Laterality.OU),
    ('AMD od  >  os', (0, 3), Laterality.OU),
    ('Gonioscopy: right eye: no NVA left eye: no NVA', (26, 29), Laterality.OD),
    ('Gonioscopy: right eye: no NVA left eye: no NVA', (43, 46), Laterality.OS),
    ('CMT OD:200 OS:200', (8, 10), Laterality.OD),
    ('CMT OD:200 possible epiretinal membrane OS:200 possible epiretinal membrane', (27, 40), Laterality.OD),
    ('CMT OD:200 OS:200', (11, 17), Laterality.OS),
    ('CMT OD:200 possible epiretinal membrane OS:200 possible epiretinal membrane', (40, 46), Laterality.OS),
])
def test_laterality_by_index(text, match_span, exp):
    latloc = build_laterality_table(text)
    res = latloc.get_by_index(match_span, text)
    assert res == exp


@pytest.mark.parametrize('pat, text, exp_count', [
    (LATERALITY_PATTERN, 'IOL OD: 1+ PCO IOL OS: tr pco', 2),
    (LATERALITY_PATTERN, 'PCIOL od, ac iol os', 2),
])
def test_laterality_patterns(pat, text, exp_count):
    assert len(pat.findall(text)) == exp_count
