from eye_extractor.laterality import Laterality


def build_cataract_surgery_variables(data):
    curr = data['cataractsurg']
    results = {}
    if not curr:
        return results
    lat = curr['cataractsurg_lat']
    results['cataractsurg_yesno'] = 'RE' if lat == Laterality.OD else 'LE' if lat == Laterality.OS else '-1'
    results.update(build_cataractsurg_ioltype(curr))
    results.update(build_cataractsurg_date(curr, lat))
    results.update(build_cataractsurg_complications(curr, lat))
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


def build_cataractsurg_date(data, lat):
    date = data.get('cataractsurg_dt')
    if lat == Laterality.OD:
        return {'cataractsurg_dt_re': date}
    elif lat == Laterality.OS:
        return {'cataractsurg_dt_le': date}
    elif lat == Laterality.OU:
        return {'cataractsurg_dt_le': date, 'cataractsurg_dt_re': date}
    else:
        return {'cataractsurg_dt_unk': date}


def build_cataractsurg_complications(data, lat):
    complications = data.get('catsurg_comp', -1)
    if lat == Laterality.OD:
        return {'catsurg_comp_yesno_re': complications['value'],
                'catsurg_comp_describe_re': complications.get('complication', '')}
    elif lat == Laterality.OS:
        return {'catsurg_comp_yesno_le': complications['value'],
                'catsurg_comp_describe_le': complications.get('complication', '')}
    elif lat == Laterality.OU:
        return {'catsurg_comp_yesno_le': complications['value'],
                'catsurg_comp_yesno_re': complications['value'],
                'catsurg_comp_describe_le': complications.get('complication', ''),
                'catsurg_comp_describe_re': complications.get('complication', ''),
                }
    else:
        return {'catsurg_comp_yesno_le': complications['value'],
                'catsurg_comp_describe_le': complications.get('complication', ''),
                }
