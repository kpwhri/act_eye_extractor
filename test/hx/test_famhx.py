import pytest

from eye_extractor.history.famhx import create_family_history


@pytest.mark.parametrize('text, exp', [
    ('FAMILY HISTORY:    Diabetes no    Migraine yes    SOCIAL HISTORY:',
     {'diabetes': 0, 'migraine': 1})
])
def test_family_history_section(text, exp):
    res = create_family_history(text)
    assert res == exp
