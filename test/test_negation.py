import pytest

from eye_extractor.common.negation import has_after, has_before, _handle_negation_with_punctuation, is_negated
from eye_extractor.laterality import LATERALITY_PLUS_COLON_PATTERN


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
])
def test_negwords_prenegation(text, term, exp_negated):
    """Test negwords global"""
    start_index = text.index(term)
    res = is_negated(start_index, text)
    assert bool(res) is exp_negated
