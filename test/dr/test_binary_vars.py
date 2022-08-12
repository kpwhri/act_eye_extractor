import pytest

from eye_extractor.dr.binary_vars import get_dr_binary
from eye_extractor.output.dr import (
    build_cottonwspot,
    build_disc_edema,
    build_dr,
    build_hard_exudates,
    build_hemorrhage,
    build_laser_scars,
    build_laser_panrentinal,
    build_ret_micro
)


@pytest.mark.parametrize('text, exp_value, exp_negword', [
    ('No visible diabetic retinopathy this visit', 0, 'no'),
    ('MA: OD normal 6/6', 1, None),
    ('No d/b hemes, CWS or NVE OU', 0, 'no'),
    ('OS:  Numerous hard exudates superior macula', 1, None),
    ('Vessels: good crossings; no venous beading;', 0, 'no'),
    ('The optic disc edema has changed location', 1, None),
    ('OU  VESSELS: Normal pattern without exudates, hemorrhage, plaques, ', 0, 'without'),
    ('ASSESSMENT : Resolving vitreous/preretinal hemorrhage  No retinal tears', 1, None),
    ('OU   No Microaneurysms/hemes, cotton-wool spots, exudates, IRMA, Venous beading, NVE', 0, 'no'),
    ('OD: area of IRMA just nasal to disc,', 1, None),
    ('also has small area of IRMA right eye', 1, None),
    ('increased IRF - Avastin OS', 1, None),
    ('PERIPHERAL RETINA: Laser scars OD, Laser scars versus cobblestone OS', 1, None),
    pytest.param('Central macular thickness: 234 um, No SRF, few focal scars', 1, None,
                 marks=pytest.mark.skip(reason="Unhandled instance of negation.")),
    ('Dilated OD M/N- c/d 0.5 OU, macula clear, laser scars around atrophic hole', 1, None),
    ('Hx of BRVO OD with PRP', 1, None),
    ('Corneal neovascularization, unspecified.', 1, None),
    ('IRIS: Normal Appearance, neg Rubeosis, OU', 0, 'neg'),
    ('Mild nonproliferative diabetic retinopathy (362.04)', 1, None),
    ('PI OS NO PDR active', 0, 'no'),
    ('Plan for surgery: Pars Plana Vitrectomy with Membrane Peel left eye.', 1, None),
    ('Patient presents with: Diabetic macular edema E11.311', 1, None),
    ('No CSME', 0, 'no'),
    ('OD: erm, CMT 291; OS: erm, CMT 280 No change', 1, None),
    ('Intravitreal injection of Avastin (Bevacizumab) of your left eye', 1, None),
    ('TRIAMCINOLONE ACETONIDE 0.1 % TOPICAL CREAM', 1, None)
])
def test_get_dr_binary(text, exp_value, exp_negword):
    data = get_dr_binary(text)
    variable = list(data[0].values())[0]

    assert len(data) > 0
    assert variable['value'] == exp_value
    assert variable['negated'] == exp_negword


@pytest.mark.parametrize('data, exp_diab_retinop_yesno_re, exp_diab_retinop_yesno_le, exp_diab_retinop_yesno_unk', [
    ([], -1, -1, -1),
    ([{'diab_retinop_yesno_re': {'value': 1},
       'diab_retinop_yesno_le': {'value': 1}}],
     1, 1, -1),
    ([{'diab_retinop_yesno_re': {'value': 0},
       'diab_retinop_yesno_le': {'value': 0}}],
     0, 0, -1),
    ([{'diab_retinop_yesno_re': {'value': 1}}], 1, -1, -1),
    ([{'diab_retinop_yesno_le': {'value': 0}}], -1, 0, -1),
    ([{'diab_retinop_yesno_unk': {'value': 1}}], -1, -1, 1),
    ([{'diab_retinop_yesno_unk': {'value': 0}}], -1, -1, 0)
])
def test_build_dr(data, exp_diab_retinop_yesno_re, exp_diab_retinop_yesno_le, exp_diab_retinop_yesno_unk):
    result = build_dr(data)
    assert result['diab_retinop_yesno_re'] == exp_diab_retinop_yesno_re
    assert result['diab_retinop_yesno_le'] == exp_diab_retinop_yesno_le
    assert result['diab_retinop_yesno_unk'] == exp_diab_retinop_yesno_unk


