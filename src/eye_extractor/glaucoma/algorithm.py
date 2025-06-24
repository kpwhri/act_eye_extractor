from eye_extractor.exam.gonio import extract_gonio
from eye_extractor.glaucoma.cct import extract_cct
from eye_extractor.glaucoma.disc_hemorrhage import extract_disc_hem
from eye_extractor.glaucoma.disc_notch import extract_disc_notch
from eye_extractor.glaucoma.disc_pallor import extract_disc_pallor
from eye_extractor.glaucoma.drops import extract_glaucoma_drops
from eye_extractor.glaucoma.dx import extract_glaucoma_dx
from eye_extractor.glaucoma.exfoliation import extract_exfoliation
from eye_extractor.glaucoma.ppa import extract_ppa
from eye_extractor.glaucoma.preglaucoma import extract_preglaucoma_dx
from eye_extractor.glaucoma.tilted_disc import extract_tilted_disc
from eye_extractor.glaucoma.tx import extract_tx
from eye_extractor.sections.document import Document


def extract_glaucoma(doc: Document):
    data = {}
    data['drops'] = extract_glaucoma_drops(doc)
    data['dx'] = extract_glaucoma_dx(doc)
    data['gonio'] = extract_gonio(doc)
    data['cct'] = extract_cct(doc)
    data['disc_hem'] = extract_disc_hem(doc)
    data['disc_notch'] = extract_disc_notch(doc)
    data['tilted_disc'] = extract_tilted_disc(doc)
    data['ppa'] = extract_ppa(doc)
    data['tx'] = extract_tx(doc)
    data['exfoliation'] = extract_exfoliation(doc)
    data['preglaucoma'] = extract_preglaucoma_dx(doc)
    data['disc_pallor'] = extract_disc_pallor(doc)
    return data
