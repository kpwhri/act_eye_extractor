import json

import pytest

from eye_extractor.glaucoma.tx import extract_tx, OBSERVE_PAT, CONTINUE_RX_PAT, NEW_MEDICATION_PAT, ALT_PAT, SLT_PAT, \
    SURGERY_PAT, TRABECULOPLASTY_PAT
from eye_extractor.headers import Headers
from eye_extractor.output.glaucoma import build_tx


@pytest.mark.parametrize('pat, text, exp', [
    (OBSERVE_PAT, 'continue to observe', True),
    (CONTINUE_RX_PAT, 'continue meds', True),
    (NEW_MEDICATION_PAT, 'add meds', True),
    (ALT_PAT, 'R ALT', True),
    (SLT_PAT, 'R SLT', True),
    (SURGERY_PAT, 'surgery', True),
    (TRABECULOPLASTY_PAT, 'trabeculoplasty', True),
])
def test_glaucoma_tx_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) == exp


@pytest.mark.parametrize('text, headers, exp_glaucoma_tx_re, exp_glaucoma_tx_le, exp_glaucoma_tx_unk', [
    ('', {'PLAN': 'Continue to observe'}, 'UNKNOWN', 'UNKNOWN', 'OBSERVE'),
])
def test_glacuoma_tx_extract_and_build(text, headers, exp_glaucoma_tx_re, exp_glaucoma_tx_le, exp_glaucoma_tx_unk):
    pre_json = extract_tx(text or '', headers=Headers(headers), lateralities=None)
    post_json = json.loads(json.dumps(pre_json))
    result = build_tx(post_json)
    assert result['glaucoma_tx_re'] == exp_glaucoma_tx_re
    assert result['glaucoma_tx_le'] == exp_glaucoma_tx_le
    assert result['glaucoma_tx_unk'] == exp_glaucoma_tx_unk
