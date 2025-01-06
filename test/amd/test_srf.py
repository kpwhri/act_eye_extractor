from datetime import date

import pytest

from eye_extractor.common.algo.fluid import extract_fluid
from eye_extractor.common.json import dumps_and_loads_json
from eye_extractor.headers import Headers
from eye_extractor.output.amd import build_subretfluid_amd


@pytest.mark.parametrize('text, headers, srf_re, srf_le, srf_unk, note_date', [
    ('resolved SRF OD', None, 0, -1, -1, None),
    ('OCT resolved SRF OD', None, 0, -1, -1, date(2022, 2, 20)),
    ('OCT: no recurrent fluid  OD; chronic subretinal fluid OS, stable', None, 0, 1, -1, None),
    ('OCT Disrupted rpe OD; PEDs with subretinal fluid and subretinal hyperreflective material OS',
     None, -1, 1, -1, None),
    ('OCT: ERM os, minimal; new subretinal fluid nasal macula, resolved ; subfoveal rpe atrophy os',
     None, -1, 0, -1, None),
    ('History of Present Illness (HPI): ¶blurry OU.  OU are blurry. he noted improvement in '
     'subretinal fluid and corneal edema.', None, -1, -1, -1, None),  # synthetic, text shortened
    ('Macula Drusen with mild pigment clumping Subtle subretinal fluid nasally without heme.', None, -1, -1, 1, None),
    ('Macula - fresh hemorrhage inferiorly, drusen, mild inferior fluid OD. Quiet, few drusen, no new SRH/SRF OS.',
     None, -1, 0, -1, None),
    ('OD: SRF improved, edema improved, PED stable', None, 1, -1, -1, None),
    # '?trace' with '?' cannot be affirmatively captured due to uncertainty.
    ('OCT: ?trace subretinal fluid OD; good resolution of subretinal fluid OS', None, -1, 1, -1, None),
    # 'recurrent SRF' has no specified laterality.
    ('¶ASSESSMENT:   ¶ ¶Exudative SRNVM OD recurrent SRF,  PEDs OU, ¶', None, -1, -1, 1, None),
    ('¶Eye History - Surgery/Lasers/Injections ¶Exudative SRNVM OD recurrent SRF, PEDs OU, ¶', None, -1, -1, -1, None),
    # 'no edema' means no fluid is present.
    ('Macula: flat RPE change, drusen, no hemorrhage no edema', None, -1, -1, 0, None),
    ('¶ASSESSMENT:  ¶(362.51) ARMD (primary encounter diagnosis) ¶(362.52) Exudative age related macular degeneration'
     ' small fluid OD', None, -1, -1, -1, None),
    # Following tests require date parsing to determine if mention is historical.
    ('Oct macula (Dr. Bowers) : 3/7/2019 CMT OD:504 subfoveal SRF OS:348 small SRF in temporal macula',
     None, -1, -1, -1, date(2019, 6, 4)),  # synthetic
    ('Oct macula: 6/4/2019 CMT OD:343 decreasing subfoveal material, no fluid OS:358 subfoveal RPED, '
     'unchanged', None, 0, -1, -1, date(2019, 6, 4)),  # synthetic
    ('Oct macula: 6/14/2019 CMT OD:330 subfoveal RPED OS:369 subfoveal RPED, dry',
     None, -1, 0, -1, date(2019, 6, 14)),  # synthetic
    ('Oct macula: 9/26/2020 CMT OD:349 trace SRF OS:364 dry', None, 1, 0, -1, date(2020, 9, 26)),  # synthetic
    ('Oct macula: 12/9/2021 CMT OD:352 subfoveal thin SRF OS:277 dry', None, 1, 0, -1, date(2021, 12, 9)),  # synthetic
    ('8/23/2022 Avastin #8 (wk 12) ¶OD: 251 , drusen, no fluid ¶OS: 258 , drusen, no fluid ¶',
     None, 0, 0, -1, date(2022, 8, 23)),  # synthetic
    ('¶Oct macula: 9/8/2017    ¶OD: RPE level changes, PEDS ¶OS: RPE level changes, PEDS, subretinal fluid ¶',
     None, -1, 1, -1, date(2017, 9, 8)),  # synthetic
    ('¶Oct macula: 1/28/2016  ¶OD: trace subretinal fluid,  ¶OS: RPE atrophy ¶',
     None, -1, -1, -1, date(2016, 4, 19)),  # synthetic
])
def test_srf_extract_build(text, headers, srf_re, srf_le, srf_unk, note_date):
    pre_json = extract_fluid(text, headers=Headers(headers))
    post_json = dumps_and_loads_json(pre_json)
    result = build_subretfluid_amd(post_json, note_date=note_date)
    assert result['amd_subretfluid_re'] == srf_re
    assert result['amd_subretfluid_le'] == srf_le
    assert result['amd_subretfluid_unk'] == srf_unk
