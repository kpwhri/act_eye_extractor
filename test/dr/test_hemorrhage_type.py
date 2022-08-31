import json

import pytest

from eye_extractor.dr.hemorrhage_type import get_hemorrhage_type, HemorrhageType
from eye_extractor.output.dr import build_dot_blot_severity, build_hemorrhage_type, build_intraretinal_severity


@pytest.mark.parametrize('text, exp_value, exp_negword', [
    ('Acute left retinal tear with small vitreous hemorrhage', HemorrhageType.VITREOUS, None),
    ('OD: preretinal hemorrhage extending from temporal periphery', HemorrhageType.PRERETINAL, None),
    ('subretinal hemorrhage from his macular degeneration', HemorrhageType.SUBRETINAL, None),
    ('swelling and intraretinal hemorrhage', HemorrhageType.INTRARETINAL, None),
    ('dot blot hemorrhage near inferior margin of GA', HemorrhageType.DOT_BLOT, None)
])
def test_get_hemorrhage_type(text, exp_value, exp_negword):
    data = get_hemorrhage_type(text)
    variable = list(data[0].values())[0]

    assert len(data) > 0
    assert variable['value'] == exp_value
    assert variable['negated'] == exp_negword


@pytest.mark.parametrize('data, exp_hemorrhage_typ_dr_re, exp_hemorrhage_typ_dr_le', [
    ([], HemorrhageType.UNKNOWN, HemorrhageType.UNKNOWN),
    ([{'hemorrhage_typ_dr_re': 0}],
     HemorrhageType.NONE, HemorrhageType.UNKNOWN),
    ([{'hemorrhage_typ_dr_re': 1,
       'hemorrhage_typ_dr_le': 1}],
     HemorrhageType.INTRARETINAL,
     HemorrhageType.INTRARETINAL),
    ([{'hemorrhage_typ_dr_re': 2,
       'hemorrhage_typ_dr_le': 3}],
     HemorrhageType.DOT_BLOT,
     HemorrhageType.PRERETINAL),
    ([{'hemorrhage_typ_dr_le': 4}],
     HemorrhageType.UNKNOWN,
     HemorrhageType.VITREOUS),
    ([{'hemorrhage_typ_dr_re': 0,
       'hemorrhage_typ_dr_le': 5}],
     HemorrhageType.NONE,
     HemorrhageType.SUBRETINAL)
])
def test_build_hemorrhage_type(data, exp_hemorrhage_typ_dr_re, exp_hemorrhage_typ_dr_le):
    result = build_hemorrhage_type(data)
    assert result['hemorrhage_typ_dr_re'] == exp_hemorrhage_typ_dr_re
    assert result['hemorrhage_typ_dr_le'] == exp_hemorrhage_typ_dr_le


@pytest.mark.parametrize('text, hemorrhage_type_dr_re, hemorrhage_type_dr_le, hemorrhage_type_dr_unk', [
    ('Acute left retinal tear with small vitreous hemorrhage',
     HemorrhageType.UNKNOWN, HemorrhageType.VITREOUS, HemorrhageType.UNKNOWN),
    ('OD: preretinal hemorrhage extending from temporal periphery',
     HemorrhageType.PRERETINAL, HemorrhageType.UNKNOWN, HemorrhageType.UNKNOWN),
    ('subretinal hemorrhage from his macular degeneration',
     HemorrhageType.UNKNOWN, HemorrhageType.UNKNOWN, HemorrhageType.SUBRETINAL),
    ('swelling and intraretinal hemorrhage',
     HemorrhageType.UNKNOWN, HemorrhageType.UNKNOWN, HemorrhageType.INTRARETINAL),
    ('dot blot hemorrhage near inferior margin of GA',
     HemorrhageType.UNKNOWN, HemorrhageType.UNKNOWN, HemorrhageType.DOT_BLOT),
])
def test_hemorrhage_type_extract_and_build(text, hemorrhage_type_dr_re, hemorrhage_type_dr_le,
                                           hemorrhage_type_dr_unk):
    data = get_hemorrhage_type(text)
    data = json.loads(json.dumps(data))  # simulate write to/reading from file
    result = build_hemorrhage_type(data)

    assert result['hemorrhage_typ_dr_re'] == hemorrhage_type_dr_re
    assert result['hemorrhage_typ_dr_le'] == hemorrhage_type_dr_le
    assert result['hemorrhage_typ_dr_unk'] == hemorrhage_type_dr_unk


