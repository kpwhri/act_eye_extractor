import datetime
import json

import pytest

from eye_extractor.exam.cmt import CMT_PAT, extract_cmt, CMT_PAT_LE, CMT_PAT_RE
from eye_extractor.headers import Headers
from eye_extractor.output.exam import build_cmt


@pytest.mark.parametrize('pat, text, exp', [
    (CMT_PAT, 'CMT OD:300 sub-foveal drusen; OS 300 sub-foveal drusen', True),
    (CMT_PAT_RE, 'CMT OD:300 sub-foveal drusen; OS 300 sub-foveal drusen', True),
    (CMT_PAT_LE, 'CMT OS: 300 sub-foveal drusen', True),
])
def test_cmt_patterns(pat, text, exp):
    assert bool(pat.search(text)) == exp


@pytest.mark.parametrize('text, headers, macularoct_thickness_re, macularoct_thickness_le', [
    ('', {'OCT MACULA': 'CMT OD:300 sub-foveal drusen. OS 301 sub-foveal drusen'}, 300, 301),
    ('', {'OCT MACULA': 'CMT OD:300 sub-foveal drusen'}, 300, -1),
    ('', {'OCT MACULA': 'CMT OS:300 sub-foveal drusen'}, -1, 300),
])
def test_cmt_extract_build(text, headers, macularoct_thickness_re, macularoct_thickness_le):
    pre_json = extract_cmt(text, headers=Headers(headers))
    post_json = json.loads(json.dumps(pre_json))
    result = build_cmt(post_json, note_date=datetime.datetime(2022, 1, 1))
    assert result['macularoct_thickness_re'] == macularoct_thickness_re
    assert result['macularoct_thickness_le'] == macularoct_thickness_le
