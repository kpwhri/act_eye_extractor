import pytest

from eye_extractor.nlp.negate.negation import (
    find_unspecified_negated_list_items,
    has_after,
    has_before,
    is_negated,
    NegationStatus,
    NEGATED_LIST_PATTERN_COMMA,
    NEGATED_LIST_PATTERN_OR,
    NEGATED_LIST_PATTERN_SLASH,
    _find_negated_list_spans,
    _handle_negation_with_punctuation,
)
from eye_extractor.laterality import LATERALITY_PATTERN, LATERALITY_PLUS_COLON_PATTERN


@pytest.mark.parametrize(
    'start_idx, text, terms, word_window, char_window, boundary_chars, skip_n_boundary_chars, exp', [
        (0, ' no', {'no'}, 10, 0, ':', 0, 'no'),
        (0, ': no', {'no'}, 10, 0, ':', 0, None),  # stops at boundary_chars
        (1, ': no', {'no'}, 10, 0, ':', 0, 'no'),  # test index
        (0, ': no', {'no'}, 10, 0, ':', 10, 'no'),  # skip first boundary_chars
        (0, ': yes glaucoma: no', {'no'}, 10, 0, ':', 1, None),  # don't skip second boundary_chars
        (0, ': yes glaucoma: no', {'no'}, 10, 0, ':', 2, 'no'),  # skip first and second boundary_chars
        (0, ': yes glaucoma: no', {'no'}, 2, 0, ':', 2, None),  # limit to only two word lookahead
    ])
def test_has_after(start_idx, text, terms, word_window, char_window, boundary_chars, skip_n_boundary_chars, exp):
    res = has_after(start_idx, text, terms, word_window=word_window, char_window=char_window,
                    boundary_chars=boundary_chars, skip_n_boundary_chars=skip_n_boundary_chars)
    assert res == exp


@pytest.mark.parametrize(
    'text, terms, word_window, char_window, boundary_chars, skip_n_boundary_chars, exp', [
        ('no ', {'no'}, 10, 0, ':', 0, 'no'),
        ('no :', {'no'}, 10, 0, ':', 0, None),  # stops at boundary_chars
        ('no :', {'no'}, 10, 0, ':', 10, 'no'),  # skip first boundary_chars
        ('no glaucoma: yes :', {'no'}, 10, 0, ':', 1, None),  # don't skip second boundary_chars
        ('no glaucoma: yes :', {'no'}, 10, 0, ':', 2, 'no'),  # skip first and second boundary_chars
        ('no glaucoma: yes :', {'no'}, 2, 0, ':', 2, None),  # limit to only two word lookahead
        ('no d/b hemes, ', {'no'}, 3, 0, ':', 0, 'no'),  # keep 'd/b' as single item
        ('no d/ b hemes, ', {'no'}, 3, 0, ':', 0, None),  # space, so should be two chars
        ('no d / b hemes, ', {'no'}, 4, 0, ':', 0, 'no'),  # ensure that the `/` still gets skipped
    ])
def test_has_before(text, terms, word_window, char_window, boundary_chars, skip_n_boundary_chars, exp):
    res = has_before(len(text), text, terms, word_window=word_window, char_window=char_window,
                     boundary_chars=boundary_chars, skip_n_boundary_chars=skip_n_boundary_chars)
    assert res == exp


def test_skip_regex_after():
    text = 'gonioscopy: OU: closed'
    res1 = has_after(10, text, {'closed'}, skip_regex=None)
    assert res1 is None
    res2 = has_after(10, text, {'closed'}, skip_regex=LATERALITY_PLUS_COLON_PATTERN)
    assert res2 == 'closed'


def test_skip_regex_before():
    text = 'gonioscopy: OU: closed'
    res1 = has_before(16, text, {'gonioscopy'}, skip_regex=None, skip_n_boundary_chars=1)
    assert res1 is None
    res2 = has_before(16, text, {'gonioscopy'}, skip_regex=LATERALITY_PLUS_COLON_PATTERN, skip_n_boundary_chars=1)
    assert res2 == 'gonioscopy'


@pytest.mark.parametrize('text, exp', [
    ('2 - 4', '2 - 4'),
    ('2, -CVN', '2,  no CVN'),
    ('2 (-)CVN', '2  no CVN'),
    ('2 (-) CVN', '2  no  CVN'),
    ('DM w/out NPDR OU', 'DM without NPDR OU'),
])
def test_handle_negation_with_punctuation(text, exp):
    """Hacky way to handle negation in punctuation"""
    res = _handle_negation_with_punctuation(text)
    assert res == exp


@pytest.mark.parametrize('text, term, exp_negated', [
    ('(-)  holes, tears, or detachments OU', 'holes', True),
    ('(-)  holes, tears, or detachments OU', 'detachments', True),  # or is negated
    ('(-)  holes, tears, or detachments OU', 'tears', True),
    ('w/out holes, tears, or detachments OU', 'tears', True),
    ('w/o holes, tears, or detachments OU', 'tears', True),
    ('holes, tears, or detachments OU', 'tears', False),
    ('anti-vegf', 'vegf', False),
    ('no new SRF', 'SRF', False),
    ('not only SRF', 'SRF', False),
])
def test_negwords_prenegation(text, term, exp_negated):
    """Test negwords global"""
    start_index = text.index(term)
    res = is_negated(start_index, text)
    match res:
        case NegationStatus.UNKNOWN:
            assert res == exp_negated
        case _:
            assert bool(res) is exp_negated


