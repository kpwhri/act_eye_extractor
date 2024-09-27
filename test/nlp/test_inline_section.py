import pytest

from eye_extractor.nlp.inline_section import is_inline_section, is_periphery, PERIPHERY_PAT


@pytest.mark.parametrize('match_start, text, pattern, exp_bool', [
    (50,  '¶Periphery - peripheral scarring, subretinal hemorrhage/fibrosis', PERIPHERY_PAT, True),
    (49,  '¶Periphery: peripheral scarring, subretinal hemorrhage/fibrosis', PERIPHERY_PAT, True),
    (50,  '¶PERIPHERY - peripheral scarring, subretinal hemorrhage/fibrosis', PERIPHERY_PAT, True),
    (49,  '¶PERIPHERY: peripheral scarring, subretinal hemorrhage/fibrosis', PERIPHERY_PAT, True),
    (78,  '¶no disciform scar ou ¶Periphery - peripheral scarring, subretinal hemorrhage/fibrosis',
     PERIPHERY_PAT, True),
    (101,  '¶Periphery - peripheral scarring, subretinal hemorrhage/fibrosis ¶MACULA: Clear & dry OU, subretinal scar',
     PERIPHERY_PAT, False),
    (13, 'no disciform scar ou', PERIPHERY_PAT, False),
    (14, '¶no disciform scar ou', PERIPHERY_PAT, False),
])
def test_is_inline_section(match_start, text, pattern, exp_bool):
    result = is_inline_section(match_start, text, pattern)
    assert result == exp_bool


@pytest.mark.parametrize('match_start, text, exp_bool', [
    (50,  '¶Periphery - peripheral scarring, subretinal hemorrhage/fibrosis', True),
    (49,  '¶Periphery: peripheral scarring, subretinal hemorrhage/fibrosis', True),
    (50,  '¶PERIPHERY - peripheral scarring, subretinal hemorrhage/fibrosis', True),
    (49,  '¶PERIPHERY: peripheral scarring, subretinal hemorrhage/fibrosis', True),
    (13, 'no disciform scar ou', False),
    (14, '¶no disciform scar ou', False),
    (50,  '¶Macula - peripheral scarring, subretinal hemorrhage/fibrosis', False),
    (49,  '¶Macula: peripheral scarring, subretinal hemorrhage/fibrosis', False),
])
def test_is_periphery(match_start, text, exp_bool):
    result = is_periphery(match_start, text)
    assert result == exp_bool
