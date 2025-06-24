import json

import pytest

from eye_extractor.glaucoma.preglaucoma import extract_preglaucoma_dx, SUSPECT_PAT, PPG_PAT, HIGH_CD_PAT
from eye_extractor.sections.document import create_doc_and_sections
from eye_extractor.sections.headers import Headers
from eye_extractor.output.glaucoma import build_preglaucoma_dx


@pytest.mark.parametrize('pat, text, exp', [
    (SUSPECT_PAT, 'glauc suspect', True),
    (PPG_PAT, 'ppg', True),
    (PPG_PAT, 'pre-perimetric glaucoma', True),
    (HIGH_CD_PAT, 'increased cup-to-disc', True),
])
def test_preglaucoma_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) is exp


@pytest.mark.parametrize(
    'text, sections, exp_preglaucoma_re, exp_preglaucoma_le, exp_preglaucoma_unk', [
        ('increased c/d', None, 'UNKNOWN', 'UNKNOWN', 'INCREASED CD'),
    ])
def test_preglaucoma_extract_build(text, sections, exp_preglaucoma_re, exp_preglaucoma_le, exp_preglaucoma_unk):
    doc = create_doc_and_sections(text, sections)
    pre_json = extract_preglaucoma_dx(doc)
    post_json = json.loads(json.dumps(pre_json))
    result = build_preglaucoma_dx(post_json)
    assert result['preglaucoma_re'] == exp_preglaucoma_re
    assert result['preglaucoma_le'] == exp_preglaucoma_le
    assert result['preglaucoma_unk'] == exp_preglaucoma_unk
