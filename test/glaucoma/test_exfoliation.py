import json

import pytest

from eye_extractor.glaucoma.exfoliation import extract_exfoliation, EXFOLIATION_PAT
from eye_extractor.output.glaucoma import build_exfoliation
from eye_extractor.sections.document import create_doc_and_sections


@pytest.mark.parametrize('pat, text, exp', [
    (EXFOLIATION_PAT, 'capsulare', True),
    (EXFOLIATION_PAT, 'pseudo-exfoliative', True),
    (EXFOLIATION_PAT, 'pxg', False),
    (EXFOLIATION_PAT, 'peg', False),
])
def test_exfoliation_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) is exp


@pytest.mark.parametrize(
    'text, sections, exp_exfoliation_re, exp_exfoliation_le, exp_exfoliation_unk', [
        ('capsulare glaucoma', None, -1, -1, -1),
    ])
def test_exfoliation_extract_build(text, sections, exp_exfoliation_re, exp_exfoliation_le, exp_exfoliation_unk):
    doc = create_doc_and_sections(text, sections)
    pre_json = extract_exfoliation(doc)
    post_json = json.loads(json.dumps(pre_json))
    result = build_exfoliation(post_json)
    assert result['exfoliation_re'] == exp_exfoliation_re
    assert result['exfoliation_le'] == exp_exfoliation_le
    assert result['exfoliation_unk'] == exp_exfoliation_unk
