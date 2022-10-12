import json

import pytest

from eye_extractor.amd.dry import DRY_PAT, DRY_AMD_PAT, extract_dryamd_severity
from eye_extractor.headers import Headers
from eye_extractor.output.amd import build_dryamd_severity


@pytest.mark.parametrize('pat, text, exp', [
    (DRY_PAT, 'dry', True),
    (DRY_AMD_PAT, 'dry amd', True),
    (DRY_AMD_PAT, 'atrophic armd', True),
])
def test_dry_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) is exp


@pytest.mark.parametrize('text, headers, exp_dryamd_severity_re, exp_dryamd_severity_le, exp_dryamd_severity_unk', [
    ('', {'MACULA': 'dry'}, 'UNKNOWN', 'UNKNOWN', 'YES'),
    ('', {'ASSESSMENT': 'atrophy od'}, 'YES', 'UNKNOWN', 'UNKNOWN'),
    ('atrophic armd', None, 'UNKNOWN', 'UNKNOWN', 'YES'),
    ('OD: non-exudative senile AMD', None, 'YES', 'UNKNOWN', 'UNKNOWN'),
])
def test_dry_extract_build(text, headers, exp_dryamd_severity_re, exp_dryamd_severity_le, exp_dryamd_severity_unk):
    pre_json = extract_dryamd_severity(text, headers=Headers(headers))
    post_json = json.loads(json.dumps(pre_json))
    result = build_dryamd_severity(post_json)
    assert result['dryamd_severity_re'] == exp_dryamd_severity_re
    assert result['dryamd_severity_le'] == exp_dryamd_severity_le
    assert result['dryamd_severity_unk'] == exp_dryamd_severity_unk
