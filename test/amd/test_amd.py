import pytest

from eye_extractor.amd.amd import extract_amd
from eye_extractor.common.json import dumps_and_loads_json
from eye_extractor.headers import Headers
from eye_extractor.output.amd import build_amd


@pytest.mark.parametrize('text, headers, amd_re, amd_le, amd_unk, note_date', [
    ('', {'ASSESSMENT': 'Age-related macular degeneration, left eye'}, -1, 1, -1, None),
    ('', {'PLAN': 'Age-related macular degeneration, right eye'}, 1, -1, -1, None),
    ('ARMD OU', {}, 1, 1, -1, None),
    ('', {'MACULA': 'no amd OU'}, 0, 0, -1, None),
])
def test_amd(text, headers, amd_re, amd_le, amd_unk, note_date):
    pre_json = extract_amd(text, headers=Headers(headers))
    post_json = dumps_and_loads_json(pre_json)
    result = build_amd(post_json)
    assert result['amd_re'] == amd_re
    assert result['amd_le'] == amd_le
    assert result['amd_unk'] == amd_unk
