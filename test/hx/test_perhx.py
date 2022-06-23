import pytest

from eye_extractor.history.perhx import create_personal_history


@pytest.mark.parametrize('text, exp', [
    ('PAST OCULAR HISTORY:    Cataract no    Diabetic retinopathy yes    SOCIAL:',
     {'cataracts': 0, 'dr': 1})
])
def test_personal_history_section(text, exp):
    res = create_personal_history(text)
    assert res == exp
