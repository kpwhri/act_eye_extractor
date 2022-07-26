import json

import pytest

from eye_extractor.amd.cnv import CNV_PAT, extract_choroidalneovasc
from eye_extractor.headers import Headers
from eye_extractor.output.amd import build_choroidalneovasc


@pytest.mark.parametrize('pat, text, exp', [
    (CNV_PAT, 'cnv', True),
    (CNV_PAT, 'choroidal neovascular membrane', True),
    (CNV_PAT, 'choroidal neovascularisations', True),
])
def test_cnv_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) is exp


@pytest.mark.parametrize('text, headers, exp_cnv_re, exp_cnv_le, exp_cnv_unk', [
        ('no cnv', None, -1, -1, 0),
        ('OS: no evidence of choroidal neovascularization', None, -1, 0, -1),
    ])
def test_cnv_extract_build(text, headers, exp_cnv_re, exp_cnv_le, exp_cnv_unk, ):
    pre_json = extract_choroidalneovasc(text, headers=Headers(headers))
    post_json = json.loads(json.dumps(pre_json))
    result = build_choroidalneovasc(post_json)
    assert result['choroidalneovasc_re'] == exp_cnv_re
    assert result['choroidalneovasc_le'] == exp_cnv_le
    assert result['choroidalneovasc_unk'] == exp_cnv_unk
