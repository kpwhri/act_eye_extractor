import json

import pytest

from eye_extractor.glaucoma.dx import POAG_PAT, NTG_PAT, LTG_PAT, PXG_PAT, PG_PAT, CONGENITAL_PAT, ICE_PAT, NV_PAT, \
    UVEI_PAT, ACG_PAT, STEROID_PAT, TRAUMATIC_PAT, extract_glaucoma_dx, SUSPECT_PAT, OCULAR_HYPERTENSIVE_PAT, \
    CUPPING_PAT
from eye_extractor.output.glaucoma import build_glaucoma_dx


@pytest.mark.parametrize('pat, text, exp', [
    (POAG_PAT, 'POAG', True),
    (POAG_PAT, 'OAG', True),
    (POAG_PAT, 'primary open-angle', True),
    (POAG_PAT, 'open angle', True),
    (NTG_PAT, 'normal pressure', True),
    (NTG_PAT, 'normal tension', True),
    (NTG_PAT, 'ntg', True),
    (NTG_PAT, 'mntg', False),
    (LTG_PAT, 'low pressure', True),
    (LTG_PAT, 'low tension', True),
    (LTG_PAT, 'ltg', True),
    (PXG_PAT, 'capsulare glaucoma', True),
    (PXG_PAT, 'pseudo-exfoliative', True),
    (PXG_PAT, 'pxg', True),
    (PG_PAT, 'pigmentary dispersion', True),
    (PG_PAT, 'pg', True),
    (PG_PAT, 'pigmentary', True),
    (CONGENITAL_PAT, 'congenital', True),
    (CONGENITAL_PAT, 'childhood glaucoma', True),
    (ICE_PAT, 'ice glaucoma', True),
    (ICE_PAT, 'irido corneal endothelial', True),
    (NV_PAT, 'neo-vascular', True),
    (NV_PAT, 'neovascular', True),
    (UVEI_PAT, 'uveitic glaucoma', True),
    (UVEI_PAT, 'uveitis', False),
    (ACG_PAT, 'closed angle glaucoma', True),
    (ACG_PAT, 'narrow angle glaucoma', True),
    (ACG_PAT, 'angle-closure glaucoma', True),
    (ACG_PAT, 'acg', True),
    (STEROID_PAT, 'steroid responder', True),
    (STEROID_PAT, 'steroid induced', True),
    (TRAUMATIC_PAT, 'blunt trauma', True),
    (TRAUMATIC_PAT, 'traumatic', True),
    (SUSPECT_PAT, 'SUSPECT', True),
    (OCULAR_HYPERTENSIVE_PAT, 'OHTN', True),
    (CUPPING_PAT, 'cupping', True),
])
def test_glaucomatype_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) is exp


@pytest.mark.parametrize(
    'text, section_label, section_text,'
    'exp_glaucoma_dx_re, exp_glaucoma_dx_le, exp_glaucoma_dx_unk,'
    'exp_glaucoma_type_re, exp_glaucoma_type_le, exp_glaucoma_type_unk', [
        ('', '', '',
         'UNKNOWN', 'UNKNOWN', 'UNKNOWN',
         'UNKNOWN', 'UNKNOWN', 'UNKNOWN'),
        ('', 'Type of Glaucoma', 'suspect',
         'UNKNOWN', 'UNKNOWN', 'SUSPECT',
         'UNKNOWN', 'UNKNOWN', 'UNKNOWN'),
        ('', 'Type of Glaucoma', 'OHTN',
         'UNKNOWN', 'UNKNOWN', 'OCULAR HYPERTENSIVE',
         'UNKNOWN', 'UNKNOWN', 'UNKNOWN'),
        ('', 'Type of Glaucoma', 'open angle OS',  # fix?
         'UNKNOWN', 'UNKNOWN', 'UNKNOWN',
         'UNKNOWN', 'UNKNOWN', 'UNKNOWN'),
        ('Type of Glaucoma: open angle OS', '', '',
         'UNKNOWN', 'GLAUCOMA', 'UNKNOWN',
         'UNKNOWN', 'POAG', 'UNKNOWN'),
    ])
def test_glaucomatype_extract_build(
        text, section_label, section_text,
        exp_glaucoma_dx_re, exp_glaucoma_dx_le, exp_glaucoma_dx_unk,
        exp_glaucoma_type_re, exp_glaucoma_type_le, exp_glaucoma_type_unk,
):
    pre_json = extract_glaucoma_dx(text, headers={section_label.upper(): section_text})
    post_json = json.loads(json.dumps(pre_json))
    result = build_glaucoma_dx(post_json)
    assert result['glaucoma_dx_re'] == exp_glaucoma_dx_re
    assert result['glaucoma_dx_le'] == exp_glaucoma_dx_le
    assert result['glaucoma_dx_unk'] == exp_glaucoma_dx_unk
    assert result['glaucoma_type_re'] == exp_glaucoma_type_re
    assert result['glaucoma_type_le'] == exp_glaucoma_type_le
    assert result['glaucoma_type_unk'] == exp_glaucoma_type_unk
