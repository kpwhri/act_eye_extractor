import pytest

from eye_extractor.glaucoma.dx import POAG_PAT, NTG_PAT, LTG_PAT, PXG_PAT, PG_PAT, CONGENITAL_PAT, ICE_PAT, NV_PAT, \
    UVEI_PAT, ACG_PAT, STEROID_PAT, TRAUMATIC_PAT


@pytest.mark.parametrize('pat, text, exp', [
    (POAG_PAT, 'POAG', True),
    (POAG_PAT, 'OAG', True),
    (POAG_PAT, 'primary open-angle', True),
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
    (ACG_PAT, 'angle-closure glaucoma', True),
    (ACG_PAT, 'acg', True),
    (STEROID_PAT, 'steroid responder', True),
    (STEROID_PAT, 'steroid induced', True),
    (TRAUMATIC_PAT, 'blunt trauma', True),
    (TRAUMATIC_PAT, 'traumatic', True),
])
def test_cataract_type_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) is exp
