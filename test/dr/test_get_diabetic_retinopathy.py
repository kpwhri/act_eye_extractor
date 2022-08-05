import pytest

from eye_extractor.dr.diabetic_retinopathy import HemorrhageType, get_dr_binary, get_hemorrhage_type


@pytest.mark.parametrize('text, exp_value, exp_negword', [
    ('MACULA: No visible diabetic retinopathy this visit', 0, 'no'),
    ('HRT II linear C/D 0.55 / 0.73 on 10/27/2077 MA: OD normal 6/6', 1, None),
    ('hemorrhage in all clock hours to ora OU  No d/b hemes, CWS or NVE OU', 0, 'no'),
    ('OS:  Numerous hard exudates superior macula', 1, None),
    ('Vessels: good crossings; no venous beading;', 0, 'no'),
    ('The optic disc edema has changed location', 1, None),
    ('OU  VESSELS: Normal pattern without exudates, hemorrhage, plaques, ', 0, 'without'),
    ('ASSESSMENT : Resolving vitreous/preretinal hemorrhage  No retinal tears', 1, None),
    ('OU   No Microaneurysms/hemes, cotton-wool spots, exudates, IRMA, Venous beading, NVE', 0, 'no'),
    ('OD: area of IRMA just nasal to disc,', 1, None),
    ('also has small area of IRMA right eye', 1, None),
    ('Oct macula: 7/4/1776 CMT OS:222, increased IRF - Avastin OS', 1, None),
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
    print(variable['term'])

    assert len(data) > 0
    assert variable['value'] == exp_value
    assert variable['negated'] == exp_negword


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

# TODO: def test_get_fluid

# TODO: def test_get_laser_scar_type

# TODO: def test_get_nvd

# TODO: def test_get_nve

# TODO: def test_get_dr_type

# TODO: def test_get_npdr

# TODO: def test_get_pdr

# TODO: def test_get_dr_tx

# TODO: def test_get_edema_tx

# TODO: def test_get_edema_antivegf


