from eye_extractor.output.variable import column_from_variable, column_from_variable_binary


def build_cataract_variables(data):
    curr = data['cataract']
    results = {}
    results.update(build_cataract(curr))
    return results


def build_cataract(data):
    return column_from_variable_binary(data, 'cataract_yesno')
