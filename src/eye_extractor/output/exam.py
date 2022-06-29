def build_exam(data):
    results = {}
    curr = data['exam']
    results.update(build_cup_disc_ratio(curr))
    return results


def build_cup_disc_ratio(data):
    results = {}
    results['cupdiscratio_rev'] = data['cupdiscratio_rev']
    results['cupdiscratio_reh'] = data['cupdiscratio_reh']
    results['cupdiscratio_lev'] = data['cupdiscratio_lev']
    results['cupdiscratio_leh'] = data['cupdiscratio_leh']
    return results
