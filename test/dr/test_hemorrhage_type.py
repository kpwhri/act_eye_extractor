import json

import pytest

from eye_extractor.dr.hemorrhage_type import get_hemorrhage_type, HemorrhageType
from eye_extractor.output.dr import build_hemorrhage_type


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