@pytest.mark.parametrize('data, exp_ret_microaneurysm_re, exp_ret_microaneurysm_le, exp_ret_microaneurysm_unk', [
    ([], -1, -1, -1),
    ([{'ret_microaneurysm_re': {'value': 1},
       'ret_microaneurysm_le': {'value': 1}}],
     1, 1, -1),
    ([{'ret_microaneurysm_re': {'value': 0},
       'ret_microaneurysm_le': {'value': 0}}],
     0, 0, -1),
    ([{'ret_microaneurysm_re': {'value': 1}}], 1, -1, -1),
    ([{'ret_microaneurysm_le': {'value': 0}}], -1, 0, -1),
    ([{'ret_microaneurysm_unk': {'value': 1}}], -1, -1, 1),
    ([{'ret_microaneurysm_unk': {'value': 0}}], -1, -1, 0)
])
def test_build_ret_micro(data, exp_ret_microaneurysm_re, exp_ret_microaneurysm_le, exp_ret_microaneurysm_unk):
    result = build_ret_micro(data)
    assert result['ret_microaneurysm_re'] == exp_ret_microaneurysm_re
    assert result['ret_microaneurysm_le'] == exp_ret_microaneurysm_le
    assert result['ret_microaneurysm_unk'] == exp_ret_microaneurysm_unk


@pytest.mark.parametrize('data, exp_cottonwspot_re, exp_cottonwspot_le, exp_cottonwspot_unk', [
    ([], -1, -1, -1),
    ([{'cottonwspot_re': {'value': 1},
       'cottonwspot_le': {'value': 1}}],
     1, 1, -1),
    ([{'cottonwspot_re': {'value': 0},
       'cottonwspot_le': {'value': 0}}],
     0, 0, -1),
    ([{'cottonwspot_re': {'value': 1}}], 1, -1, -1),
    ([{'cottonwspot_le': {'value': 0}}], -1, 0, -1),
    ([{'cottonwspot_unk': {'value': 1}}], -1, -1, 1),
    ([{'cottonwspot_unk': {'value': 0}}], -1, -1, 0)
])
def test_build_cottonwspot(data, exp_cottonwspot_re, exp_cottonwspot_le, exp_cottonwspot_unk):
    result = build_cottonwspot(data)
    assert result['cottonwspot_re'] == exp_cottonwspot_re
    assert result['cottonwspot_le'] == exp_cottonwspot_le
    assert result['cottonwspot_unk'] == exp_cottonwspot_unk


@pytest.mark.parametrize('data, exp_hardexudates_re, exp_hardexudates_le, exp_hardexudates_unk', [
    ([], -1, -1, -1),
    ([{'hardexudates_re': {'value': 1},
       'hardexudates_le': {'value': 1}}],
     1, 1, -1),
    ([{'hardexudates_re': {'value': 0},
       'hardexudates_le': {'value': 0}}],
     0, 0, -1),
    ([{'hardexudates_re': {'value': 1}}], 1, -1, -1),
    ([{'hardexudates_le': {'value': 0}}], -1, 0, -1),
    ([{'hardexudates_unk': {'value': 1}}], -1, -1, 1),
    ([{'hardexudates_unk': {'value': 0}}], -1, -1, 0)
])
def test_build_hard_exudates(data, exp_hardexudates_re, exp_hardexudates_le, exp_hardexudates_unk):
    result = build_hard_exudates(data)
    assert result['hardexudates_re'] == exp_hardexudates_re
    assert result['hardexudates_le'] == exp_hardexudates_le
    assert result['hardexudates_unk'] == exp_hardexudates_unk


@pytest.mark.parametrize('data, exp_disc_edema_dr_re, exp_disc_edema_dr_le, exp_disc_edema_dr_unk', [
    ([], -1, -1, -1),
    ([{'disc_edema_dr_re': {'value': 1},
       'disc_edema_dr_le': {'value': 1}}],
     1, 1, -1),
    ([{'disc_edema_dr_re': {'value': 0},
       'disc_edema_dr_le': {'value': 0}}],
     0, 0, -1),
    ([{'disc_edema_dr_re': {'value': 1}}], 1, -1, -1),
    ([{'disc_edema_dr_le': {'value': 0}}], -1, 0, -1),
    ([{'disc_edema_dr_unk': {'value': 1}}], -1, -1, 1),
    ([{'disc_edema_dr_unk': {'value': 0}}], -1, -1, 0)
])
def test_build_disc_edema(data, exp_disc_edema_dr_re, exp_disc_edema_dr_le, exp_disc_edema_dr_unk):
    result = build_disc_edema(data)
    assert result['disc_edema_dr_re'] == exp_disc_edema_dr_re
    assert result['disc_edema_dr_le'] == exp_disc_edema_dr_le
    assert result['disc_edema_dr_unk'] == exp_disc_edema_dr_unk


