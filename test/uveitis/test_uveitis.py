import pytest

from eye_extractor.common.json import dumps_and_loads_json
from eye_extractor.output.uveitis import build_uveitis
from eye_extractor.uveitis.uveitis import UVEITIS_PAT, ALL_UVEITIS_PAT, get_uveitis


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


@pytest.mark.parametrize(
    'text, exp_uveitis_yesno_re, exp_uveitis_yesno_le, exp_uveitis_yesno_unk',
    [
        ('', -1, -1, -1),
        ('uveitis od', 1, -1, -1),
        ('OS: no uveitis', -1, 0, -1),
    ]
)
def test_extract_and_build_uveitis(text, exp_uveitis_yesno_re, exp_uveitis_yesno_le, exp_uveitis_yesno_unk):
    pre_json = get_uveitis(text)
    post_json = dumps_and_loads_json(pre_json)
    result = build_uveitis(post_json)
    assert result['uveitis_yesno_re'] == exp_uveitis_yesno_re
    assert result['uveitis_yesno_le'] == exp_uveitis_yesno_le
    assert result['uveitis_yesno_unk'] == exp_uveitis_yesno_unk
