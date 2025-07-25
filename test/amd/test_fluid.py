import datetime

import pytest

from eye_extractor.common.algo.fluid import FLUID_NOS_PAT, SUBRETINAL_FLUID_PAT, INTRARETINAL_FLUID_PAT, extract_fluid, \
    SUB_AND_INTRARETINAL_FLUID_PAT, MACULAR_EDEMA_PAT, Fluid
from eye_extractor.common.json import dumps_and_loads_json
from eye_extractor.common.noteinfo import extract_note_level_info
from eye_extractor.sections.document import create_doc_and_sections
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
    ('no new heme and fluid od', 21, None),
    ('new subretinal fluid in central macula', 11, None),
    ('fluid not noted today', 20, 'not'),
    ('no irf', 20, 'no'),
    ('srf not noted', 10, 'not'),
])
def test_fluid_value_first_variable(text, exp_value, exp_negword):
    doc = create_doc_and_sections(text)
    data = extract_fluid(doc)
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


@pytest.mark.parametrize('text, sections, exp_fluid_re, exp_fluid_le, exp_fluid_unk, note_date', [
    ('', {'MACULA': 'subretinal fluid od'}, 'SUBRETINAL FLUID', 'UNKNOWN', 'UNKNOWN', None),
    ('', {'MACULA': 'with fluid and exudates'}, 'UNKNOWN', 'UNKNOWN', 'INTRARETINAL FLUID', None),
    ('', {'MACULA': 'large area of edema OD'}, 'INTRARETINAL FLUID', 'UNKNOWN', 'UNKNOWN', None),
    ('', {'MACULA': 'no srf od'}, 'NO SUBRETINAL FLUID', 'UNKNOWN', 'UNKNOWN', None),
    ('corneal fluid', {}, 'UNKNOWN', 'UNKNOWN', 'UNKNOWN', None),
    ('', {'MACULA': 'recurrence of macular fluid od'}, 'INTRARETINAL FLUID', 'UNKNOWN', 'UNKNOWN', None),
    ('corneal edema', {}, 'UNKNOWN', 'UNKNOWN', 'UNKNOWN', None),
    ('macular edema os', {}, 'UNKNOWN', 'INTRARETINAL FLUID', 'UNKNOWN', None),
    ('(-) edema OD', {}, 'NO INTRARETINAL FLUID', 'UNKNOWN', 'UNKNOWN', None),
    ('(-) mac edema OD', {}, 'NO INTRARETINAL FLUID', 'UNKNOWN', 'UNKNOWN', None),
    ('-CSME OS', {}, 'UNKNOWN', 'NO INTRARETINAL FLUID', 'UNKNOWN', None),
    ('CSME OS', {}, 'UNKNOWN', 'INTRARETINAL FLUID', 'UNKNOWN', None),
    ('OCT MACULA: 2/2/2022 OD: 132, mild edema ', {}, 'INTRARETINAL FLUID', 'UNKNOWN', 'UNKNOWN', None),
    ('OCT MACULA: 2/2/2022 OD: 132, mild edema ', {'MACULA': 'no edema od'},
     'INTRARETINAL FLUID', 'UNKNOWN', 'UNKNOWN', datetime.date(2022, 2, 2)),
    ('OCT MACULA: 2/9/2022 OD: 132, mild edema ', {'MACULA': 'no edema od'},
     'NO INTRARETINAL FLUID', 'UNKNOWN', 'UNKNOWN', datetime.date(2022, 2, 2)),
    ('OCT: No fluid od, no recurrent fluid os', {}, 'NO INTRARETINAL FLUID', 'NO INTRARETINAL FLUID', 'UNKNOWN', None),
])
def test_fluid_extract_build(text, sections, exp_fluid_re, exp_fluid_le, exp_fluid_unk, note_date):
    doc = create_doc_and_sections(text, sections)
    pre_json = extract_fluid(doc)
    post_json = dumps_and_loads_json(pre_json)
    result = build_fluid_amd(post_json, skip_rename_variable=True, note_date=note_date)
    assert result['fluid_amd_re'] == exp_fluid_re
    assert result['fluid_amd_le'] == exp_fluid_le
    assert result['fluid_amd_unk'] == exp_fluid_unk


def test_fluid_extract_build_no_amd():
    """Test fluid when no AMD"""
    text = 'macular edema os'
    doc = create_doc_and_sections(text)
    fluid_pre_json = extract_fluid(doc)
    amd_pre_json = extract_note_level_info(doc)
    fluid_post_json = dumps_and_loads_json(fluid_pre_json)
    amd_post_json = dumps_and_loads_json(amd_pre_json)
    result = build_fluid_amd(fluid_post_json, is_amd=amd_post_json['is_amd'])
    assert result['fluid_amd_re'] == Fluid.UNKNOWN
    assert result['fluid_amd_le'] == Fluid.UNKNOWN
    assert result['fluid_amd_unk'] == Fluid.UNKNOWN
