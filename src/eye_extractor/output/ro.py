from eye_extractor.output.variable import column_from_variable, column_from_variable_binary


def build_rao(data):
    return column_from_variable_binary(data, 'rao_yesno')


def build_rvo(data):
    return column_from_variable_binary(data, 'rvo_yesno')


def build_ro_variables(data):
    curr = data['ro']
    results = {}
    results.update(build_rao(curr['rao']))
    results.update(build_rvo(curr['rvo']))
    return results