# Test severity
_intraretinal_severity_extract_and_build_cases = [
    ('mild intraretinal hemorrhage OU', {}, 'MILD', 'MILD', 'UNKNOWN'),
    ('Mild - moderate intraretinal heme OD', {}, 'MODERATE', 'UNKNOWN', 'UNKNOWN'),
    ('no intraretinal hemorrhage ou', {}, 'NONE', 'NONE', 'UNKNOWN'),
    ('moderate intraretinal heme OS', {}, 'UNKNOWN', 'MODERATE', 'UNKNOWN'),
    ('severe intraretinal hemorrhage', {}, 'UNKNOWN', 'UNKNOWN', 'SEVERE'),
    ('intraretinal heme severity=3Q OS', {}, 'UNKNOWN', 'Q3', 'UNKNOWN'),
    ('intraretinal hemorrhage temporal and inferior quadrant OD', {}, 'Q2', 'UNKNOWN', 'UNKNOWN'),
    ('nasal quadrant, hemorrhage intraretinal', {}, 'UNKNOWN', 'UNKNOWN', 'Q1'),
    ('intraretinal heme in all quadrants ou', {}, 'Q4', 'Q4', 'UNKNOWN'),
]

_dot_blot_severity_extract_and_build_cases = [
    ('mild dot blot hemorrhage OU', {}, 'MILD', 'MILD', 'UNKNOWN'),
    ('Mild - moderate dot blot heme OD', {}, 'MODERATE', 'UNKNOWN', 'UNKNOWN'),
    ('no dot blot hemorrhage ou', {}, 'NONE', 'NONE', 'UNKNOWN'),
    ('moderate dot blot heme OS', {}, 'UNKNOWN', 'MODERATE', 'UNKNOWN'),
    ('severe dot blot hemorrhage', {}, 'UNKNOWN', 'UNKNOWN', 'SEVERE'),
    ('dot blot heme severity=3Q OS', {}, 'UNKNOWN', 'Q3', 'UNKNOWN'),
    ('dot blot hemorrhage temporal and inferior quadrant OD', {}, 'Q2', 'UNKNOWN', 'UNKNOWN'),
    ('nasal quadrant, hemorrhage dot blot', {}, 'UNKNOWN', 'UNKNOWN', 'Q1'),
    ('dot blot heme in all quadrants ou', {}, 'Q4', 'Q4', 'UNKNOWN'),
]


@pytest.mark.parametrize('text, headers, exp_intraretinal_hem_re, exp_intraretinal_hem_le, '
                         'exp_intraretinal_hem_unk',
                         _intraretinal_severity_extract_and_build_cases)
def test_intraretinal_severity_extract_and_build(text,
                                                 headers,
                                                 exp_intraretinal_hem_re,
                                                 exp_intraretinal_hem_le,
                                                 exp_intraretinal_hem_unk):
    pre_json = get_hemorrhage_type(text)
    post_json = json.loads(json.dumps(pre_json))
    result = build_intraretinal_severity(post_json)
    assert result['intraretinal_hem_re'] == exp_intraretinal_hem_re
    assert result['intraretinal_hem_le'] == exp_intraretinal_hem_le
    assert result['intraretinal_hem_unk'] == exp_intraretinal_hem_unk


@pytest.mark.parametrize('text, headers, exp_dotblot_hem_re, exp_dotblot_hem_le, '
                         'exp_dotblot_hem_unk',
                         _dot_blot_severity_extract_and_build_cases)
def test_dot_blot_severity_extract_and_build(text,
                                             headers,
                                             exp_dotblot_hem_re,
                                             exp_dotblot_hem_le,
                                             exp_dotblot_hem_unk):
    pre_json = get_hemorrhage_type(text)
    post_json = json.loads(json.dumps(pre_json))
    result = build_dot_blot_severity(post_json)
    assert result['dotblot_hem_re'] == exp_dotblot_hem_re
    assert result['dotblot_hem_le'] == exp_dotblot_hem_le
    assert result['dotblot_hem_unk'] == exp_dotblot_hem_unk
