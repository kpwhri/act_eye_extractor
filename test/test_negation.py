import pytest

from eye_extractor.common.negation import has_after, has_before


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
    ])
def test_has_before(text, terms, word_window, char_window, boundary_chars, skip_n_boundary_chars, exp):
    res = has_before(len(text), text, terms, word_window=word_window, char_window=char_window,
                     boundary_chars=boundary_chars, skip_n_boundary_chars=skip_n_boundary_chars)
    assert res == exp
