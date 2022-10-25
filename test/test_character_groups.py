import pytest

from eye_extractor.nlp.character_groups import get_previous_text_to_newline


@pytest.mark.parametrize('index, text, exp_line', [
    (10, 'This\nthat', 'that'),
    (10, 'This¶that', 'that'),
])
def test_previous_text_to_newline(index, text, exp_line):
    line = get_previous_text_to_newline(index, text)
    assert line == exp_line
