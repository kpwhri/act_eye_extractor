from eye_extractor.exam.gonio import extract_gonio
from eye_extractor.glaucoma.cct import extract_cct
from eye_extractor.glaucoma.disc_hemorrhage import extract_disc_hem
from eye_extractor.glaucoma.disc_notch import extract_disc_notch
from eye_extractor.glaucoma.drops import extract_glaucoma_drops
from eye_extractor.glaucoma.dx import extract_glaucoma_dx
from eye_extractor.glaucoma.exfoliation import extract_exfoliation
from eye_extractor.glaucoma.ppa import extract_ppa
from eye_extractor.glaucoma.tilted_disc import extract_tilted_disc
from eye_extractor.glaucoma.tx import extract_tx


def extract_glaucoma(text, *, headers=None, lateralities=None):
    data = {}
    data['drops'] = extract_glaucoma_drops(text, headers=headers, lateralities=lateralities)
    data['dx'] = extract_glaucoma_dx(text, headers=headers, lateralities=lateralities)
    data['gonio'] = extract_gonio(text, headers=headers, lateralities=lateralities)
    data['cct'] = extract_cct(text, headers=headers, lateralities=lateralities)
    data['disc_hem'] = extract_disc_hem(text, headers=headers, lateralities=lateralities)
    data['disc_notch'] = extract_disc_notch(text, headers=headers, lateralities=lateralities)
    data['tilted_disc'] = extract_tilted_disc(text, headers=headers, lateralities=lateralities)
    data['ppa'] = extract_ppa(text, headers=headers, lateralities=lateralities)
    data['tx'] = extract_tx(text, headers=headers, lateralities=lateralities)
    data['exfoliation'] = extract_exfoliation(text, headers=headers, lateralities=lateralities)
    return data
