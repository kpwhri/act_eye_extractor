from eye_extractor.glaucoma.drops import GenericDrop


def build_glaucoma_drops(data):
    results = {f'glaucoma_rx_{x.name.lower()}': -1 for x in GenericDrop if x.name != 'UNKNOWN'}
    for record in data:
        for key, value in record.items():
            results[key] = value['value']
    return results


def build_glaucoma(data):
    results = {}
    curr = data['glaucoma']
    results.update(build_glaucoma_drops(curr['drops']))
    return results
