from eye_extractor.output.variable import column_from_variable


def build_uveitis_variables(data):
    curr = data['uveitis']
    results = {}
    results.update(build_uveitis(curr))
    return results


def build_uveitis(data):
    return column_from_variable({
        'uveitis_yesno_re': -1,
        'uveitis_yesno_le': -1,
    }, data)
