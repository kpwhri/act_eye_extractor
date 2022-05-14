import pytest

from eye_extractor.output.cataract import build_cataract
from eye_extractor.cataract.cataract import CATARACT_PAT, get_cataract


@pytest.mark.parametrize('text', [
    'significant cataract',
])
def test_cataract_pattern(text):
    assert CATARACT_PAT.match(text)


@pytest.mark.parametrize('text, exp_value, exp_negword', [
    ('visually significant cataract', 1, None),
])
def test_cataract_value(text, exp_value, exp_negword):
    data = get_cataract(text)
    assert len(data) > 0
    first_variable = list(data[0].values())[0]
    assert first_variable['value'] == exp_value
    assert first_variable['negated'] == exp_negword


@pytest.mark.parametrize('data, cataract_yesno_re, cataract_yesno_le', [
    ([], -1, -1),
    ([{'cataractiol_yesno_le': {'value': 1},
       'cataractiol_yesno_re': {'value': 1}}],
     1, 1)
])
def test_cataract_to_column(data, cataract_yesno_re, cataract_yesno_le):
    result = build_cataract(data)
    assert result['cataractiol_yesno_le'] == cataract_yesno_le
    assert result['cataractiol_yesno_re'] == cataract_yesno_re
