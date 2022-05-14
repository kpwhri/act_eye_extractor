import pytest

from eye_extractor.cataract.cataract_type import NS_PAT, CS_PAT, PSC_PAT, ACS_PAT, get_cataract_type, CataractType
from eye_extractor.output.cataract import build_cataract_type


@pytest.mark.parametrize('text', [
    'NS 3-4',
    '2-3 NS',
    'nuclear cataract',
])
def test_ns_cataract_pattern(text):
    assert NS_PAT.match(text)


@pytest.mark.parametrize('text', [
    'ACS 3-4',
    '2-3 ACS',
])
def test_acs_cataract_pattern(text):
    assert ACS_PAT.match(text)


@pytest.mark.parametrize('text', [
    'PSC 1',
    'PSC 1+',
])
def test_psc_cataract_pattern(text):
    assert PSC_PAT.match(text)


@pytest.mark.parametrize('text', [
    'CS 2',
    'cortical cataract',
])
def test_cs_cataract_pattern(text):
    assert CS_PAT.match(text)


@pytest.mark.parametrize('text, exp_value, exp_negword', [
    ('no nuclear cataract', CataractType.NONE, 'no'),
    ('nuclear cataract', CataractType.NS, None),
    ('CS 1+', CataractType.CS, None),
    ('cortical cataract', CataractType.CS, None),
])
def test_cataract_value_first_variable(text, exp_value, exp_negword):
    data = get_cataract_type(text)
    print(data)
    assert len(data) > 0
    first_variable = list(data[0].values())[0]
    assert first_variable['value'] == exp_value
    assert first_variable['negated'] == exp_negword


@pytest.mark.parametrize('data, exp_cataract_type_re, exp_cataract_type_le', [
    ([], CataractType.UNKNOWN, CataractType.UNKNOWN),
    ([{'cataract_type_le': 1}], CataractType.UNKNOWN, CataractType.NONE),
    ([{'cataract_type_le': 2, 'cataract_type_re': 3}], CataractType.CS, CataractType.NS),
])
def test_cataract_to_column(data, exp_cataract_type_re, exp_cataract_type_le):
    result = build_cataract_type(data)
    assert result['cataract_type_le'] == exp_cataract_type_le
    assert result['cataract_type_re'] == exp_cataract_type_re
