import json

import pytest


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