@pytest.mark.parametrize('data, exp_hemorrhage_dr_re, exp_hemorrhage_dr_le, exp_hemorrhage_dr_unk', [
    ([], -1, -1, -1),
    ([{'hemorrhage_dr_re': {'value': 1},
       'hemorrhage_dr_le': {'value': 1}}],
     1, 1, -1),
    ([{'hemorrhage_dr_re': {'value': 0},
       'hemorrhage_dr_le': {'value': 0}}],
     0, 0, -1),
    ([{'hemorrhage_dr_re': {'value': 1}}], 1, -1, -1),
    ([{'hemorrhage_dr_le': {'value': 0}}], -1, 0, -1),
    ([{'hemorrhage_dr_unk': {'value': 1}}], -1, -1, 1),
    ([{'hemorrhage_dr_unk': {'value': 0}}], -1, -1, 0)
])
def test_build_hemorrhage(data, exp_hemorrhage_dr_re, exp_hemorrhage_dr_le, exp_hemorrhage_dr_unk):
    result = build_hemorrhage(data)
    assert result['hemorrhage_dr_re'] == exp_hemorrhage_dr_re
    assert result['hemorrhage_dr_le'] == exp_hemorrhage_dr_le
    assert result['hemorrhage_dr_unk'] == exp_hemorrhage_dr_unk


@pytest.mark.parametrize('data, exp_dr_laser_scars_re, exp_dr_laser_scars_le, exp_dr_laser_scars_unk', [
    ([], -1, -1, -1),
    ([{'dr_laser_scars_re': {'value': 1},
       'dr_laser_scars_le': {'value': 1}}],
     1, 1, -1),
    ([{'dr_laser_scars_re': {'value': 0},
       'dr_laser_scars_le': {'value': 0}}],
     0, 0, -1),
    ([{'dr_laser_scars_re': {'value': 1}}], 1, -1, -1),
    ([{'dr_laser_scars_le': {'value': 0}}], -1, 0, -1),
    ([{'dr_laser_scars_unk': {'value': 1}}], -1, -1, 1),
    ([{'dr_laser_scars_unk': {'value': 0}}], -1, -1, 0)
])
def test_build_laser_scars(data, exp_dr_laser_scars_re, exp_dr_laser_scars_le, exp_dr_laser_scars_unk):
    result = build_laser_scars(data)
    assert result['dr_laser_scars_re'] == exp_dr_laser_scars_re
    assert result['dr_laser_scars_le'] == exp_dr_laser_scars_le
    assert result['dr_laser_scars_unk'] == exp_dr_laser_scars_unk


@pytest.mark.parametrize('data, exp_laserpanret_photocoag_re, exp_laserpanret_photocoag_le, '
                         'exp_laserpanret_photocoag_unk', [
                             ([], -1, -1, -1),
                             ([{'laserpanret_photocoag_re': {'value': 1},
                                'laserpanret_photocoag_le': {'value': 1}}],
                              1, 1, -1),
                             ([{'laserpanret_photocoag_re': {'value': 0},
                                'laserpanret_photocoag_le': {'value': 0}}],
                              0, 0, -1),
                             ([{'laserpanret_photocoag_re': {'value': 1}}], 1, -1, -1),
                             ([{'laserpanret_photocoag_le': {'value': 0}}], -1, 0, -1),
                             ([{'laserpanret_photocoag_unk': {'value': 1}}], -1, -1, 1),
                             ([{'laserpanret_photocoag_unk': {'value': 0}}], -1, -1, 0)
                         ])
def test_build_laser_panretinal(data,
                                exp_laserpanret_photocoag_re,
                                exp_laserpanret_photocoag_le,
                                exp_laserpanret_photocoag_unk):
    result = build_laser_panrentinal(data)
    assert result['laserpanret_photocoag_re'] == exp_laserpanret_photocoag_re
    assert result['laserpanret_photocoag_le'] == exp_laserpanret_photocoag_le
    assert result['laserpanret_photocoag_unk'] == exp_laserpanret_photocoag_unk
