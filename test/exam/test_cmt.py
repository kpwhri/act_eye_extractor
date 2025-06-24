import datetime
import json

import pytest

from eye_extractor.exam.cmt import CMT_PAT, extract_cmt, CMT_PAT_LE, CMT_PAT_RE
from eye_extractor.sections.document import create_doc_and_sections
from eye_extractor.output.exam import build_cmt
from eye_extractor.sections.patterns import SectionName


@pytest.mark.parametrize('pat, text, exp', [
    (CMT_PAT, 'CMT OD:300 sub-foveal drusen; OS 300 sub-foveal drusen', True),
    (CMT_PAT_RE, 'CMT OD:300 sub-foveal drusen; OS 300 sub-foveal drusen', True),
    (CMT_PAT_LE, 'CMT OS: 300 sub-foveal drusen', True),
])
def test_cmt_patterns(pat, text, exp):
    assert bool(pat.search(text)) == exp


@pytest.mark.parametrize('text, sections, macularoct_thickness_re, macularoct_thickness_le', [
    ('', {SectionName.OCT: 'CMT OD:300 sub-foveal drusen. OS 301 sub-foveal drusen'}, 300, 301),
    ('', {SectionName.OCT: 'CMT OD:300 sub-foveal drusen'}, 300, -1),
    ('', {SectionName.OCT: 'CMT OS:300 sub-foveal drusen'}, -1, 300),
])
def test_cmt_extract_build(text, sections, macularoct_thickness_re, macularoct_thickness_le):
    doc = create_doc_and_sections(text, sections)
    pre_json = extract_cmt(doc)
    post_json = json.loads(json.dumps(pre_json))
    result = build_cmt(post_json, note_date=datetime.datetime(2022, 1, 1))
    assert result['macularoct_thickness_re'] == macularoct_thickness_re
    assert result['macularoct_thickness_le'] == macularoct_thickness_le
