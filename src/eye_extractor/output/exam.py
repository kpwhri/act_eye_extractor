def build_exam(data):
    results = {}
    curr = data['exam']
    results.update(build_cup_disc_ratio(curr['cd_ratio']))
    results.update(build_rnfl(curr['rnfl'], data['note_date']))
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
    curr_list = list(filter(lambda x: x.get('measurement_date', None) is None, data))
    if not curr_list:
        curr_list = sorted(data, key=lambda x: x['measurement_date'], reverse=True)
    cols = ['cupdiscratio_rev', 'cupdiscratio_reh', 'cupdiscratio_lev', 'cupdiscratio_leh']
    for d in curr_list:
        # exit once all values have been filled
        if sum([_update(results, d, col) for col in cols]) == len(cols):
            break

    return results


def build_rnfl(data, note_date):
    """
    Look for both RNFL values and thinning. Once enough values have been found (or any thinning), skip.
    Sort by date to get most recent values first (RNFL can be presented as a table).
    :param data:
    :param note_date:
    :return:
    """
    results = {}
    found_values_counter = 0
    skip_values = False
    found_thinning = False
    # start with most recent values
    for d in sorted([d | {'date': d['date'] or note_date} for d in data], key=lambda x: x['date'], reverse=True):
        if found_values_counter > 4:
            skip_values = True
        for k, v in d.items():
            if 'thinning' in k:
                if found_thinning:
                    continue
                elif v is not -1:
                    found_thinning = True
            elif skip_values:
                continue
            else:
                if found_values_counter != -1:
                    found_values_counter += 1

            if results.get(k, -1) == -1:
                results[k] = v
        if found_thinning and skip_values:
            return results

    return results
