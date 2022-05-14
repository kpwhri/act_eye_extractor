from eye_extractor.output.variable import column_from_variable


def build_rao(data):
    return column_from_variable(
        {
            'rao_yesno_le': -1,
            'rao_yesno_re': -1,
        },
        data,
    )


def build_ro_variables(data):
    curr = data['ro']
    results = {}
    results.update(build_rao(curr))
    return results
