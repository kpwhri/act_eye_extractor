def build_history(data):
    results = {}
    results.update(build_family_history(data['family']))
    results.update(build_personal_history(data['personal']))
    return results


def build_family_history(data):
    return {
        'famhx_glaucoma': data.get('glaucoma', -1),
        'famhx_amd': data.get('amd', -1),
        'famhx_cataract': data.get('cataracts', -1),
    }


def build_personal_history(data):
    return {
        'perhx_glaucoma': data.get('glaucoma', -1),
        'perhx_amd': data.get('amd', -1),
        'perhx_dr': data.get('dr', -1),
        'perhx_dme': data.get('dme', -1),
        'perhx_cataract': data.get('cataracts', -1),
    }
