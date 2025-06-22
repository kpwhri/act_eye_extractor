import pytest

from eye_extractor.amd.dry import extract_dryamd_severity
from eye_extractor.common.json import dumps_and_loads_json
from eye_extractor.sections.headers import Headers
from eye_extractor.output.shared import build_dry_severity


@pytest.mark.parametrize(
    'text, headers, exp_dry_re, exp_dry_le, exp_dry_unk, note_date', [
        ('', {'MACULA': 'dry'}, 'UNKNOWN', 'UNKNOWN', 'YES', None),
        ('', {'MACULA': 'not dry'}, 'UNKNOWN', 'UNKNOWN', 'NO', None),
    ])
def test_dry_extract_build(text, headers, exp_dry_re, exp_dry_le, exp_dry_unk, note_date):
    pre_json = extract_dryamd_severity(text, headers=Headers(headers))
    post_json = dumps_and_loads_json(pre_json)
    result = build_dry_severity(post_json, note_date=note_date)
    assert result['dry_severity_re'] == exp_dry_re
    assert result['dry_severity_le'] == exp_dry_le
    assert result['dry_severity_unk'] == exp_dry_unk
