import json

import pytest

from eye_extractor.amd.scar import extract_subret_fibrous, SCAR_PAT, MACULAR_SCAR_PAT, SUBRET_SCAR_PAT, \
    DISCIFORM_SCAR_PAT
from eye_extractor.headers import Headers
from eye_extractor.output.amd import build_subret_fibrous


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

# TODO: Create section tests for non-macular sections in `text` field.
# TODO: Write end-end tests that include header extraction OR that run entire note on a specific variable.
@pytest.mark.parametrize('text, headers, exp_subret_fibrous_re, exp_subret_fibrous_le, exp_subret_fibrous_unk', [
    ('', {'MACULA': 'scar'}, 'UNKNOWN', 'UNKNOWN', 'YES'),
    ('', {'MACULA': 'OD: macular scar'}, 'MACULAR', 'UNKNOWN', 'UNKNOWN'),
    ('', {'MACULA': 'sub ret scar os'}, 'UNKNOWN', 'SUBRETINAL', 'UNKNOWN'),
    ('disciform scar ou', None, 'DISCIFORM', 'DISCIFORM', 'UNKNOWN'),
    ('no disciform scar ou', None, 'NO', 'NO', 'UNKNOWN'),
    ('Macula scar Drusen and RPE changes', None, 'UNKNOWN', 'UNKNOWN', 'MACULAR'),
    ('', {'MACULA': 'scar Drusen and RPE changes'}, 'UNKNOWN', 'UNKNOWN', 'YES'),
    ('(H31.011) Macular scar of right eye', None, 'MACULAR', 'UNKNOWN', 'UNKNOWN'),
    ('OD: CMT: 258, large RPE scar vs. new CNVM nasal to fovea with possible mild SRF, diffuse drusen OD>OS',
     None, 'YES', 'UNKNOWN', 'UNKNOWN'),
    ('MACULA: Laser scars Od; trace thickening OS', None, 'UKNOWN', 'UNKNOWN', 'UNKNOWN'),
    ('Periphery - attached with peripheral scarring scarring, temporally subretinal hemorrhage/fibrosis',
     None, 'UNKNOWN', 'UNKNOWN', 'UNKNOWN'),
    ('Periphery - attached with peripheral scarring, temporal and superior subretinal hemorrhage/fibrosis',
     None, 'UNKNOWN', 'UNKNOWN', 'UNKNOWN'),
    ('Macula - central mild subretinalhemorrhage noted; temporal scarring', None, 'UNKNOWN', 'UNKNOWN', 'YES'),
    ('', {'MACULA': '- central mild subretinalhemorrhage noted; temporal scarring'}, 'UNKNOWN', 'UNKNOWN', 'YES'),
    ('MACULA: RPE scar off ctr, no edema, exudates, or hemorrhage, OU', None, 'UNKNOWN', 'UNKNOWN', 'YES'),
    ('', {'MACULA': ' RPE scar off ctr, no edema, exudates, or hemorrhage, OU'}, 'UNKNOWN', 'UNKNOWN', 'YES'),
    ('AMD Vs old RPE scar OD', None, 'YES', 'UNKNOWN', 'UNKNOWN'),
    ('Periphery: subretinal fibrosis and RPE change temporally', None, 'UNKNOWN', 'UNKNOWN', 'UNKNOWN'),
    ('', {'PERIPHERY': ' subretinal fibrosis and RPE change temporally'}, None, 'UNKNOWN', 'UNKNOWN', 'UNKNOWN'),
    ('disciform scar os', None, 'UNKNOWN', 'DISCIFORM', 'UNKNOWN'),
    ('SUBJECTIVE: The patient is here for followup evaluation of disciform scar os. has no new complaints.',
     None, 'UNKNOWN', 'DISCIFORM', 'UNKNOWN'),
    ('MACULA: Mottled od; shallow disciform scar os', None, 'UNKNOWN', 'DISCIFORM', 'UNKNOWN'),
    ('', {'MACULA': ' Mottled od; shallow disciform scar os'}, 'UNKNOWN', 'DISCIFORM', 'UNKNOWN'),
    ('MACULA:  Peripapillary scar with residual exudates only', None, 'UNKNOWN', 'UNKNOWN', 'YES'),
    ('', {'MACULA': '  Peripapillary scar with residual exudates only'}, 'UNKNOWN', 'UNKNOWN', 'YES'),
    ('OCT: no recurrent fluid od; Scar os', 'UNKNOWN', 'YES', 'UNKNOWN'),
    ('Follow up in 8 weeks for OD with IVE, OCT and DILATION OU.\nmacular scar', None, 'UNKNOWN', 'UNKNOWN', 'YES'),

])
def test_scar_extract_build(text, headers, exp_subret_fibrous_re, exp_subret_fibrous_le, exp_subret_fibrous_unk):
    pre_json = extract_subret_fibrous(text, headers=Headers(headers))
    post_json = json.loads(json.dumps(pre_json))
    result = build_subret_fibrous(post_json)
    assert result['subret_fibrous_re'] == exp_subret_fibrous_re
    assert result['subret_fibrous_le'] == exp_subret_fibrous_le
    assert result['subret_fibrous_unk'] == exp_subret_fibrous_unk
