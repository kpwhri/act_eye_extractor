import pytest

from eye_extractor.output.uveitis import build_uveitis
from eye_extractor.uveitis.uveitis import UVEITIS_PAT, ALL_UVEITIS_PAT


@pytest.mark.parametrize('text, exp', [
    ('uveitis', 0),
    ('anterior uveitis', 1),
    ('posterior iritis', 1),
])
def test_uveitis_pattern(text, exp):
    assert bool(UVEITIS_PAT.search(text)) == exp


@pytest.mark.parametrize('text, exp', [
    ('uveitis', 1),
    ('anterior uveitis', 1),
    ('posterior iritis', 1),
])
def test_all_uveitis_pattern(text, exp):
    assert bool(ALL_UVEITIS_PAT.search(text)) == exp


@pytest.mark.parametrize('data, exp_uveitis_yesno_re, exp_uveitis_yesno_le', [
    ([], -1, -1),
])
def test_build_uveitis(data, exp_uveitis_yesno_re, exp_uveitis_yesno_le):
    result = build_uveitis(data)
    assert result['uveitis_yesno_re'] == exp_uveitis_yesno_re
    assert result['uveitis_yesno_le'] == exp_uveitis_yesno_le
