import pytest

from eye_extractor.output.ro import build_rao
from eye_extractor.ro.rao import RAO_PAT, get_rao


@pytest.mark.parametrize('text', [
    'retinal artery occlusion',
    'rvaso',
    'BRAO',
    'CRAO',
    'central retinal artery occlusion',
])
def test_rao_pattern(text):
    assert RAO_PAT.match(text)


@pytest.mark.parametrize('text, exp_value, exp_negword', [
    ('362.32B Branch retinal artery occlusion', 1, None),
])
def test_rao_value(text, exp_value, exp_negword):
    data = get_rao(text)
    assert len(data) > 0
    first_variable = list(data[0].values())[0]
    assert first_variable['value'] == exp_value
    assert first_variable['negated'] == exp_negword


@pytest.mark.parametrize('data, exp_rao_re, exp_rao_le', [
    ([], -1, -1),
    ([{'rao_yesno_le': {'value': 1, 'term': 'Branch retinal artery occlusion', 'label': 'yes', 'negated': None,
                        'regex': 'RAO_PAT', 'source': 'ALL'},
       'rao_yesno_re': {'value': 1, 'term': 'Branch retinal artery occlusion', 'label': 'yes', 'negated': None,
                        'regex': 'RAO_PAT', 'source': 'ALL'}}],
     1, 1)
])
def test_rao_to_column(data, exp_rao_re, exp_rao_le):
    result = build_rao(data)
    assert result['rao_yesno_re'] == exp_rao_re
    assert result['rao_yesno_le'] == exp_rao_le
