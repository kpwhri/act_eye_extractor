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


@pytest.mark.parametrize('text, headers, exp_value, exp_negword', [
    ('subretinal hemorrhage', {}, 1, None),
    ('no subretinal hemorrhage', {}, 0, 'no'),
    ('no srh', {}, 0, 'no'),
    # Negation `word_window` > 2 captures 'no' as negword, otherwise 'or'.
    ('no srf or srh', {}, 0, 'no'),
])
def test_srh_value_first_variable(text, headers, exp_value, exp_negword):
    data = extract_subretinal_hemorrhage(text, headers=Headers(headers))
    assert len(data) > 0
    first_variable = list(data[0].values())[0]
    assert first_variable['value'] == exp_value
    assert first_variable['negated'] == exp_negword


@pytest.mark.parametrize('text, headers, subretinal_hem_re, subretinal_hem_le, subretinal_hem_unk, note_date', [
    ('subretinal hemorrhage', {}, -1, -1, 1, None),
    ('macular sr heme', {}, -1, -1, 1, None),
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
    ('MACULA: Mild rpe changes OS. Thin subretinal heme centrally with SRF OD.', {}, 1, -1, -1, None),
    ('', {'MACULA': 'Mild rpe changes OS. Thin subretinal heme centrally with SRF OD.'}, 1, -1, -1, None),
    ('OU ¶ ¶ASSESSMENT COMMENTS: Central subretinal heme', {}, -1, -1, 1, None),
    # TODO: Determine if we should extract from 'ASSESSMENT COMMENTS' section.
    # ('', {'ASSESSMENT COMMENTS': 'Central subretinal heme'}, -1, -1, 1, None),
    ('decreased VA OD for 4 weeks sub retinal Hem', {}, 1, -1, -1, None),  # synthetic
    ("PERIPHERAL RETINA: pigmentation at 12 o'clock OD, large domed subretinal hemorrhage", {}, -1, -1, -1, None),
    ('Periphery - attached with peripheral scarring scarring, temporally subretinal hemorrhage/fibrosis',
     {}, -1, -1, -1, None),
    ('Macula -  ¶OD:  No SRH; temporal scarring ¶OS:', {}, 0, -1, -1, None),
    # Laterality sub-section preventing periphery exclusion.
    # ('Periphery -  ¶OD:  attached with peripheral scarring, temporal and superior subretinal hemorrhage/fibrosis',
    #  {}, -1, -1, -1, None),
    ('SF6 OD 10/23/77 ¶            -patient also with subretinal hemorrhaging', {}, -1, -1, 1, None),  # synthetic
    # Laterality sub-section preventing periphery exclusion.
    # ('¶Peripheral fundus:  ¶»OD: fake, text ¶»OS: new N cystic lesion with adjacent ?subretinal hemorrhage',
    #  {}, -1, -1, -1, None),  # text shortened
    ("¶Peripheral fundus: blah blah OD, large patches of sub retinal hemes temporally (from 11-6 o'clock) OD, "
     "WNL OS, (-)NVE OU", {}, -1, -1, -1, None),  # text shortened
    ('Periphery: temporally and inferiorly, subretinal hemorrhage', {}, -1, -1, -1, None),
    ('PLAN: ¶SR heme', {}, -1, -1, 1, None),
    # TODO: Determine if we should extract from 'PLAN' section.
    # ('', {'PLAN': '¶SR heme'}, -1, -1, 1, None),
    ('Follow up for: SR heme', {}, -1, -1, 1, None),
    ('PLAN:  ¶Subretinal Hemorrhagic mass', {}, -1, -1, 1, None),
    # TODO: Determine if we should extract from 'PLAN' section.
    # ('', {'PLAN':  '¶Subretinal Hemorrhagic mass'}, -1, -1, 1, None),
    ('Periphery: choroidal elevation with surrounding sub retinal hemorrhage', {}, -1, -1, -1, None),
    # Inverted laterality sectioning - tricky to capture.
    # ('¶OS: ¶Vitreous: clear  ¶Optic Nerve: crisp  ¶C:D ratio: 0.3 ¶Macula: ped temporal srh', {}, -1, 1, -1, None),
    ('Oct macula: 3/10/2017  ¶OD: CMT 248 , new subretinal hemorrhage and drusen  ¶OS: CMT 231 , drusen, no new SRH',
     {}, 1, -1, -1, datetime.date(2017, 3, 10)),  # synthetic
    ('Macula - fresh hemorrhage inferiorly, drusen, mild inferior fluid OD. Quiet, few drusen, no new SRH/SRF OS.',
     {}, -1, -1, -1, None),
    ('OCT: Disrupted RPE OD>OS with new PED and subretinal heme and fluid OD ¶', {}, 1, -1, -1, None),
    ('Macula - flat OU. Small PED OS nasal to fovea.  No notable drusen/SRF/SRH OU.', {}, 0, 0, -1, None),
    # Text shortened before 'drusen OD;'.
    ('MACULA: drusen OD; large 8-10 dd subretinal hemorrhage encompassing previously identified RPE detachment OS  ¶',
     {}, -1, 1, -1, None),
    ('(H35.62) Subretinal hemorrhage of left eye-', {}, -1, 1, -1, None),
    ('4/2/2019  Subretinal hemorrhage left eye', {}, -1, 1, -1, datetime.date(2019, 4, 2)),  # synthetic
    ('Macula:subretinal hemorrhage temporal to optic nerve with trc elevation OD, single pigmented area fovea OS ¶',
     {}, 1, -1, -1, None),
    ('ASSESSMENT: ¶1.»(H35.61) Subretinal hemorrhage of right eye', {}, 1, -1, -1, None),
    ('SUBJECTIVE:  The patient is here for follow up evaluation of peripapillary subretinal hemorrhage OD.',
     {}, -1, -1, -1, None),
    # TODO: Determine if we should extract from 'SUBJECTIVE' section.
    # ('', {'SUBJECTIVE': 'The patient is here for follow up evaluation of peripapillary subretinal hemorrhage OD'},
    #  -1, -1, -1, None),
    # Inverted laterality sectioning - tricky to capture.
    # ('¶OD: ¶Vitreous: clear  ¶Optic Nerve: crisp tr pale ¶C:D ratio: 0.5 ¶Macula: SRH,', {}, 1, -1, -1, None),
])
def test_srh_extract_build(text, headers, subretinal_hem_re, subretinal_hem_le, subretinal_hem_unk, note_date):
    pre_json = extract_subretinal_hemorrhage(text, headers=Headers(headers))
    post_json = dumps_and_loads_json(pre_json)
    result = build_subretinal_hemorrhage(post_json, note_date=note_date)
    assert result['subretinal_hem_re'] == subretinal_hem_re
    assert result['subretinal_hem_le'] == subretinal_hem_le
    assert result['subretinal_hem_unk'] == subretinal_hem_unk
