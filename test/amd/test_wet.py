import json

import pytest

from eye_extractor.amd.wet import WET_PAT, WET_AMD_PAT, extract_wetamd_severity
from eye_extractor.headers import Headers
from eye_extractor.output.amd import build_wetamd_severity


@pytest.mark.parametrize('pat, text, exp', [
    (WET_PAT, 'wet', True),
    (WET_AMD_PAT, 'wet amd', True),
    (WET_AMD_PAT, 'nvARMD', True),
])
def test_wet_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) is exp


@pytest.mark.parametrize('text, headers, exp_wetamd_severity_re, exp_wetamd_severity_le, exp_wetamd_severity_unk', [
    ('', {'MACULA': 'wet'}, 'UNKNOWN', 'UNKNOWN', 'UNSPECIFIED'),
    ('', {'ASSESSMENT': 'exudative od'}, 'UNSPECIFIED', 'UNKNOWN', 'UNKNOWN'),
    ('neovascular armd', None, 'UNKNOWN', 'UNKNOWN', 'UNSPECIFIED'),
    ('non-neovascular armd', None, 'UNKNOWN', 'UNKNOWN', 'NO'),
])
def test_wet_extract_build(text, headers, exp_wetamd_severity_re, exp_wetamd_severity_le, exp_wetamd_severity_unk):
    pre_json = extract_wetamd_severity(text, headers=Headers(headers))
    post_json = json.loads(json.dumps(pre_json))
    result = build_wetamd_severity(post_json)
    assert result['wetamd_severity_re'] == exp_wetamd_severity_re
    assert result['wetamd_severity_le'] == exp_wetamd_severity_le
    assert result['wetamd_severity_unk'] == exp_wetamd_severity_unk
