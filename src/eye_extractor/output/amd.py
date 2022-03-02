from eye_extractor.output.laterality import laterality_from_int
from eye_extractor.laterality import Laterality
from eye_extractor.output.variable import column_from_variable


def build_amd_variables(data):
    curr = data['amd']
    results = {}
    results.update(get_amd(curr))
    results.update(get_drusen(curr))
    results.update(get_subretinal_hemorrhage(curr))
    results.update(get_pigmentary_changes(curr))
    return results


def get_amd(data):
    results = {
        'amd_re': 8,
        'amd_le': 8,
    }
    for item in data:
        laterality = laterality_from_int(item['laterality'])
        if {Laterality.OS, Laterality.OU} & {laterality}:
            results['amd_le'] = min(1, results['amd_le'])
        elif laterality:  # any mention
            results['amd_le'] = min(0, results['amd_le'])
        if {Laterality.OD, Laterality.OU} & {laterality}:
            results['amd_re'] = min(1, results['amd_re'])
        elif laterality:  # any mention
            results['amd_re'] = min(0, results['amd_re'])
    return results


def get_drusen(data):
    results = {}
    for k, v in data.items():
        results[k] = v['label'].upper()
    return results


def get_subretinal_hemorrhage(data):
    return column_from_variable({
        'subretinal_hem_re': -1,
        'subretinal_hem_le': -1,
    }, data)


def get_pigmentary_changes(data):
    return column_from_variable({
        'pigmentchanges_re': -1,
        'pigmentchanges_le': -1,
    }, data)
