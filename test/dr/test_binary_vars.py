import pytest

from eye_extractor.dr.binary_vars import get_dr_binary
from eye_extractor.output.dr import (
    build_cottonwspot,
    build_disc_edema,
    build_dr,
    build_edema,
    build_hard_exudates,
    build_hemorrhage,
    build_laser_scars,
    build_laser_panrentinal,
    build_neovasc,
    build_nva,
    build_nvd,
    build_nve,
    build_nvi,
    build_oct_cme,
    build_ret_micro,
    build_sig_edema
)


@pytest.mark.parametrize('text, exp_value, exp_negword', [
    ('No visible diabetic retinopathy this visit', 0, 'no'),
    ('MA: OD normal 6/6', 1, None),
    ('No d/b hemes, CWS or NVE OU', 0, 'no'),
    ('OS:  Numerous hard exudates superior macula', 1, None),
    ('The optic disc edema has changed location', 1, None),
    ('OU  VESSELS: Normal pattern without exudates, hemorrhage, plaques, ', 0, 'without'),
    ('ASSESSMENT : Resolving vitreous/preretinal hemorrhage  No retinal tears', 1, None),
    ('OU   No Microaneurysms/hemes, cotton-wool spots, exudates, IRMA, Venous beading, NVE', 0, 'no'),
    ('PERIPHERAL RETINA: Laser scars OD, Laser scars versus cobblestone OS', 1, None),
    pytest.param('Central macular thickness: 234 um, No SRF, few focal scars', 1, None,
                 marks=pytest.mark.skip(reason="Unhandled instance of negation.")),
    ('Dilated OD M/N- c/d 0.5 OU, macula clear, laser scars around atrophic hole', 1, None),
    ('Hx of BRVO OD with PRP', 1, None),
    ('Corneal neovascularization, unspecified.', 1, None),
    ('no NVD OD', 0, 'no'),
    ('Normal blood cells without NVD', 0, 'without'),
    ('No d/b hemes, CWS or NVE OU', 0, 'no'),
    ('without NVD, NVE', 0, 'without'),
    ('no NVE Disc 0.45', 0, 'no'),
    ('Mild nonproliferative diabetic retinopathy (362.04)', 1, None),
    ('Plan for surgery: Pars Plana Vitrectomy with Membrane Peel left eye.', 1, None),
    ('Patient presents with: Diabetic macular edema E11.311', 1, None),
    ('No CSME', 0, 'no'),
    ('OD: erm, CMT 291; OS: erm, CMT 280 No change', 1, None),
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


@pytest.mark.parametrize('data, exp_neovasc_yesno_re, exp_neovasc_yesno_le, exp_neovasc_yesno_unk', [
    ([], -1, -1, -1),
    ([{'neovasc_yesno_re': {'value': 1},
       'neovasc_yesno_le': {'value': 1}}],
     1, 1, -1),
    ([{'neovasc_yesno_re': {'value': 0},
       'neovasc_yesno_le': {'value': 0}}],
     0, 0, -1),
    ([{'neovasc_yesno_re': {'value': 1}}], 1, -1, -1),
    ([{'neovasc_yesno_le': {'value': 0}}], -1, 0, -1),
    ([{'neovasc_yesno_unk': {'value': 1}}], -1, -1, 1),
    ([{'neovasc_yesno_unk': {'value': 0}}], -1, -1, 0)
])
def test_build_neovasc(data, exp_neovasc_yesno_re, exp_neovasc_yesno_le, exp_neovasc_yesno_unk):
    result = build_neovasc(data)
    assert result['neovasc_yesno_re'] == exp_neovasc_yesno_re
    assert result['neovasc_yesno_le'] == exp_neovasc_yesno_le
    assert result['neovasc_yesno_unk'] == exp_neovasc_yesno_unk


@pytest.mark.parametrize('data, exp_nva_yesno_re, exp_nva_yesno_le, exp_nva_yesno_unk', [
    ([], -1, -1, -1),
    ([{'nva_yesno_re': {'value': 1},
       'nva_yesno_le': {'value': 1}}],
     1, 1, -1),
    ([{'nva_yesno_re': {'value': 0},
       'nva_yesno_le': {'value': 0}}],
     0, 0, -1),
    ([{'nva_yesno_re': {'value': 1}}], 1, -1, -1),
    ([{'nva_yesno_le': {'value': 0}}], -1, 0, -1),
    ([{'nva_yesno_unk': {'value': 1}}], -1, -1, 1),
    ([{'nva_yesno_unk': {'value': 0}}], -1, -1, 0)
])
def test_build_nva(data, exp_nva_yesno_re, exp_nva_yesno_le, exp_nva_yesno_unk):
    result = build_nva(data)
    assert result['nva_yesno_re'] == exp_nva_yesno_re
    assert result['nva_yesno_le'] == exp_nva_yesno_le
    assert result['nva_yesno_unk'] == exp_nva_yesno_unk


@pytest.mark.parametrize('data, exp_nvi_yesno_re, exp_nvi_yesno_le, exp_nvi_yesno_unk', [
    ([], -1, -1, -1),
    ([{'nvi_yesno_re': {'value': 1},
       'nvi_yesno_le': {'value': 1}}],
     1, 1, -1),
    ([{'nvi_yesno_re': {'value': 0},
       'nvi_yesno_le': {'value': 0}}],
     0, 0, -1),
    ([{'nvi_yesno_re': {'value': 1}}], 1, -1, -1),
    ([{'nvi_yesno_le': {'value': 0}}], -1, 0, -1),
    ([{'nvi_yesno_unk': {'value': 1}}], -1, -1, 1),
    ([{'nvi_yesno_unk': {'value': 0}}], -1, -1, 0)
])
def test_build_nvi(data, exp_nvi_yesno_re, exp_nvi_yesno_le, exp_nvi_yesno_unk):
    result = build_nvi(data)
    assert result['nvi_yesno_re'] == exp_nvi_yesno_re
    assert result['nvi_yesno_le'] == exp_nvi_yesno_le
    assert result['nvi_yesno_unk'] == exp_nvi_yesno_unk


@pytest.mark.parametrize('data, exp_nvd_yesno_re, exp_nvd_yesno_le, exp_nvd_yesno_unk', [
    ([], -1, -1, -1),
    ([{'nvd_yesno_re': {'value': 1},
       'nvd_yesno_le': {'value': 1}}],
     1, 1, -1),
    ([{'nvd_yesno_re': {'value': 0},
       'nvd_yesno_le': {'value': 0}}],
     0, 0, -1),
    ([{'nvd_yesno_re': {'value': 1}}], 1, -1, -1),
    ([{'nvd_yesno_le': {'value': 0}}], -1, 0, -1),
    ([{'nvd_yesno_unk': {'value': 1}}], -1, -1, 1),
    ([{'nvd_yesno_unk': {'value': 0}}], -1, -1, 0)
])
def test_build_nvd(data, exp_nvd_yesno_re, exp_nvd_yesno_le, exp_nvd_yesno_unk):
    result = build_nvd(data)
    assert result['nvd_yesno_re'] == exp_nvd_yesno_re
    assert result['nvd_yesno_le'] == exp_nvd_yesno_le
    assert result['nvd_yesno_unk'] == exp_nvd_yesno_unk


@pytest.mark.parametrize('data, exp_nve_yesno_re, exp_nve_yesno_le, exp_nve_yesno_unk', [
    ([], -1, -1, -1),
    ([{'nve_yesno_re': {'value': 1},
       'nve_yesno_le': {'value': 1}}],
     1, 1, -1),
    ([{'nve_yesno_re': {'value': 0},
       'nve_yesno_le': {'value': 0}}],
     0, 0, -1),
    ([{'nve_yesno_re': {'value': 1}}], 1, -1, -1),
    ([{'nve_yesno_le': {'value': 0}}], -1, 0, -1),
    ([{'nve_yesno_unk': {'value': 1}}], -1, -1, 1),
    ([{'nve_yesno_unk': {'value': 0}}], -1, -1, 0)
])
def test_build_nve(data, exp_nve_yesno_re, exp_nve_yesno_le, exp_nve_yesno_unk):
    result = build_nve(data)
    assert result['nve_yesno_re'] == exp_nve_yesno_re
    assert result['nve_yesno_le'] == exp_nve_yesno_le
    assert result['nve_yesno_unk'] == exp_nve_yesno_unk


@pytest.mark.parametrize('data, exp_dmacedema_yesno_re, exp_dmacedema_yesno_le, exp_dmacedema_yesno_unk', [
    ([], -1, -1, -1),
    ([{'dmacedema_yesno_re': {'value': 1},
       'dmacedema_yesno_le': {'value': 1}}],
     1, 1, -1),
    ([{'dmacedema_yesno_re': {'value': 0},
       'dmacedema_yesno_le': {'value': 0}}],
     0, 0, -1),
    ([{'dmacedema_yesno_re': {'value': 1}}], 1, -1, -1),
    ([{'dmacedema_yesno_le': {'value': 0}}], -1, 0, -1),
    ([{'dmacedema_yesno_unk': {'value': 1}}], -1, -1, 1),
    ([{'dmacedema_yesno_unk': {'value': 0}}], -1, -1, 0)
])
def test_build_edema(data, exp_dmacedema_yesno_re, exp_dmacedema_yesno_le, exp_dmacedema_yesno_unk):
    result = build_edema(data)
    assert result['dmacedema_yesno_re'] == exp_dmacedema_yesno_re
    assert result['dmacedema_yesno_le'] == exp_dmacedema_yesno_le
    assert result['dmacedema_yesno_unk'] == exp_dmacedema_yesno_unk


@pytest.mark.parametrize('data, exp_dmacedema_clinsignif_re, exp_dmacedema_clinsignif_le, '
                         'exp_dmacedema_clinsignif_unk', [
                             ([], -1, -1, -1),
                             ([{'dmacedema_clinsignif_re': {'value': 1},
                                'dmacedema_clinsignif_le': {'value': 1}}],
                              1, 1, -1),
                             ([{'dmacedema_clinsignif_re': {'value': 0},
                                'dmacedema_clinsignif_le': {'value': 0}}],
                              0, 0, -1),
                             ([{'dmacedema_clinsignif_re': {'value': 1}}], 1, -1, -1),
                             ([{'dmacedema_clinsignif_le': {'value': 0}}], -1, 0, -1),
                             ([{'dmacedema_clinsignif_unk': {'value': 1}}], -1, -1, 1),
                             ([{'dmacedema_clinsignif_unk': {'value': 0}}], -1, -1, 0)
                         ])
def test_build_sig_edema(data, exp_dmacedema_clinsignif_re, exp_dmacedema_clinsignif_le, exp_dmacedema_clinsignif_unk):
    result = build_sig_edema(data)
    assert result['dmacedema_clinsignif_re'] == exp_dmacedema_clinsignif_re
    assert result['dmacedema_clinsignif_le'] == exp_dmacedema_clinsignif_le
    assert result['dmacedema_clinsignif_unk'] == exp_dmacedema_clinsignif_unk


@pytest.mark.parametrize('data, exp_oct_centralmac_re, exp_oct_centralmac_le, exp_oct_centralmac_unk', [
    ([], -1, -1, -1),
    ([{'oct_centralmac_re': {'value': 1},
       'oct_centralmac_le': {'value': 1}}],
     1, 1, -1),
    ([{'oct_centralmac_re': {'value': 0},
       'oct_centralmac_le': {'value': 0}}],
     0, 0, -1),
    ([{'oct_centralmac_re': {'value': 1}}], 1, -1, -1),
    ([{'oct_centralmac_le': {'value': 0}}], -1, 0, -1),
    ([{'oct_centralmac_unk': {'value': 1}}], -1, -1, 1),
    ([{'oct_centralmac_unk': {'value': 0}}], -1, -1, 0)
])
def test_build_oct_cme(data, exp_oct_centralmac_re, exp_oct_centralmac_le, exp_oct_centralmac_unk):
    result = build_oct_cme(data)
    assert result['oct_centralmac_re'] == exp_oct_centralmac_re
    assert result['oct_centralmac_le'] == exp_oct_centralmac_le
    assert result['oct_centralmac_unk'] == exp_oct_centralmac_unk