_negated_list_pattern_cases = [
    (NEGATED_LIST_PATTERN_COMMA, 'no plums, carrots.', True),
    (NEGATED_LIST_PATTERN_COMMA, 'no plums, carrots, oranges\n', True),
    (NEGATED_LIST_PATTERN_COMMA, '(-) plums, carrots, oranges.\n', True),
    (NEGATED_LIST_PATTERN_COMMA, '(-)plums, carrots, oranges.', True),
    (NEGATED_LIST_PATTERN_COMMA, 'novels, cookbooks, diaries\n', False),
    (NEGATED_LIST_PATTERN_COMMA, 'Novels, cookbooks, diaries.', False),
    (NEGATED_LIST_PATTERN_COMMA, 'No Microaneurysms/hemes, cotton-wool spots, exudates, IRMA, Venous beading.', True),
    (NEGATED_LIST_PATTERN_COMMA, 'no venous beading', False),
    (NEGATED_LIST_PATTERN_SLASH, 'no venous beading', False),
    (NEGATED_LIST_PATTERN_SLASH, 'but no NVZE/hg/CWS/HE noted today', True),
    (NEGATED_LIST_PATTERN_OR, 'no venous beading', False),
    (NEGATED_LIST_PATTERN_OR, 'no pate or horseradish', True),
    (NEGATED_LIST_PATTERN_OR, 'but no CWS or HE', True),
]


def _get_negated_list_pattern_cases():
    return [(x[0], x[1], x[2]) for x in _negated_list_pattern_cases]


@pytest.mark.parametrize('pat, text, exp', _get_negated_list_pattern_cases())
def test_negated_list_pattern(pat, text, exp):
    m = pat.search(text)
    assert bool(m) == exp


_find_negated_list_spans_cases = [
    ('no plums, carrots, oranges.', [(0, 26, ',')]),
    ('hello there! no plums,  carrots,  oranges', [(13, 41, ',')]),
    ('Macula: flat, dry (-)heme, MA, HE, CWS, VB, IRMA, NVE OD, ERM OS.', [(18, 64, ',')]),
    ('but no NVZE/hg/CWS/HE noted today', [(4, 21, '/')]),
    ('Vessels: (-) MAs, Venous Beading, IRMA, CWS. Good caliber, color and crossings OU. '
     'No hemes, cotton-wool spots, exudates, IRMA, Venous beading', [(9, 43, ','), (83, 142, ',')]),
    ('Vessels: (-) MAs, Venous Beading, IRMA, CWS. Good caliber, color and crossings OU. '
     'LE with extensive PRP, but no NVZE/hg/CWS/HE noted today', [(9, 43, ','), (110, 127, '/')]),
    ('hello, (-)pate or horseradish please', [(7, 29, ' or ')]),
    ('Vessels: scattered MA/dot hgs, but no CWS or HE; no plaques or emboli noted',
     [(35, 47, ' or '), (49, 69, ' or ')]),
]


@pytest.mark.parametrize('text, exp_spans', _find_negated_list_spans_cases)
def test__find_negated_list_spans(text, exp_spans):
    actual_spans = _find_negated_list_spans(text)
    assert len(actual_spans) == len(exp_spans)

    for actual, exp in zip(actual_spans, exp_spans):
        assert actual[0] == exp[0]
        assert actual[1] == exp[1]
        assert actual[2] == exp[2]


_find_unspecified_negated_list_items_cases = [
    ('no plums, carrots, oranges.', [(3, 8), (10, 17), (19, 26)]),
    ('hello there! no plums,  carrots,  oranges', [(16, 21), (24, 31), (34, 41)]),
    ('Macula: flat, dry (-)heme, MA, HE, CWS, VB, IRMA, NVE OD, ERM OS.',
     [(21, 25), (27, 29), (31, 33), (35, 38), (40, 42), (44, 48)]),
    ('No Microaneurysms/hemes, cotton-wool spots, exudates, IRMA, Venous beading.',
     [(3, 23), (25, 42), (44, 52), (54, 58), (60, 74)]),
    ('but no NVZE/hg/CWS/HE noted today', [(7, 11), (12, 14), (15, 18), (19, 21)]),
    ('Vessels: (-) MAs, Venous Beading, IRMA, CWS. Good caliber, color and crossings OU. '
     'No hemes, cotton-wool spots, exudates, IRMA, Venous beading',
     [(13, 16), (18, 32), (34, 38), (40, 43), (86, 91), (93, 110), (112, 120), (122, 126), (128, 142)]),
    ('Vessels: (-) MAs, Venous Beading, IRMA, CWS. Good caliber, color and crossings OU. '
     'LE with extensive PRP, but no NVZE/hg/CWS/HE noted today',
     [(13, 16), (18, 32), (34, 38), (40, 43), (113, 117), (118, 120), (121, 124), (125, 127)]),
    ('Vessels: scattered MA/dot hgs, but no CWS or HE; no plaques or emboli noted',
     [(38, 41), (45, 47), (52, 59), (63, 69)]),
]


@pytest.mark.parametrize('text, exp_spans', _find_unspecified_negated_list_items_cases)
def test_find_unspecified_negated_list_items(text, exp_spans):
    actual_spans = find_unspecified_negated_list_items(text, LATERALITY_PATTERN)
    assert len(actual_spans) == len(exp_spans)

    for actual, exp in zip(actual_spans, exp_spans):
        assert actual[0] == exp[0]
        assert actual[1] == exp[1]
