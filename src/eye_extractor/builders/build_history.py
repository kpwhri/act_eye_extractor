from eye_extractor.common.safeget import safeget


def build_history(data):
    results = {}
    if not data.get('history', None):
        return results
    results.update(build_family_history(safeget(data, 'history', 'family')))
    results.update(build_personal_history(safeget(data, 'history', 'personal')))
    return results


def build_family_history(data):
    if not data:
        return {}
    return {
        'famhx_glaucoma': data.get('glaucoma', -1),
        'famhx_amd': data.get('amd', -1),
        'famhx_cataract': data.get('cataracts', -1),
    }


def build_personal_history(data):
    if not data:
        return {}
    return {
        'perhx_glaucoma': data.get('glaucoma', -1),
        'perhx_amd': data.get('amd', -1),
        'perhx_dr': data.get('dr', -1),
        'perhx_dme': data.get('dme', -1),
        'perhx_cataract': data.get('cataracts', -1),
    }
