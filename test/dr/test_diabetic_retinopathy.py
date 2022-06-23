import pytest

from eye_extractor.dr.diabetic_retinopathy import get_dr

@pytest.mark.parametrize('text, exp_value, exp_negword', [
    ('MACULA: No visible diabetic retinopathy this visit', 0, 'no'),
])
def test_dr_value(text, exp_value, exp_negword):
    data = get_dr(text)
    variable = list(data[0].values())[0]

    assert variable['value'] == exp_value
    assert variable['negated'] == exp_negword