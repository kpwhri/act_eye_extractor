import pytest

from eye_extractor.nlp.negate.negation import NEGATED_LIST_PATTERN

# Test pattern.
_pattern_cases = [
    (NEGATED_LIST_PATTERN, 'no plums, carrots, oranges', True),
    (NEGATED_LIST_PATTERN, '(-) plums, carrots, oranges', True),
    (NEGATED_LIST_PATTERN, '(-)plums, carrots, oranges', True),
    (NEGATED_LIST_PATTERN, 'novels, cookbooks, diaries', False),
]


def _get_pattern_cases():
    return [(x[0], x[1], x[2]) for x in _pattern_cases]


@pytest.mark.parametrize('pat, text, exp', _get_pattern_cases())
def test_negated_list_pattern(pat, text, exp):
    m = pat.search(text)
    assert bool(m) == exp
