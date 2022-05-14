from eye_extractor.laterality import Laterality
from eye_extractor.output.variable import column_from_variable, column_from_variable_binary


def build_cataract_surgery_variables(data):
    curr = data['cataractsurg']
    results = {}
    results.update(build_cataractsurg_ioltype(curr))
    return results


def build_cataractsurg_ioltype(data):
    od = data.get(Laterality.OD, None)
    os = data.get(Laterality.OS, None)
    d = {}
    if od:
        d['cataractsurg_ioltype_re'] = od[0]['model']
        d['cataractsurg_iolpower_re'] = od[0]['power']
        d['cataractsurg_otherlens_re'] = ','.join(x['model'] for x in od[1:])
    elif os:
        d['cataractsurg_ioltype_le'] = os[0]['model']
        d['cataractsurg_iolpower_le'] = os[0]['power']
        d['cataractsurg_otherlens_le'] = ','.join(x['model'] for x in os[1:])
    return d
