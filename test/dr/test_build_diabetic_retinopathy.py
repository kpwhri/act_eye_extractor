import pytest
from eye_extractor.dr.diabetic_retinopathy import HemorrhageType
from eye_extractor.output.dr import build_dr, build_ret_micro, build_hemorrhage_type


@pytest.mark.parametrize('data, exp_diab_retinop_yesno_re, exp_diab_retinop_yesno_le', [
    ([], -1, -1),
    ([{'diab_retinop_yesno_re': {'value': 1},
       'diab_retinop_yesno_le': {'value': 1}}],
     1, 1),
    ([{'diab_retinop_yesno_re': {'value': 0},
       'diab_retinop_yesno_le': {'value': 0}}],
     0, 0),
    ([{'diab_retinop_yesno_re': {'value': 1}}], 1, -1),
    ([{'diab_retinop_yesno_le': {'value': 0}}], -1, 0)
])
def test_build_dr(data, exp_diab_retinop_yesno_re, exp_diab_retinop_yesno_le):
    result = build_dr(data)
    assert result['diab_retinop_yesno_re'] == exp_diab_retinop_yesno_re
    assert result['diab_retinop_yesno_le'] == exp_diab_retinop_yesno_le


@pytest.mark.parametrize('data, exp_ret_microaneurysm_re, exp_ret_microaneurysm_le', [
    ([], -1, -1),
    ([{'ret_microaneurysm_re': {'value': 1},
       'ret_microaneurysm_le': {'value': 1}}],
     1, 1),
    ([{'ret_microaneurysm_re': {'value': 0},
       'ret_microaneurysm_le': {'value': 0}}],
     0, 0),
    ([{'ret_microaneurysm_re': {'value': 1}}], 1, -1),
    ([{'ret_microaneurysm_le': {'value': 0}}], -1, 0)
])
def test_build_ret_micro(data, exp_ret_microaneurysm_re, exp_ret_microaneurysm_le):
    result = build_ret_micro(data)
    assert result['ret_microaneurysm_re'] == exp_ret_microaneurysm_re
    assert result['ret_microaneurysm_le'] == exp_ret_microaneurysm_le


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
