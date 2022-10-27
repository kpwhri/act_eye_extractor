import datetime
import json

import pytest

from eye_extractor.common.algo.fluid import FLUID_NOS_PAT, SUBRETINAL_FLUID_PAT, INTRARETINAL_FLUID_PAT, extract_fluid, \
    SUB_AND_INTRARETINAL_FLUID_PAT, MACULAR_EDEMA_PAT
from eye_extractor.common.json import dumps_and_loads_json
from eye_extractor.headers import Headers
from eye_extractor.output.amd import build_fluid_amd


@pytest.mark.parametrize('text, exp', [
    ('with fluid and exudates', 1),
    ('subretinal fluid', 1),
    ('intraretinal fluid', 1),
])
def test_fluid_nos_pattern(text, exp):
    assert bool(FLUID_NOS_PAT.search(text)) == exp


@pytest.mark.parametrize('text, exp', [
    ('macular edema', 1),
    ('csme', 1),
    ('SCME', 1),
])
def test_fluid_macular_edema(text, exp):
    assert bool(MACULAR_EDEMA_PAT.search(text)) == exp


@pytest.mark.parametrize('text, exp', [
    ('with fluid and exudates', 0),
    ('subretinal fluid', 1),
    ('intraretinal fluid', 0),
    ('srf', 1),
    ('sr fluid', 1),
    ('srfluids', 1),
    ('bowsr fanta', 0),
    ('sub ret fluid', 1),
])
def test_subretinal_fluid_pattern(text, exp):
    assert bool(SUBRETINAL_FLUID_PAT.search(text)) == exp


@pytest.mark.parametrize('text, exp', [
    ('with fluid and exudates', 0),
    ('subretinal fluid', 0),
    ('intraretinal fluid', 1),
    ('airflow', 0),
    ('irf', 1),
    ('ir fluid', 1),
    ('irfluids', 1),
    ('bowir fanta', 0),
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
    ('sr fluid and irfluids', 1),
])
def test_intraretinal_fluid_pattern(text, exp):
    assert bool(SUB_AND_INTRARETINAL_FLUID_PAT.search(text)) == exp


@pytest.mark.parametrize('text, exp_value, exp_negword', [
    ('no new heme and fluid od', 0, 'no'),
    ('new subretinal fluid in central macula', 1, None),
    ('fluid not noted today', 0, 'not'),
    ('no irf', 20, 'no'),
    ('srf not noted', 10, 'not'),
])
def test_fluid_value_first_variable(text, exp_value, exp_negword):
    data = extract_fluid(text)
    assert len(data) > 0
    first_variable = list(data[0].values())[0]
    assert first_variable['value'] == exp_value
    assert first_variable['negated'] == exp_negword


@pytest.mark.parametrize('data, exp_fluid_amd_re, exp_fluid_amd_le', [
    ([], 'UNKNOWN', 'UNKNOWN'),
])
def test_fluid_to_column(data, exp_fluid_amd_re, exp_fluid_amd_le):
    result = build_fluid_amd(data, skip_rename_variable=True)
    assert result['fluid_amd_re'] == exp_fluid_amd_re
    assert result['fluid_amd_le'] == exp_fluid_amd_le


@pytest.mark.parametrize('text, headers, exp_fluid_re, exp_fluid_le, exp_fluid_unk, note_date', [
    ('', {'MACULA': 'subretinal fluid od'}, 'SUBRETINAL FLUID', 'UNKNOWN', 'UNKNOWN', None),
    ('', {'MACULA': 'with fluid and exudates'}, 'UNKNOWN', 'UNKNOWN', 'FLUID', None),
    ('', {'MACULA': 'large area of edema OD'}, 'INTRARETINAL FLUID', 'UNKNOWN', 'UNKNOWN', None),
    ('corneal fluid', {}, 'UNKNOWN', 'UNKNOWN', 'UNKNOWN', None),
    ('corneal edema', {}, 'UNKNOWN', 'UNKNOWN', 'UNKNOWN', None),
    ('macular edema os', {}, 'UNKNOWN', 'INTRARETINAL FLUID', 'UNKNOWN', None),
    ('(-) edema OD', {}, 'NO INTRARETINAL FLUID', 'UNKNOWN', 'UNKNOWN', None),
    ('(-) mac edema OD', {}, 'NO INTRARETINAL FLUID', 'UNKNOWN', 'UNKNOWN', None),
    ('-CSME OS', {}, 'UNKNOWN', 'NO INTRARETINAL FLUID', 'UNKNOWN', None),
    ('CSME OS', {}, 'UNKNOWN', 'INTRARETINAL FLUID', 'UNKNOWN', None),
    ('OCT MACULA: 2/2/2022 OD: 132, mild edema ', {}, 'INTRARETINAL FLUID', 'UNKNOWN', 'UNKNOWN', None),
    ('OCT MACULA: 2/2/2022 OD: 132, mild edema ', {'MACULA': 'no edema od'},
     'INTRARETINAL FLUID', 'UNKNOWN', 'UNKNOWN', datetime.date(2022, 2, 2)),
])
def test_fluid_extract_build(text, headers, exp_fluid_re, exp_fluid_le, exp_fluid_unk, note_date):
    pre_json = extract_fluid(text, headers=Headers(headers))
    post_json = dumps_and_loads_json(pre_json)
    result = build_fluid_amd(post_json, skip_rename_variable=True, note_date=note_date)
    assert result['fluid_amd_re'] == exp_fluid_re
    assert result['fluid_amd_le'] == exp_fluid_le
    assert result['fluid_amd_unk'] == exp_fluid_unk
