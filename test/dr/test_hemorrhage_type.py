import json

import pytest

from eye_extractor.dr.hemorrhage_type import get_hemorrhage_type, HemorrhageType
from eye_extractor.output.dr import (
    build_dot_blot_severity,
    build_hemorrhage_type,
    build_intraretinal_severity,
    build_preretinal_severity,
    build_vitreous_severity,
)


@pytest.mark.parametrize('text, exp_value, exp_negword', [
    ('Acute left retinal tear with small vitreous hemorrhage', HemorrhageType.VITREOUS, None),
    ('OD: preretinal hemorrhage extending from temporal periphery', HemorrhageType.PRERETINAL, None),
    ('subretinal hemorrhage from his macular degeneration', HemorrhageType.SUBRETINAL, None),
    ('swelling and intraretinal hemorrhage', HemorrhageType.INTRARETINAL, None),
    ('dot blot hemorrhage near inferior margin of GA', HemorrhageType.DOT_BLOT, None)
])
def test_get_hemorrhage_type(text, exp_value, exp_negword):
    data = get_hemorrhage_type(text)
    variable = list(data[-2].values())[0]  # 'hemorrhage_typ_dr' will be last variable added to `data`.

    assert len(data) > 0
    assert variable['value'] == exp_value
    assert variable['negated'] == exp_negword


@pytest.mark.parametrize('data, exp_hemorrhage_typ_dr_re, exp_hemorrhage_typ_dr_le', [
    ([], HemorrhageType.UNKNOWN, HemorrhageType.UNKNOWN),
    ([{'hemorrhage_typ_dr_re': 0}],
     HemorrhageType.NONE, HemorrhageType.UNKNOWN),
    ([{'hemorrhage_typ_dr_re': 2,
       'hemorrhage_typ_dr_le': 2}],
     HemorrhageType.INTRARETINAL,
     HemorrhageType.INTRARETINAL),
    ([{'hemorrhage_typ_dr_re': 3,
       'hemorrhage_typ_dr_le': 4}],
     HemorrhageType.DOT_BLOT,
     HemorrhageType.PRERETINAL),
    ([{'hemorrhage_typ_dr_le': 5}],
     HemorrhageType.UNKNOWN,
     HemorrhageType.VITREOUS),
    ([{'hemorrhage_typ_dr_re': 0,
       'hemorrhage_typ_dr_le': 6}],
     HemorrhageType.NONE,
     HemorrhageType.SUBRETINAL)
])
def test_build_hemorrhage_type(data, exp_hemorrhage_typ_dr_re, exp_hemorrhage_typ_dr_le):
    result = build_hemorrhage_type(data)
    assert result['hemorrhage_typ_dr_re'] == exp_hemorrhage_typ_dr_re
    assert result['hemorrhage_typ_dr_le'] == exp_hemorrhage_typ_dr_le


