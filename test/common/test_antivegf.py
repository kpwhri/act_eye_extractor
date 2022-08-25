import json

import pytest

from eye_extractor.common.algo.treatment import extract_treatment
from eye_extractor.common.drug.antivegf import ANTIVEGF_RX
from eye_extractor.headers import Headers
from eye_extractor.output.amd import build_amd_antivegf
from eye_extractor.output.dr import build_dmacedema_antivegf


@pytest.mark.parametrize('pat, text, exp', [
    (ANTIVEGF_RX, 'aflibercept', True),
    (ANTIVEGF_RX, 'eyelea', True),
    (ANTIVEGF_RX, 'bevacizumab', True),
    (ANTIVEGF_RX, 'avastin', True),
    (ANTIVEGF_RX, 'ranibuzumab', True),
    (ANTIVEGF_RX, 'lucentis', True),
    (ANTIVEGF_RX, 'anti-vegf', True)
])
def test_antivegf_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) == exp


@pytest.mark.parametrize('text, headers, builder, prefix, exp_antivegf_re, exp_antivegf_le, exp_antivegf_unk', [
    ('s/p aflibercept', None, build_amd_antivegf, 'amd_', -1, -1, 2),
    # pytest.param('anti-VEGF intravitreal injection', None, build_dmacedema_antivegf, 'dmacedema_', -1, -1, 4,
    #              marks=pytest.mark.skip(reason="Failure to extract 'anti-vegf' from `ANTIVEGF_TO_ENUM`")),
    # ('Intravitreal injection of Avastin (Bevacizumab)', None, build_dmacedema_antivegf, 'dmacedema_', -1, -1, 1),
])
def test_antivegf_extract_and_build(text, headers, builder, prefix, exp_antivegf_re, exp_antivegf_le, exp_antivegf_unk):
    pre_json = extract_treatment(text, headers=Headers(headers), lateralities=None)
    post_json = json.loads(json.dumps(pre_json))
    result = builder(post_json)
    assert result[f'{prefix}antivegf_re'] == exp_antivegf_re
    assert result[f'{prefix}antivegf_le'] == exp_antivegf_le
    assert result[f'{prefix}antivegf_unk'] == exp_antivegf_unk
