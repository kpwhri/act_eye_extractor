from eye_extractor.glaucoma.drops import extract_glaucoma_drops
from eye_extractor.glaucoma.dx import extract_glaucoma_dx


def extract_glaucoma(text, *, headers=None, lateralities=None):
    data = {}
    data['drops'] = extract_glaucoma_drops(text, headers=headers, lateralities=lateralities)
    data['dx'] = extract_glaucoma_dx(text, headers=headers, lateralities=lateralities)
    return data
