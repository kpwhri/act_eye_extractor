from eye_extractor.output.variable import column_from_variable, column_from_variable_binary
from eye_extractor.ro.rvo import RvoType


def build_rao(data):
    return column_from_variable_binary(data, 'rao_yesno')


def build_rvo(data):
    return column_from_variable_binary(data, 'rvo_yesno')


def build_rvo_type(data):
    return column_from_variable(
        {
            'rvo_yesno_re': RvoType.UNKNOWN,
            'rvo_yesno_le': RvoType.UNKNOWN,
            'rvo_yesno_unk': RvoType.UNKNOWN,
        },
        data,
        transformer_func=lambda x: RvoType(x['kind']),
        renamevar_func=lambda x: f'rvo_type_{x.split("_")[-1]}',
    )


def build_ro_variables(data):
    curr = data['ro']
    results = {}
    results.update(build_rao(curr['rao']))
    results.update(build_rvo(curr['rvo']))
    results.update(build_rvo_type(curr['rvo']))
    return results