@pytest.mark.parametrize('text, headers, hemorrhage_type_dr_re, hemorrhage_type_dr_le, hemorrhage_type_dr_unk', [
    ('Acute left retinal tear with small vitreous hemorrhage',
     {}, HemorrhageType.UNKNOWN, HemorrhageType.VITREOUS, HemorrhageType.UNKNOWN),
    ('OD: preretinal hemorrhage extending from temporal periphery',
     {}, HemorrhageType.PRERETINAL, HemorrhageType.UNKNOWN, HemorrhageType.UNKNOWN),
    ('subretinal hemorrhage from his macular degeneration',
     {}, HemorrhageType.UNKNOWN, HemorrhageType.UNKNOWN, HemorrhageType.SUBRETINAL),
    ('swelling and intraretinal hemorrhage',
     {}, HemorrhageType.UNKNOWN, HemorrhageType.UNKNOWN, HemorrhageType.INTRARETINAL),
    ('dot blot hemorrhage near inferior margin of GA',
     {}, HemorrhageType.UNKNOWN, HemorrhageType.UNKNOWN, HemorrhageType.DOT_BLOT),
    ('vitreous hemorrhage vs inflammation- iritis/uveitis OD',
     {}, HemorrhageType.VITREOUS, HemorrhageType.UNKNOWN, HemorrhageType.UNKNOWN),
    ('Hx of vx os for vitreous hemorrhage', {}, HemorrhageType.UNKNOWN, HemorrhageType.UNKNOWN, HemorrhageType.UNKNOWN),
    ('Resolved vitreous hemorrhage OD', {}, HemorrhageType.UNKNOWN, HemorrhageType.UNKNOWN, HemorrhageType.UNKNOWN),
    ('ADDED HX NOTES: ¶OD s/p BRVO, vitreous heme',
     {}, HemorrhageType.UNKNOWN, HemorrhageType.UNKNOWN, HemorrhageType.UNKNOWN),
    ('¶H/o posterior vitreous detachment with vitreous hemorrhage, left eye.',
     {}, HemorrhageType.UNKNOWN, HemorrhageType.UNKNOWN, HemorrhageType.UNKNOWN),
    # TODO: Resolve laterality issues to pass below tests.
    # ('¶VITREOUS:  Minimal vitreous heme ¶ ¶Discs pink OU',
    #  {}, HemorrhageType.UNKNOWN, HemorrhageType.UNKNOWN, HemorrhageType.VITREOUS),
    ('no new hemorrhage', {}, HemorrhageType.UNKNOWN, HemorrhageType.UNKNOWN, HemorrhageType.UNKNOWN),
    ('no new heme', {}, HemorrhageType.UNKNOWN, HemorrhageType.UNKNOWN, HemorrhageType.UNKNOWN),
    ('no new vitreous hemorrhage', {}, HemorrhageType.UNKNOWN, HemorrhageType.UNKNOWN, HemorrhageType.UNKNOWN),
    ('no new vitreous heme', {}, HemorrhageType.UNKNOWN, HemorrhageType.UNKNOWN, HemorrhageType.UNKNOWN),
    ('post pole with occasional dot/blot heme',
     {}, HemorrhageType.UNKNOWN, HemorrhageType.UNKNOWN, HemorrhageType.DOT_BLOT),
    ('PERIPHERAL RETINA: Normal appearance/flat; occasional dot heme',
     {}, HemorrhageType.UNKNOWN, HemorrhageType.UNKNOWN, HemorrhageType.DOT_BLOT),
    ('PERIPHERAL RETINA: Normal appearance/flat; dot heme OS>OD',
     {}, HemorrhageType.DOT_BLOT, HemorrhageType.DOT_BLOT, HemorrhageType.UNKNOWN),
    ('PERIPHERAL RETINA: Normal appearance/flat; dot heme OU',
     {}, HemorrhageType.DOT_BLOT, HemorrhageType.DOT_BLOT, HemorrhageType.UNKNOWN),
    ('MACULA: Occasional small blot heme in post pole OU',
     {}, HemorrhageType.DOT_BLOT, HemorrhageType.DOT_BLOT, HemorrhageType.UNKNOWN),
    ('VESSELS: isolated dot heme inf arcade OD',
     {}, HemorrhageType.DOT_BLOT, HemorrhageType.UNKNOWN, HemorrhageType.UNKNOWN),
    ('VESSELS:isolated dot heme inf arcade OD',
     {}, HemorrhageType.DOT_BLOT, HemorrhageType.UNKNOWN, HemorrhageType.UNKNOWN),
    ('Scattered dot blot hemes and MAs', {}, HemorrhageType.UNKNOWN, HemorrhageType.UNKNOWN, HemorrhageType.DOT_BLOT),
    ('MACULA: 1 dot heme OD, otherwise WNL OU',
     {}, HemorrhageType.DOT_BLOT, HemorrhageType.UNKNOWN, HemorrhageType.UNKNOWN),
    ('PERIPHERAL RETINA: Rare dot hemes OU.',
     {}, HemorrhageType.DOT_BLOT, HemorrhageType.DOT_BLOT, HemorrhageType.UNKNOWN),
    ('VESSELS: WNL OU occasional isolated dot/blot heme OU',
     {}, HemorrhageType.DOT_BLOT, HemorrhageType.DOT_BLOT, HemorrhageType.UNKNOWN),
    ('VESSELS: WNL OU isolated dot/blot heme OU',
     {}, HemorrhageType.DOT_BLOT, HemorrhageType.DOT_BLOT, HemorrhageType.UNKNOWN),
    ('Tiny dot hem sup nasal off disc OD', {}, HemorrhageType.DOT_BLOT, HemorrhageType.UNKNOWN, HemorrhageType.UNKNOWN),
    ('Macula: Dot and Blot hemorrhages OU',
     {}, HemorrhageType.DOT_BLOT, HemorrhageType.DOT_BLOT, HemorrhageType.UNKNOWN),
    # Chantelle says OU, previously in note both eyes were dilated and examined.
    # Unsure how to implement with OU with current, shallow approach.
    ('MACULA: rare tiny dot hem in arcades, no exud; string of 4 ~0.25dd size blot hem in a line nasal to disc OD. '
     'rare dot hem, no exud.', {}, HemorrhageType.DOT_BLOT, HemorrhageType.UNKNOWN, HemorrhageType.DOT_BLOT),
    ('Mac - rare dot heme os but hazy view',
     {}, HemorrhageType.UNKNOWN, HemorrhageType.DOT_BLOT, HemorrhageType.UNKNOWN),
    ('Mac - Normal x for rare dot heme od',
     {}, HemorrhageType.DOT_BLOT, HemorrhageType.UNKNOWN, HemorrhageType.UNKNOWN),
    ('MACULA: sm dot hem nsl to fov, some focal scarring OD',
     {}, HemorrhageType.DOT_BLOT, HemorrhageType.UNKNOWN, HemorrhageType.UNKNOWN),
    ('MACULA - dot heme OD',
     {}, HemorrhageType.DOT_BLOT, HemorrhageType.UNKNOWN, HemorrhageType.UNKNOWN),
    ('Macula paramacular laser marks,blot heme',
     {}, HemorrhageType.UNKNOWN, HemorrhageType.UNKNOWN, HemorrhageType.DOT_BLOT),
    ('VESSELS: 2-3 dot heme OU', {}, HemorrhageType.DOT_BLOT, HemorrhageType.DOT_BLOT, HemorrhageType.UNKNOWN),
    ('Macula show few dot hemorrhages.', {}, HemorrhageType.UNKNOWN, HemorrhageType.UNKNOWN, HemorrhageType.DOT_BLOT),
    ('MACULA - heme OD', {}, HemorrhageType.YES_NOS, HemorrhageType.UNKNOWN, HemorrhageType.UNKNOWN),  # synthetic
    ('VESSELS: WNL OU isolated heme OU',
     {}, HemorrhageType.YES_NOS, HemorrhageType.YES_NOS, HemorrhageType.UNKNOWN),  # synthetic
    ('Acute left retinal tear with small hemorrhage',
     {}, HemorrhageType.UNKNOWN, HemorrhageType.YES_NOS, HemorrhageType.UNKNOWN)  # synthetic
])
def test_hemorrhage_type_extract_and_build(text, headers, hemorrhage_type_dr_re, hemorrhage_type_dr_le,
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
    ('swelling and intraretinal hemorrhage', {}, 'UNKNOWN', 'UNKNOWN', 'YES NOS'),
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


_dot_blot_severity_extract_and_build_cases = [
    ('mild dot blot hemorrhage OU', {}, 'MILD', 'MILD', 'UNKNOWN'),
    ('Mild - moderate dot blot heme OD', {}, 'MODERATE', 'UNKNOWN', 'UNKNOWN'),
    ('no dot blot hemorrhage ou', {}, 'NONE', 'NONE', 'UNKNOWN'),
    ('moderate dot blot heme OS', {}, 'UNKNOWN', 'MODERATE', 'UNKNOWN'),
    ('severe dot blot hemorrhage', {}, 'UNKNOWN', 'UNKNOWN', 'SEVERE'),
    ('dot blot heme severity=3Q OS', {}, 'UNKNOWN', 'Q3', 'UNKNOWN'),
    ('dot blot hemorrhage temporal and inferior quadrant OD', {}, 'Q2', 'UNKNOWN', 'UNKNOWN'),
    ('dot blot heme in all quadrants ou', {}, 'Q4', 'Q4', 'UNKNOWN'),
    ('*scattered d/b hemes in all 4 quadrants (-)CWS', {}, 'UNKNOWN', 'UNKNOWN', 'Q4'),
    ('occasional dot/blot heme', {}, 'UNKNOWN', 'UNKNOWN', 'YES NOS'),
]


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


_preretinal_severity_extract_and_build_cases = [
    ('mild preretinal hemorrhage OU', {}, 'MILD', 'MILD', 'UNKNOWN'),  # synthetic
    ('Mild - moderate preretinal heme OD', {}, 'MODERATE', 'UNKNOWN', 'UNKNOWN'),  # synthetic
    ('no preretinal hemorrhage ou', {}, 'NONE', 'NONE', 'UNKNOWN'),  # synthetic
    ('moderate preretinal heme OS', {}, 'UNKNOWN', 'MODERATE', 'UNKNOWN'),  # synthetic
    ('severe preretinal hemorrhage', {}, 'UNKNOWN', 'UNKNOWN', 'SEVERE'),  # synthetic
    ('preretinal heme severity=3Q OS', {}, 'UNKNOWN', 'Q3', 'UNKNOWN'),  # synthetic
    ('preretinal hemorrhage temporal and inferior quadrant OD', {}, 'Q2', 'UNKNOWN', 'UNKNOWN'),  # synthetic
    ('nasal quadrant, hemorrhage preretinal', {}, 'UNKNOWN', 'UNKNOWN', 'Q1'),  # synthetic
    ('preretinal heme in all quadrants ou', {}, 'Q4', 'Q4', 'UNKNOWN'),  # synthetic
    ('swelling and preretinal hemorrhage', {}, 'UNKNOWN', 'UNKNOWN', 'YES NOS'),  # synthetic
]


@pytest.mark.parametrize('text, headers, exp_preretinal_hem_re, exp_preretinal_hem_le, '
                         'exp_preretinal_hem_unk',
                         _preretinal_severity_extract_and_build_cases)
def test_preretinal_severity_extract_and_build(text,
                                               headers,
                                               exp_preretinal_hem_re,
                                               exp_preretinal_hem_le,
                                               exp_preretinal_hem_unk):
    pre_json = get_hemorrhage_type(text)
    post_json = json.loads(json.dumps(pre_json))
    result = build_preretinal_severity(post_json)
    assert result['preretinal_hem_re'] == exp_preretinal_hem_re
    assert result['preretinal_hem_le'] == exp_preretinal_hem_le
    assert result['preretinal_hem_unk'] == exp_preretinal_hem_unk


_vitreous_severity_extract_and_build_cases = [
    ('mild vitreous hemorrhage OU', {}, 'MILD', 'MILD', 'UNKNOWN'),  # synthetic
    ('Mild - moderate vitreous heme OD', {}, 'MODERATE', 'UNKNOWN', 'UNKNOWN'),  # synthetic
    ('no vitreous hemorrhage ou', {}, 'NONE', 'NONE', 'UNKNOWN'),  # synthetic
    ('moderate vitreous heme OS', {}, 'UNKNOWN', 'MODERATE', 'UNKNOWN'),  # synthetic
    ('severe vitreous hemorrhage', {}, 'UNKNOWN', 'UNKNOWN', 'SEVERE'),  # synthetic
    ('vitreous heme severity=3Q OS', {}, 'UNKNOWN', 'Q3', 'UNKNOWN'),  # synthetic
    ('vitreous hemorrhage temporal and inferior quadrant OD', {}, 'Q2', 'UNKNOWN', 'UNKNOWN'),  # synthetic
    ('nasal quadrant, hemorrhage vitreous', {}, 'UNKNOWN', 'UNKNOWN', 'Q1'),  # synthetic
    ('vitreous heme in all quadrants ou', {}, 'Q4', 'Q4', 'UNKNOWN'),  # synthetic
    ('swelling and vitreous hemorrhage', {}, 'UNKNOWN', 'UNKNOWN', 'YES NOS'),  # synthetic
]


@pytest.mark.parametrize('text, headers, exp_vitreous_hem_re, exp_vitreous_hem_le, '
                         'exp_vitreous_hem_unk',
                         _vitreous_severity_extract_and_build_cases)
def test_vitreous_severity_extract_and_build(text,
                                             headers,
                                             exp_vitreous_hem_re,
                                             exp_vitreous_hem_le,
                                             exp_vitreous_hem_unk):
    pre_json = get_hemorrhage_type(text)
    post_json = json.loads(json.dumps(pre_json))
    result = build_vitreous_severity(post_json)
    assert result['vitreous_hem_re'] == exp_vitreous_hem_re
    assert result['vitreous_hem_le'] == exp_vitreous_hem_le
    assert result['vitreous_hem_unk'] == exp_vitreous_hem_unk
