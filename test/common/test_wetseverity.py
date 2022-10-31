import pytest

from eye_extractor.amd.wet import extract_wetamd_severity
from eye_extractor.common.json import dumps_and_loads_json
from eye_extractor.headers import Headers
from eye_extractor.output.shared import build_wet_severity


@pytest.mark.parametrize('text, headers, exp_wet_re, exp_wet_le, exp_wet_unk', [
    ('', {'MACULA': 'wet'}, 'UNKNOWN', 'UNKNOWN', 'YES'),
    ('', {'MACULA': 'not wet'}, 'UNKNOWN', 'UNKNOWN', 'NO'),
])
def test_wet_severity_extract_build(text, headers, exp_wet_re, exp_wet_le, exp_wet_unk):
    pre_json = extract_wetamd_severity(text, headers=Headers(headers))
    post_json = dumps_and_loads_json(pre_json)
    result = build_wet_severity(post_json)
    assert result['wet_severity_re'] == exp_wet_re
    assert result['wet_severity_le'] == exp_wet_le
    assert result['wet_severity_unk'] == exp_wet_unk
