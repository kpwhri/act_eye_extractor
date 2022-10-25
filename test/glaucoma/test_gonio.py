import json

import pytest

from eye_extractor.exam.gonio import OPEN_PAT, CLOSED_PAT, extract_gonio
from eye_extractor.headers import Headers
from eye_extractor.output.glaucoma import build_gonio


@pytest.mark.parametrize('pat, text, exp', [
    (OPEN_PAT, 'gonio: open', True),
    (OPEN_PAT, 'gonio: opened', True),
    (CLOSED_PAT, 'gonio: closed', True),
])
def test_gonio_patterns(pat, text, exp):
    res = pat.search(text)
    assert bool(res) == exp


@pytest.mark.parametrize('text, headers, exp_gonio_re, exp_gonio_le, exp_gonio_unk', [
    ('gonioscopy, he has had open angles', None, 'UNKNOWN', 'UNKNOWN', 'OPEN'),
    ('', {'ANGLE': 'OPEN, OU'}, 'OPEN', 'OPEN', 'UNKNOWN'),
    ('', {'ANGLE': 'IV OU'}, 'OPEN', 'OPEN', 'UNKNOWN'),
    ('', {'ANGLE': '4 OU'}, 'OPEN', 'OPEN', 'UNKNOWN'),
    ('', {'ANGLE': '0 OD'}, 'CLOSED', 'UNKNOWN', 'UNKNOWN'),
])
def test_gonio_extract_build(text, headers, exp_gonio_re, exp_gonio_le, exp_gonio_unk):
    pre_json = extract_gonio(text, headers=Headers(headers))
    post_json = json.loads(json.dumps(pre_json))
    result = build_gonio(post_json)
    assert result['gonio_re'] == exp_gonio_re
    assert result['gonio_le'] == exp_gonio_le
    assert result['gonio_unk'] == exp_gonio_unk
