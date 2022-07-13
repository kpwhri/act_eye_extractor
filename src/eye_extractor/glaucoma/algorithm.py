from eye_extractor.glaucoma.drops import extract_glaucoma_drops


def extract_glaucoma(text, *, headers=None, lateralities=None):
    data = {}
    data['drops'] = extract_glaucoma_drops(text, headers=headers, lateralities=lateralities)
    return data
