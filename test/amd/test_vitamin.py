import json

import pytest

from eye_extractor.amd.vitamins import VITAMIN_PAT, CONTINUE_VITAMIN_PAT, extract_amd_vitamin
from eye_extractor.sections.document import create_doc_and_sections
from eye_extractor.sections.headers import Headers
from eye_extractor.output.amd import build_amd_vitamin


@pytest.mark.parametrize('pat, text, exp', [
    (VITAMIN_PAT, 'ocuvite', True),
    (VITAMIN_PAT, 'preservision', True),
    (CONTINUE_VITAMIN_PAT, 'continue taking preservision', True),
])
def test_vitamin_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) is exp


@pytest.mark.parametrize('text, sections, exp_amd_vitamin', [
    ('', {'eye_meds': 'ocuvite'}, 1),
    ('', {'meds': 'ocuvite'}, 1),
    ('Continue using ocuvite', None, 1),
])
def test_vitamin_extract_build(text, sections, exp_amd_vitamin):
    doc = create_doc_and_sections(text, sections)
    pre_json = extract_amd_vitamin(doc)
    post_json = json.loads(json.dumps(pre_json))
    result = build_amd_vitamin(post_json)
    assert result['amd_vitamin'] == exp_amd_vitamin
