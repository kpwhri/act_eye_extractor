import json

import pytest

from eye_extractor.amd.wet import WET_PAT, WET_AMD_PAT, extract_wetamd_severity, WetSeverity
from eye_extractor.headers import Headers
from eye_extractor.output.amd import build_wetamd_severity, augment_wetamd_severity
from eye_extractor.output.variable import update_column


@pytest.mark.parametrize('pat, text, exp', [
    (WET_PAT, 'wet', True),
    (WET_AMD_PAT, 'wet amd', True),
    (WET_AMD_PAT, 'nvARMD', True),
    (WET_AMD_PAT, 'macular degeneration: n', False),
])
def test_wet_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) is exp


@pytest.mark.parametrize('text, headers, exp_wetamd_severity_re, exp_wetamd_severity_le, exp_wetamd_severity_unk', [
    ('', {'MACULA': 'wet'}, 'UNKNOWN', 'UNKNOWN', 'YES'),
    ('', {'MACULA': 'not wet'}, 'UNKNOWN', 'UNKNOWN', 'NO'),
    ('', {'MACULA': 'non wet amd od'}, 'NO', 'UNKNOWN', 'UNKNOWN'),
    ('', {'ASSESSMENT': 'exudative od'}, 'YES', 'UNKNOWN', 'UNKNOWN'),
    ('', {'ASSESSMENT': '(H35.32) age-related macular degeneration, wet, right eye'}, 'YES', 'UNKNOWN', 'UNKNOWN'),
    ('neovascular armd', None, 'UNKNOWN', 'UNKNOWN', 'YES'),
    ('non-neovascular armd', None, 'UNKNOWN', 'UNKNOWN', 'NO'),
    ('non-exudative macular degeneration od', None, 'NO', 'UNKNOWN', 'UNKNOWN'),
])
def test_wet_extract_build(text, headers, exp_wetamd_severity_re, exp_wetamd_severity_le, exp_wetamd_severity_unk):
    pre_json = extract_wetamd_severity(text, headers=Headers(headers))
    post_json = json.loads(json.dumps(pre_json))
    result = build_wetamd_severity(post_json)
    assert result['wetamd_severity_re'] == exp_wetamd_severity_re
    assert result['wetamd_severity_le'] == exp_wetamd_severity_le
    assert result['wetamd_severity_unk'] == exp_wetamd_severity_unk


def test_wet_augment():
    srh_result = {'subretinal_hem_re': 1}
    wet_result = {'wetamd_severity_re': 'UNKNOWN'}
    res = augment_wetamd_severity(wet_result, srh_result=srh_result, is_amd=True)
    assert res['wetamd_severity_re'] == 'YES'
