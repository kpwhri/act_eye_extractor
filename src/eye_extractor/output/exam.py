def build_exam(data):
    results = {}
    curr = data['exam']
    results.update(build_cup_disc_ratio(curr['cd_ratio']))
    return results


def _update(results, data, key):
    if key in results and results[key]:
        return True
    if key in data and data[key]:
        results[key] = data[key]
        return True
    return False


def build_cup_disc_ratio(data):
    results = {}
    # get undated or most recent date
    curr_list = list(filter(lambda x: x['measurement_date'] is None, data))
    if not curr_list:
        curr_list = sorted(data, key=lambda x: x['measurement_date'], reverse=True)
    cols = ['cupdiscratio_rev', 'cupdiscratio_reh', 'cupdiscratio_lev', 'cupdiscratio_leh']
    for d in curr_list:
        # exit once all values have been filled
        if sum([_update(results, d, col) for col in cols]) == len(cols):
            break

    return results
