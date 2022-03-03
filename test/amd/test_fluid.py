import pytest

from eye_extractor.amd.fluid import FLUID_NOS_PAT, SUBRETINAL_FLUID_PAT, INTRARETINAL_FLUID_PAT, get_fluid, \
    SUB_AND_INTRARETINAL_FLUID_PAT, FluidAMD
from eye_extractor.output.amd import get_fluid_from_variable


@pytest.mark.parametrize('text, exp', [
    ('with fluid and exudates', 1),
    ('subretinal fluid', 1),
    ('intraretinal fluid', 1),
])
def test_fluid_nos_pattern(text, exp):
    assert bool(FLUID_NOS_PAT.search(text)) == exp


@pytest.mark.parametrize('text, exp', [
    ('with fluid and exudates', 0),
    ('subretinal fluid', 1),
    ('intraretinal fluid', 0),
])
def test_subretinal_fluid_pattern(text, exp):
    assert bool(SUBRETINAL_FLUID_PAT.search(text)) == exp


@pytest.mark.parametrize('text, exp', [
    ('with fluid and exudates', 0),
    ('subretinal fluid', 0),
    ('intraretinal fluid', 1),
    ('airflow', 0),
    ('irf', 1),
])
def test_intraretinal_fluid_pattern(text, exp):
    assert bool(INTRARETINAL_FLUID_PAT.search(text)) == exp


@pytest.mark.parametrize('text, exp', [
    ('with fluid and exudates', 0),
    ('subretinal fluid', 0),
    ('intraretinal fluid', 0),
    ('subretinal and intraretinal fluid', 1),
    ('subretinal fluid and intraretinal fluid', 1),
    ('sub and intraretinal fluid', 1),
    ('srf/irf', 1),
    ('srf and irf', 1),
])
def test_intraretinal_fluid_pattern(text, exp):
    assert bool(SUB_AND_INTRARETINAL_FLUID_PAT.search(text)) == exp


@pytest.mark.parametrize('text, exp_value, exp_negword', [
    ('no new heme and fluid od', 0, 'no'),
    ('new subretinal fluid in central macula', 99, None),
    ('fluid not noted today', 0, 'not'),
    ('no irf', 20, 'no'),
    ('srf not noted', 10, 'not'),
])
def test_fluid_value_first_variable(text, exp_value, exp_negword):
    data = get_fluid(text)
    assert len(data) > 0
    first_variable = list(data[0].values())[0]
    assert first_variable['value'] == exp_value
    assert first_variable['negated'] == exp_negword


@pytest.mark.parametrize('data, exp_fluid_amd_re, exp_fluid_amd_le', [
    ([], FluidAMD.NO, FluidAMD.NO),
])
def test_fluid_to_column(data, exp_fluid_amd_re, exp_fluid_amd_le):
    result = get_fluid_from_variable(data)
    assert result['fluid_amd_re'] == exp_fluid_amd_re
    assert result['fluid_amd_le'] == exp_fluid_amd_le
