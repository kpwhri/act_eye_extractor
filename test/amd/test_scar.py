import json

import pytest

from eye_extractor.amd.scar import extract_subret_fibrous, SCAR_PAT, MACULAR_SCAR_PAT, SUBRET_SCAR_PAT, \
    DISCIFORM_SCAR_PAT
from eye_extractor.sections.document import create_doc_and_sections
from eye_extractor.sections.headers import Headers
from eye_extractor.output.amd import build_subret_fibrous
from eye_extractor.sections.patterns import SectionName


@pytest.mark.parametrize('pat, text, exp', [
    (SCAR_PAT, 'scar', True),
    (MACULAR_SCAR_PAT, 'macular scar', True),
    (SUBRET_SCAR_PAT, 'sub ret scar', True),
    (SUBRET_SCAR_PAT, 'subretinal scar', True),
    (DISCIFORM_SCAR_PAT, 'disciform scar', True),
])
def test_scar_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) is exp


# TODO: Ignore mentions of scar in 'Periphery' sections. Headers will not capture most mentions, use alternative.
# TODO: Write end-end tests that include header extraction OR that run entire note on a specific variable.
@pytest.mark.parametrize('text, sections, exp_subret_fibrous_re, exp_subret_fibrous_le, exp_subret_fibrous_unk', [
    ('', {'MACULA': 'scar'}, 'UNKNOWN', 'UNKNOWN', 'YES'),
    ('', {'MACULA': 'OD: macular scar'}, 'MACULAR', 'UNKNOWN', 'UNKNOWN'),
    ('', {'MACULA': 'sub ret scar os'}, 'UNKNOWN', 'SUBRETINAL', 'UNKNOWN'),
    ('disciform scar ou', None, 'DISCIFORM', 'DISCIFORM', 'UNKNOWN'),
    ('no disciform scar ou', None, 'NO', 'NO', 'UNKNOWN'),
    ('Macula scar Drusen and RPE changes', None, 'UNKNOWN', 'UNKNOWN', 'MACULAR'),
    ('', {'MACULA': 'scar Drusen and RPE changes'}, 'UNKNOWN', 'UNKNOWN', 'YES'),
    ('(H31.011) Macular scar of right eye', None, 'MACULAR', 'UNKNOWN', 'UNKNOWN'),
    ('OCT OD: CMT: 258, large RPE scar vs. new CNVM nasal to fovea with possible mild SRF, diffuse drusen OD>OS',
     None, 'YES', 'UNKNOWN', 'UNKNOWN'),
    ('MACULA: Laser scars Od; trace thickening OS', None, 'UNKNOWN', 'UNKNOWN', 'UNKNOWN'),
    ('¶Periphery - attached with peripheral scarring scarring, temporally subretinal hemorrhage/fibrosis',
     None, 'UNKNOWN', 'UNKNOWN', 'UNKNOWN'),
    ('¶Periphery - attached with peripheral scarring, temporal and superior subretinal hemorrhage/fibrosis',
     None, 'UNKNOWN', 'UNKNOWN', 'UNKNOWN'),
    ('Macula - central mild subretinalhemorrhage noted; temporal scarring', None, 'UNKNOWN', 'UNKNOWN', 'YES'),
    ('', {'MACULA': '- central mild subretinalhemorrhage noted; temporal scarring'}, 'UNKNOWN', 'UNKNOWN', 'YES'),
    ('MACULA: RPE scar off ctr, no edema, exudates, or hemorrhage, OU', None, 'UNKNOWN', 'UNKNOWN', 'YES'),
    ('', {'MACULA': ' RPE scar off ctr, no edema, exudates, or hemorrhage, OU'}, 'UNKNOWN', 'UNKNOWN', 'YES'),
    ('AMD Vs old RPE scar OD', None, 'YES', 'UNKNOWN', 'UNKNOWN'),
    ('¶Periphery: subretinal fibrosis and RPE change temporally', None, 'UNKNOWN', 'UNKNOWN', 'UNKNOWN'),
    ('disciform scar os', None, 'UNKNOWN', 'DISCIFORM', 'UNKNOWN'),
    ('SUBJECTIVE: The patient is here for followup evaluation of disciform scar os. has no new complaints.',
     None, 'UNKNOWN', 'UNKNOWN', 'UNKNOWN'),  # can't trust subjective
    ('MACULA: Mottled od; shallow disciform scar os', None, 'UNKNOWN', 'DISCIFORM', 'UNKNOWN'),
    ('', {'MACULA': ' Mottled od; shallow disciform scar os'}, 'UNKNOWN', 'DISCIFORM', 'UNKNOWN'),
    ('MACULA:  Peripapillary scar with residual exudates only', None, 'UNKNOWN', 'UNKNOWN', 'YES'),
    ('', {'MACULA': '  Peripapillary scar with residual exudates only'}, 'UNKNOWN', 'UNKNOWN', 'YES'),
    ('OCT: no recurrent fluid od; Scar os', None, 'UNKNOWN', 'YES', 'UNKNOWN'),
    pytest.param('PLAN: Follow up in 8 weeks for OD with IV E, OCT and DILATION OU. ¶ ¶ ¶ ¶macular scar ¶',
     None, 'UNKNOWN', 'UNKNOWN', 'MACULAR', marks=pytest.mark.skip()),  # TODO: not sure we should accept this?
    ('A pigmented scar-like lesion', None, 'UNKNOWN', 'UNKNOWN', 'UNKNOWN'),
    ('MACULA: trace ERM OD and para-macular scar superior to fovea', None, 'MACULAR', 'UNKNOWN', 'UNKNOWN'),
    ('', {'MACULA': ' trace ERM OD and para-macular scar superior to fovea'}, 'MACULAR', 'UNKNOWN', 'UNKNOWN'),
    ('MACULA:  Mottled RPE OD; scar OS without edema, exudates, or hemorrhage, OU', None, 'UNKNOWN', 'YES', 'UNKNOWN'),
    ('', {'MACULA': '  Mottled RPE OD; scar OS without edema, exudates, or hemorrhage, OU'},
     'UNKNOWN', 'YES', 'UNKNOWN'),
    ('ASSESSMENT : ARMD OU dry with disciform scar OS Stable', None, 'UNKNOWN', 'DISCIFORM', 'UNKNOWN'),
    ('¶Periphery: superior chorioretinal scar', None, 'UNKNOWN', 'UNKNOWN', 'UNKNOWN'),
    ('Hx of avastin os with disciform scar.', None, 'UNKNOWN', 'UNKNOWN', 'UNKNOWN'),
    ('Macular scar OD', None, 'MACULAR', 'UNKNOWN', 'UNKNOWN'),
    ('366.50 PCO (posterior capsular opacification), left ¶363.32 Other macular scars of chorioretina',
     None, 'UNKNOWN', 'UNKNOWN', 'MACULAR'),
    ('IOL OS poor vision due to macular scar', None, 'UNKNOWN', 'MACULAR', 'UNKNOWN'),
    ('¶PERIPHERAL RETINA: disciform scar OD', None, 'UNKNOWN', 'UNKNOWN', 'UNKNOWN'),
    ('SRNVM OD, evolving\ndisciform scar in evolution', None, 'DISCIFORM', 'UNKNOWN', 'UNKNOWN'),
    # TODO: Fix laterality (intervening chars) to pass below case.
    # ('Oct macula: 2/4/2017 CMT OD: 202, no intraretinal or subretinal fluid OS: 245, disciform scar - Eylea OD',
    #  None, 'UNKNOWN', 'DISCIFORM', 'UNKNOWN'),  # synthetic
    ('MACULA: clr OU ¶No hem, no exud, no CWS OU ¶OS ~1.5dd, h oval white glial scar ~1dd temp of fov',
     None, 'UNKNOWN', 'MACULAR', 'UNKNOWN'),
    ('', {'MACULA': ' clr OU ¶No hem, no exud, no CWS OU ¶OS ~1.5dd, h oval white glial scar ~1dd temp of fov'},
     'UNKNOWN', 'MACULAR', 'UNKNOWN'),
    ("possibly 2' macular scar", None, 'UNKNOWN', 'UNKNOWN', 'UNKNOWN'),
    ('Other macular scars of chorioretina', None, 'UNKNOWN', 'UNKNOWN', 'MACULAR'),
    ('Plan.) her visual synmptoms might be due to her macular scar', None, 'UNKNOWN', 'UNKNOWN', 'MACULAR'),
    ('MACULA: Two tiny spots of heme OD; Disciform scar os with trace heme without edema, exudates, or hemorrhage, OU',
     None, 'UNKNOWN', 'DISCIFORM', 'UNKNOWN'),
    ('', {'MACULA': ' Two tiny spots of heme OD; Disciform scar os with trace heme without edema, '
                    'exudates, or hemorrhage, OU'}, 'UNKNOWN', 'DISCIFORM', 'UNKNOWN'),
    ('MACULA:  Drusen od; disciform scar os', None, 'UNKNOWN', 'DISCIFORM', 'UNKNOWN'),
    ('', {'MACULA': '  Drusen od; disciform scar os'}, 'UNKNOWN', 'DISCIFORM', 'UNKNOWN'),
    # PURPOSE: prioritize scar in macula
    ('MACULA: disciform scar od \nPLAN: treatment for scar', {}, 'DISCIFORM', 'UNKNOWN', 'UNKNOWN'),
])
def test_scar_extract_build(text, sections, exp_subret_fibrous_re, exp_subret_fibrous_le, exp_subret_fibrous_unk):
    doc = create_doc_and_sections(text, sections, default_section=SectionName.MACULA)
    pre_json = extract_subret_fibrous(doc)
    post_json = json.loads(json.dumps(pre_json, default=str))
    result = build_subret_fibrous(post_json)
    assert result['subret_fibrous_re'] == exp_subret_fibrous_re
    assert result['subret_fibrous_le'] == exp_subret_fibrous_le
    assert result['subret_fibrous_unk'] == exp_subret_fibrous_unk
