import pytest

from eye_extractor.history.perhx import create_personal_history


@pytest.mark.parametrize('text, exp', [
    ('PAST OCULAR HISTORY:    Cataract no    Diabetic retinopathy yes    SOCIAL:',
     {'cataracts': 0, 'dr': 1}),
    ('Past ocular history of:    no- Amblyopia/ strabismus-lazy eye  yes- Cataracts  Yes- Cornea:',
     {'cataracts': 1, 'amblyopia': 0}),
    ('Past Ocular Hx:   Cataract OD  IOL OS 12/2010  Drusen',
     {'cataracts': 1}),
    ('Family Past Ocular Hx:   yes- Cataract OD  brother no- Amblyopia father',  # test if family members included
     {}),
])
def test_personal_history_section(text, exp):
    res = create_personal_history(text)
    assert res == exp
