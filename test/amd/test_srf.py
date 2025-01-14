from datetime import date

import pytest

from eye_extractor.common.algo.fluid import extract_fluid
from eye_extractor.common.json import dumps_and_loads_json
from eye_extractor.headers import Headers
from eye_extractor.output.amd import build_subretfluid_amd


@pytest.mark.parametrize('text, headers, srf_re, srf_le, srf_unk, note_date', [
    ('resolved SRF OD', None, 0, -1, -1, None),
    ('OCT resolved SRF OD', None, 0, -1, -1, date(2022, 2, 20)),
    # TODO: To pass below test, change handling of non-specified fluid mention to be for fluid, not IRF.
    # ('OCT: no recurrent fluid  OD; chronic subretinal fluid OS, stable', None, 0, 1, -1, None),
    # TODO: Fix laterality (intervening chars) to pass below case.
    # ('OCT Disrupted rpe OD; PEDs with subretinal fluid and subretinal hyperreflective material OS',
    #  None, -1, 1, -1, None),
    ('OCT: ERM os, minimal; new subretinal fluid nasal macula, resolved ; subfoveal rpe atrophy os',
     None, -1, 0, -1, None),
    # 'History of Present Illness (HPI)' many lines before SRF mention - tricky to capture.
    # TODO: Implement in-line search & ignore for history sections.
    # ('History of Present Illness (HPI): ¶blurry OU.  OU are blurry. he noted improvement in '
    #  'subretinal fluid and corneal edema.', None, -1, -1, -1, None),  # synthetic, text shortened
    ('Macula Drusen with mild pigment clumping Subtle subretinal fluid nasally without heme.', None, -1, -1, 1, None),
    # 'no new' currently not treated as negating phrase, although interpretation of below snippet is negative SRF OS.
    # ('Macula - fresh hemorrhage inferiorly, drusen, mild inferior fluid OD. Quiet, few drusen, no new SRH/SRF OS.',
    #  None, -1, 0, -1, None),
    ('OD: SRF improved, edema improved, PED stable', None, 1, -1, -1, None),
    # '?trace' with '?' cannot be affirmatively captured due to uncertainty.
    # 'resolution' currently captured as negword, although interpretation of below snippet is affirmative SRF OS.
    # ('OCT: ?trace subretinal fluid OD; good resolution of subretinal fluid OS', None, -1, 1, -1, None),
    # 'recurrent SRF' has no specified laterality - tricky to capture.
    # ('¶ASSESSMENT:   ¶ ¶Exudative SRNVM OD recurrent SRF,  PEDs OU, ¶', None, -1, -1, 1, None),
    # TODO: Implement in-line search & ignore for history sections.
    # ('¶Eye History - Surgery/Lasers/Injections ¶Exudative SRNVM OD recurrent SRF, PEDs OU, ¶',
    #  None, -1, -1, -1, None),
    # 'no edema' means no fluid is present.
    # TODO: To pass below test, change handling of non-specified fluid mention to be for fluid, not IRF.
    # ('Macula: flat RPE change, drusen, no hemorrhage no edema', None, -1, -1, 0, None),
    ('¶ASSESSMENT:  ¶(362.51) ARMD (primary encounter diagnosis) ¶(362.52) Exudative age related macular degeneration'
     ' small fluid OD', None, -1, -1, -1, None),
    ('MACULA:  ¶OD: patchy atrophy with flecks of heme and SRF ¶OS: frank edema with flecks of heme',
     None, 1, -1, -1, None),
    ('ASSESSMENT: AMD/SRF/SRN: Worsening acuity both eyes, patient now has '
     'SRF and heme in the RIGHT EYE as well as OS.', None, 1, 1, -1, None),
    ('OCT os with ERM/VMT and SRF.', None, -1, 1, -1, None),
    # Historical mention, should be ignored - tricky to ignore due to format '[doctor last name]'s note'.
    # ("¶OCT-Mac: from Cronkite's note ¶Disrupted RPE OU with trace subretinal fluid OD and "
    #  "marked macular and subretinal fluid OS ¶", None, -1, -1, -1, None),  # synthetic
    ('MACULA: + srf OD-just off axis; OS-drusen, rpe changes OS', None, 1, -1, -1, None),
    # TODO: To pass below test, change handling of non-specified fluid mention to be for fluid, not IRF.
    # ('OCT mac-+SRF CT 498 OD ; OS 328 drusen with no fluid', None, 1, 0, -1, None),  # synthetic
    ('p-m bundle just temporal to the disc. Appears to have some subretinal fluid associated.', None, -1, -1, 1, None),
    ('¶Macula OCT ¶OD: CMT of 240, appears stable to prior/dry '
     '¶OS: CMT of 413, several new areas of sub retinal fluid  ¶ ¶', None, -1, 1, -1, None),
    ('OCT: slight subretinal fluid od, persistent.', None, 1, -1, -1, None),
    # Below snippet contains likely misspelling - 'so' instead of 'os'.
    # ('¶OCT:   Persistent subretinal fluid so ¶', None, -1, 1, -1, None),
    ('OU ¶PERIPHERAL RETINA: Normal appearance/flat ¶ ¶OCT:  Incomplete image OD;  Subretinal fluid OS ¶ ¶',
     None, -1, 1, -1, None),
    # Following tests require date parsing to determine if mention is historical.
    # ('Oct macula (Dr. Bowers) : 3/7/2019 CMT OD:504 subfoveal SRF OS:348 small SRF in temporal macula',
    #  None, -1, -1, -1, date(2019, 6, 4)),  # synthetic
    # TODO: To pass below test, change handling of non-specified fluid mention to be for fluid, not IRF.
    # ('Oct macula: 6/4/2019 CMT OD:343 decreasing subfoveal material, no fluid OS:358 subfoveal RPED, '
    #  'unchanged', None, 0, -1, -1, date(2019, 6, 4)),  # synthetic
    # TODO: Add 'dry' as search term for `Fluid.NO`.
    # ('Oct macula: 6/14/2019 CMT OD:330 subfoveal RPED OS:369 subfoveal RPED, dry',
    #  None, -1, 0, -1, date(2019, 6, 14)),  # synthetic
    # TODO: Add 'dry' as search term for `Fluid.NO`.
    # ('Oct macula: 9/26/2020 CMT OD:349 trace SRF OS:364 dry', None, 1, 0, -1, date(2020, 9, 26)),  # synthetic
    # TODO: Add 'dry' as search term for `Fluid.NO`.
    # ('Oct macula: 12/9/2021 CMT OD:352 subfoveal thin SRF OS:277 dry',
    #  None, 1, 0, -1, date(2021, 12, 9)),  # synthetic
    # TODO: To pass below test, change handling of non-specified fluid mention to be for fluid, not IRF.
    # ('8/23/2022 Avastin #8 (wk 12) ¶OD: 251 , drusen, no fluid ¶OS: 258 , drusen, no fluid ¶',
    #  None, 0, 0, -1, date(2022, 8, 23)),  # synthetic
    ('¶Oct macula: 9/8/2017    ¶OD: RPE level changes, PEDS ¶OS: RPE level changes, PEDS, subretinal fluid ¶',
     None, -1, 1, -1, date(2017, 9, 8)),  # synthetic
    ('¶Oct macula: 1/28/2016  ¶OD: trace subretinal fluid,  ¶OS: RPE atrophy ¶',
     None, -1, -1, -1, date(2016, 4, 19)),  # synthetic
    # # Mention appears in 'Personal Ocular History Includes' section - should be ignored.
    # ('AMD - SRF vs CME noted on exam OS 3/08', None, -1, -1, -1, date(2008, 6, 15)),  # synthetic
    ('¶sOCT 3-4-2018 Macula ¶OD»341»Temporal thinning and irreg ¶OS»307»Erm, VMT with SRF',
     None, -1, 1, -1, date(2018, 3, 4)),  # synthetic
    ('Oct macula: 3/19/2018 CMT OD: 2018, no intraretinal and subretinal fluid OS: 306, disciform scar',
     None, 0, -1, -1, date(2018, 3, 19)),  # synthetic
    ('Oct macula: 7/27/2016 OD: New PED, SRF, CMT 503; OS: WNL, CMT 296 Avastin OD # 1',
     None, 1, -1, -1, date(2016, 7, 27)),  # synthetic
    ('¶Oct macula: 11/20/2018 CMT OD:327 with stable medium size PED and '
     'small amount of subretinal fluid  inferior to fovea', None, 1, -1, -1, date(2018, 11, 20)),  # synthetic
    ('¶11/14/2021  CMT  OD:322  OS:293 ¶OD: SRF temporal to ONH, (-) IRF, (-) drusen '
     '¶OS: central ?drusenoid PED  ¶ ¶ ¶ ¶', None, 1, -1, -1, date(2021, 11, 14)),  # synthetic
])
def test_srf_extract_build(text, headers, srf_re, srf_le, srf_unk, note_date):
    pre_json = extract_fluid(text, headers=Headers(headers))
    post_json = dumps_and_loads_json(pre_json)
    result = build_subretfluid_amd(post_json, note_date=note_date)
    assert result['amd_subretfluid_re'] == srf_re
    assert result['amd_subretfluid_le'] == srf_le
    assert result['amd_subretfluid_unk'] == srf_unk
