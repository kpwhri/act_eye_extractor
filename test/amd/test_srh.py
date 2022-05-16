import pytest

from eye_extractor.amd.srh import SRH_PAT, get_subretinal_hemorrhage, SRH_IN_MACULA_PAT


@pytest.mark.parametrize('text, exp', [
    ('subretinal hemorrhage', 1),
    ('srh', 1),
    ('srhfe', 1),
    ('srheme', 1),
    ('dysrhythmia', 0),
    ('(intraretinal?) hg', 0),
])
def test_srh_pattern(text, exp):
    assert bool(SRH_PAT.search(text)) == exp


@pytest.mark.parametrize('text, exp', [
    ('no hemorrhage', 1),
    ('hem', 1),
    ('no heme', 1),
])
def test_srh_in_macula_pattern(text, exp):
    assert bool(SRH_IN_MACULA_PAT.search(text)) == exp


@pytest.mark.parametrize('text, exp_value, exp_negword', [
    ('subretinal hemorrhage', 1, None),
    ('no subretinal hemorrhage', 0, 'no'),
    ('no srh', 0, 'no'),
    ('no srf or srh', 0, 'or'),
])
def test_srh_value_first_variable(text, exp_value, exp_negword):
    data = get_subretinal_hemorrhage(text)
    assert len(data) > 0
    first_variable = list(data[0].values())[0]
    assert first_variable['value'] == exp_value
    assert first_variable['negated'] == exp_negword
