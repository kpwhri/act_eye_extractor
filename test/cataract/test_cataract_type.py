import pytest

from eye_extractor.cataract.cataract_type import NS_PAT, CS_PAT, PSC_PAT, ACS_PAT, get_cataract_type, CataractType


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
def test_fluid_value_first_variable(text, exp_value, exp_negword):
    data = get_cataract_type(text)
    assert len(data) > 0
    first_variable = list(data[0].values())[0]
    assert first_variable['value'] == exp_value
    assert first_variable['negated'] == exp_negword
