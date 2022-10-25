import json

import pytest

from eye_extractor.glaucoma.cct import CCT_OD_OS_PAT, CCT_OD_PAT, CCT_OS_PAT, CCT_OU_PAT, extract_cct, CCT_OS_OD_PAT, \
    CCT_OD_OS_GEN_PAT
from eye_extractor.headers import Headers
from eye_extractor.output.glaucoma import build_cct


@pytest.mark.parametrize('pat, text, exp', [
    pytest.param(CCT_OD_OS_PAT, 'thick cct', True, marks=pytest.mark.skip()),
    (CCT_OD_OS_GEN_PAT, 'Pachymetry: 565/565', True),
    (CCT_OD_OS_PAT, 'Pachymetry: 494 OD; 488 OS', True),
    (CCT_OS_PAT, 'Pachymetry: 488 OS', True),
    (CCT_OD_PAT, 'Pachymetry: 494 OD', True),
    (CCT_OD_PAT, 'Pachymetry: OD: 494', True),
    (CCT_OS_PAT, 'Pachymetry: OS: 494', True),
    (CCT_OU_PAT, 'Pachymetry: OU: 494', True),
    (CCT_OD_OS_PAT, 'Pachymetry: OD: 494 OS: 495', True),
    (CCT_OS_OD_PAT, 'Pachymetry: OS: 494 OD: 495', True),
    (CCT_OD_OS_PAT, 'Pachymetry: OS: 494 OD: 495', False),
    (CCT_OD_OS_PAT, 'PACHYMETRY: 470 microns OD and 480 microns OS', True),
    (CCT_OD_OS_PAT, 'PACHYMETRY: 470 microns OD, 480 microns OS', True),
])
def test_cct_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) == exp


@pytest.mark.parametrize('text, headers, exp_cct_re, exp_cct_le, exp_cct_unk', [
    ('Pachymetry: 494 OD; 488 OS', None, 494, 488, -1),
    ('Pachymetry: 494 OU', None, 494, 494, -1),
    ('', {'PACHYMETRY': '494 OD; 488 OS'}, 494, 488, -1),
    ('', {'PACHYMETRY': 'CCT 494 OS; 488 OD'}, 488, 494, -1),
    ('', {'CCT': '494'}, 494, 494, -1),
    ('Pachymetry  540/585 ', None, 540, 585, -1),
    ('Pachymetry: CCT  540, 585 ', None, 540, 585, -1),
])
def test_cct_extract_and_build(text, headers, exp_cct_re, exp_cct_le, exp_cct_unk):
    pre_json = extract_cct(text, headers=Headers(headers), lateralities=None)
    post_json = json.loads(json.dumps(pre_json))
    result = build_cct(post_json)
    assert result['centralcornealthickness_re'] == exp_cct_re
    assert result['centralcornealthickness_le'] == exp_cct_le
    assert result['centralcornealthickness_unk'] == exp_cct_unk
