import pytest

from eye_extractor.dr.diabetic_retinopathy import get_dr


@pytest.mark.parametrize('text, exp_value, exp_negword', [
    ('MACULA: No visible diabetic retinopathy this visit', 0, 'no'),
    ('HRT II linear C/D 0.55 / 0.73 on 10/17/2011 MA: OD normal 6/6', 1, None),
    ('hemorrhage in all clock hours to ora OU  No d/b hemes, CWS or NVE OU', 0, 'no'),
    ('OS:  Numerous hard exudates superior macula', 1, None),
    ('Vessels: good crossings; no venous beading;', 0, 'no'),
    ('The optic disc edema has changed location', 1, None),
    ('OU  VESSELS: Normal pattern without exudates, hemorrhage, plaques, ', 0, 'without'),
    ('ASSESSMENT : Resolving vitreous/preretinal hemorrhage  No retinal tears', 1, None),
    ('OU   No Microaneurysms/hemes, cotton-wool spots, exudates, IRMA, Venous beading, NVE', 0, 'no'),
    ('Oct macula: 7/12/2013 CMT OS:222, increased IRF - Avastin OS', 1, None),
    ('PERIPHERAL RETINA: Laser scars OD, Laser scars versus cobblestone OS', 1, None),
    ('Central macular thickness: 234 um, No SRF, few focal scars', 1, None),
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
def test_dr_value(text, exp_value, exp_negword):
    data = get_dr(text)
    variable = list(data[0].values())[0]

    assert variable['value'] == exp_value
    assert variable['negated'] == exp_negword



