import datetime

import pytest

from eye_extractor.amd.srh import SRH_PAT, extract_subretinal_hemorrhage
from eye_extractor.common.json import dumps_and_loads_json
from eye_extractor.headers import Headers
from eye_extractor.output.amd import build_subretinal_hemorrhage


@pytest.mark.parametrize('text, exp', [
    ('subretinal hemorrhage', 1),
    ('srh', 1),
    ('srhfe', 1),
    ('srheme', 1),
    ('dysrhythmia', 0),
    ('(intraretinal?) hg', 0),
    ('subretinal hg', 1),
])
def test_srh_pattern(text, exp):
    assert bool(SRH_PAT.search(text)) == exp


@pytest.mark.parametrize('text, exp_value, exp_negword', [
    ('subretinal hemorrhage', 1, None),
    ('no subretinal hemorrhage', 0, 'no'),
    ('no srh', 0, 'no'),
    ('no srf or srh', 0, 'or'),
])
def test_srh_value_first_variable(text, exp_value, exp_negword):
    data = extract_subretinal_hemorrhage(text)
    assert len(data) > 0
    first_variable = list(data[0].values())[0]
    assert first_variable['value'] == exp_value
    assert first_variable['negated'] == exp_negword


@pytest.mark.parametrize('text, headers, subretinal_hem_re, subretinal_hem_le, subretinal_hem_unk, note_date', [
    ('subretinal hemorrhage', {}, -1, -1, 1, None),
    ('no subretinal hemorrhage', {}, -1, -1, 0, None),
    ('no srh', {}, -1, -1, 0, None),
    ('no sr hem', {}, -1, -1, 0, None),
    ('sr hem od, no srh os', {}, 1, 0, -1, None),
    ('sub and intraretinal heme os', {}, -1, 1, -1, None),
    ('no srf or srh', {}, -1, -1, 0, None),
    ('no srf od, srh os', {}, -1, 1, -1, None),
    ('', {'MACULA': 'w/o srh ou'}, 0, 0, -1, None),
    ('OCT MACULA: 2/2/2022 OS: srh', {'MACULA': 'w/o srh os'}, -1, 1, -1, None),
    ('OCT MACULA: 2/2/2022 OS: srh', {'MACULA': 'w/o srh os'}, -1, 1, -1, None),
    ('OCT MACULA: 2/2/2022 OS: srh', {'MACULA': 'w/o srh os'}, -1, 0, -1, datetime.date(2022, 2, 9)),
    ('OCT MACULA: 2/2/2022 OS: srh', {'MACULA': 'w/o srh ou'}, 0, 0, -1, datetime.date(2022, 2, 9)),
    ('OCT MACULA: 2/2/2022 OS: srh', {'MACULA': 'w/o srh ou'}, 0, 1, -1, datetime.date(2022, 2, 1)),

])
def test_srh_extract_build(text, headers, subretinal_hem_re, subretinal_hem_le, subretinal_hem_unk, note_date):
    pre_json = extract_subretinal_hemorrhage(text, headers=Headers(headers))
    post_json = dumps_and_loads_json(pre_json)
    result = build_subretinal_hemorrhage(post_json, note_date=note_date)
    assert result['subretinal_hem_re'] == subretinal_hem_re
    assert result['subretinal_hem_le'] == subretinal_hem_le
    assert result['subretinal_hem_unk'] == subretinal_hem_unk
