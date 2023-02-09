import pytest

from eye_extractor.nlp.negate.negation import NEGATED_LIST_PATTERN, find_negated_list_spans


_pattern_cases = [
    (NEGATED_LIST_PATTERN, 'no plums, carrots', True),
    (NEGATED_LIST_PATTERN, 'no plums, carrots, oranges', True),
    (NEGATED_LIST_PATTERN, '(-) plums, carrots, oranges', True),
    (NEGATED_LIST_PATTERN, '(-)plums, carrots, oranges', True),
    (NEGATED_LIST_PATTERN, 'novels, cookbooks, diaries', False),
    (NEGATED_LIST_PATTERN, 'No Microaneurysms/hemes, cotton-wool spots, exudates, IRMA, Venous beading', True),
]


def _get_pattern_cases():
    return [(x[0], x[1], x[2]) for x in _pattern_cases]


@pytest.mark.parametrize('pat, text, exp', _get_pattern_cases())
def test_negated_list_pattern(pat, text, exp):
    m = pat.search(text)
    assert bool(m) == exp


_find_negated_list_spans_cases = [
    ('no plums, carrots, oranges', [(0, 26)]),
    ('hello there! no plums, carrots, oranges', [(13, 39)]),
    ('Macula: flat, dry (-)heme, MA, HE, CWS, VB, IRMA, NVE OD, ERM OS.', [(18, 65)])
]


@pytest.mark.parametrize('text, exp_spans', _find_negated_list_spans_cases)
def test_find_unspecified_negated_list_items(text, exp_spans):
    actual_spans = find_negated_list_spans(text)
    assert len(actual_spans) == len(exp_spans)

    for actual, exp in zip(actual_spans, exp_spans):
        assert actual[0] == exp[0]
        assert actual[1] == exp[1]
