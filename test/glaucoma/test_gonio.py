import json

import pytest

from eye_extractor.exam.gonio import OPEN_PAT, CLOSED_PAT, extract_gonio
from eye_extractor.sections.document import create_doc_and_sections
from eye_extractor.output.glaucoma import build_gonio
from eye_extractor.sections.patterns import SectionName


@pytest.mark.parametrize('pat, text, exp', [
    (OPEN_PAT, 'gonio: open', True),
    (OPEN_PAT, 'gonio: opened', True),
    (CLOSED_PAT, 'gonio: closed', True),
])
def test_gonio_patterns(pat, text, exp):
    res = pat.search(text)
    assert bool(res) == exp


@pytest.mark.parametrize('text, sections, exp_gonio_re, exp_gonio_le, exp_gonio_unk', [
    ('gonioscopy, he has had open angles', None, 'UNKNOWN', 'UNKNOWN', 'OPEN'),
    ('', {SectionName.ANGLE: 'OPEN, OU'}, 'OPEN', 'OPEN', 'UNKNOWN'),
    ('', {SectionName.ANGLE: 'IV OU'}, 'OPEN', 'OPEN', 'UNKNOWN'),
    ('', {SectionName.ANGLE: '4 OU'}, 'OPEN', 'OPEN', 'UNKNOWN'),
    ('', {SectionName.ANGLE: '0 OD'}, 'CLOSED', 'UNKNOWN', 'UNKNOWN'),
])
def test_gonio_extract_build(text, sections, exp_gonio_re, exp_gonio_le, exp_gonio_unk):
    doc = create_doc_and_sections(text, sections)
    pre_json = extract_gonio(doc)
    post_json = json.loads(json.dumps(pre_json))
    result = build_gonio(post_json)
    assert result['gonio_re'] == exp_gonio_re
    assert result['gonio_le'] == exp_gonio_le
    assert result['gonio_unk'] == exp_gonio_unk
