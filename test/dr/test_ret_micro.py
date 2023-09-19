import json

import pytest

from eye_extractor.dr.ret_micro import get_ret_micro, RET_MICRO_PAT
from eye_extractor.headers import Headers
from eye_extractor.output.dr import build_ret_micro


# Test pattern.
_pattern_cases = [
    (RET_MICRO_PAT, 'ma', True),
    (RET_MICRO_PAT, 'retinal ma', True),
    (RET_MICRO_PAT, 'retinal microaneurysm', True),
]


def _get_pattern_cases():
    return [(x[0], x[1], x[2]) for x in _pattern_cases]


@pytest.mark.parametrize('pat, text, exp', _get_pattern_cases())
def test_ret_micro_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) == exp


# Test extract and build.
_ret_micro_extract_and_build_cases = [
    ('retinal microaneurysm ou', {}, 'YES NOS', 'YES NOS', 'UNKNOWN'),
]


@pytest.mark.parametrize('text, headers,'
                         'exp_ret_micro_re, exp_ret_micro_le, exp_ret_micro_unk',
                         _ret_micro_extract_and_build_cases)
def test_ret_micro_extract_and_build(text,
                                     headers,
                                     exp_ret_micro_re,
                                     exp_ret_micro_le,
                                     exp_ret_micro_unk):
    pre_json = get_ret_micro(text, headers=Headers(headers))
    post_json = json.loads(json.dumps(pre_json, default=str))
    result = build_ret_micro(post_json)
    assert result['ret_microaneurysm_re'] == exp_ret_micro_re
    assert result['ret_microaneurysm_le'] == exp_ret_micro_le
    assert result['ret_microaneurysm_unk'] == exp_ret_micro_unk

