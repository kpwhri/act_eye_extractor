import pytest

from eye_extractor.output.ro import build_rvo
from eye_extractor.ro.rvo import RVO_PAT, get_rvo


@pytest.mark.parametrize('text', [
    'retinal vein occlusion',
    'rvaso',
    'BRVO',
    'CRVO',
    'central retinal vein occlusion',
])
def test_rao_pattern(text):
    assert RVO_PAT.match(text)


@pytest.mark.parametrize('text, exp_value, exp_negword', [
    ('Branch retinal vein occlusion', 1, None),
])
def test_rao_value(text, exp_value, exp_negword):
    data = get_rvo(text)
    assert len(data) > 0
    first_variable = list(data[0].values())[0]
    assert first_variable['value'] == exp_value
    assert first_variable['negated'] == exp_negword


@pytest.mark.parametrize('data, exp_rvo_re, exp_rvo_le', [
    ([], -1, -1),
    ([{'rvo_yesno_le': {'value': 1, 'term': 'Branch retinal vein occlusion', 'label': 'yes', 'negated': None,
                        'regex': 'RVO_PAT', 'source': 'ALL'},
       'rvo_yesno_re': {'value': 1, 'term': 'Branch retinal vein occlusion', 'label': 'yes', 'negated': None,
                        'regex': 'RVO_PAT', 'source': 'ALL'}}],
     1, 1)
])
def test_rao_to_column(data, exp_rvo_re, exp_rvo_le):
    result = build_rvo(data)
    assert result['rvo_yesno_re'] == exp_rvo_re
    assert result['rvo_yesno_le'] == exp_rvo_le