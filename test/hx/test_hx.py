from eye_extractor.history.common import find_end


def test_find_end():
    text = 'blah blah dr: yes gonioscopy: when'
    idx = find_end(text, 0)
    exp = ': when'
    assert text[idx:] == exp
