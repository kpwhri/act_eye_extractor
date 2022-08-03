import pytest
from eye_extractor.dr.diabetic_retinopathy import HemorrhageType
from eye_extractor.output.dr import build_hemorrhage_type

@pytest.mark.parametrize('data, exp_hemorrhage_typ_dr_re, exp_hemorrhage_typ_dr_le', [
    ([], HemorrhageType.UNKNOWN, HemorrhageType.UNKNOWN),
    ([{'hemorrhage_typ_dr_re': 1}],
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
    ([{'hemorrhage_typ_dr_re': 1,
       'hemorrhage_typ_dr_le': 6}],
     HemorrhageType.NONE,
     HemorrhageType.SUBRETINAL)
])
def test_hemorrhage_type_to_column(data, exp_hemorrhage_typ_dr_re, exp_hemorrhage_typ_dr_le):
    result = build_hemorrhage_type(data)
    assert result['hemorrhage_typ_dr_re'] == exp_hemorrhage_typ_dr_re
    assert result['hemorrhage_typ_dr_le'] == exp_hemorrhage_typ_dr_le
