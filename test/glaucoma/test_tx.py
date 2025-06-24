import json

import pytest

import eye_extractor.glaucoma.tx as gl
import eye_extractor.common.algo.treatment as tx
from eye_extractor.sections.document import create_doc_and_sections
from eye_extractor.sections.headers import Headers
from eye_extractor.output.glaucoma import build_tx, build_tx_new
from eye_extractor.sections.patterns import SectionName

# test data
_patterns = [
    (tx.OBSERVE_PAT, gl.OBSERVE_PAT, 'continue to observe', True),
    (tx.CONTINUE_RX_PAT, gl.CONTINUE_RX_PAT, 'continue meds', True),
    (tx.NEW_MEDICATION_PAT, gl.NEW_MEDICATION_PAT, 'add meds', True),
    (tx.ALT_PAT, gl.ALT_PAT, 'R ALT', True),
    (tx.SLT_PAT, gl.SLT_PAT, 'R SLT', True),
    (tx.SURGERY_PAT, gl.SURGERY_PAT, 'surgery', True),
    (tx.TRABECULOPLASTY_PAT, gl.TRABECULOPLASTY_PAT, 'trabeculoplasty', True),
]
_end_to_end = [
    ('', {SectionName.PLAN: 'Continue to observe'}, 'UNKNOWN', 'UNKNOWN', 'OBSERVE'),
    ('', {SectionName.PLAN: 'trabeculoplasty od'}, 'TRABECULOPLASTY', 'UNKNOWN', 'UNKNOWN'),
    ('', {SectionName.PLAN: 'os: alt'}, 'UNKNOWN', 'ALT', 'UNKNOWN'),
]


def get(old_version=False):
    return [
        (x[1] if old_version else x[0], x[2], x[3])
        for x in _patterns
    ]


# Generic approach
@pytest.mark.parametrize('pat, text, exp', get())
def test_tx_patterns_for_glaucoma(pat, text, exp):
    m = pat.search(text)
    assert bool(m) == exp


@pytest.mark.parametrize('text, sections, exp_glaucoma_tx_re, exp_glaucoma_tx_le, exp_glaucoma_tx_unk', _end_to_end)
def test_tx_extract_and_build_for_glaucoma(text, sections, exp_glaucoma_tx_re, exp_glaucoma_tx_le, exp_glaucoma_tx_unk):
    doc = create_doc_and_sections(text, sections)
    pre_json = tx.extract_treatment(doc)
    post_json = json.loads(json.dumps(pre_json))
    result = build_tx_new(post_json)
    assert result['glaucoma_tx_re'] == exp_glaucoma_tx_re
    assert result['glaucoma_tx_le'] == exp_glaucoma_tx_le
    assert result['glaucoma_tx_unk'] == exp_glaucoma_tx_unk


# GLAUCOMA-targeted approach
@pytest.mark.parametrize('pat, text, exp', get(old_version=True))
def test_glaucoma_tx_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) == exp


@pytest.mark.parametrize('text, sections, exp_glaucoma_tx_re, exp_glaucoma_tx_le, exp_glaucoma_tx_unk', _end_to_end)
def test_glacuoma_tx_extract_and_build(text, sections, exp_glaucoma_tx_re, exp_glaucoma_tx_le, exp_glaucoma_tx_unk):
    doc = create_doc_and_sections(text, sections)
    pre_json = gl.extract_tx(doc)
    post_json = json.loads(json.dumps(pre_json))
    result = build_tx(post_json)
    assert result['glaucoma_tx_re'] == exp_glaucoma_tx_re
    assert result['glaucoma_tx_le'] == exp_glaucoma_tx_le
    assert result['glaucoma_tx_unk'] == exp_glaucoma_tx_unk
