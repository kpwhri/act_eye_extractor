from eye_extractor.output.variable import column_from_variable, column_from_variable_binary
from eye_extractor.ro.rvo import RvoType


def build_rao(data):
    return column_from_variable_binary(data, 'rao_yesno')


def build_rvo(data):
    return column_from_variable_binary(data, 'rvo_yesno')


def _rename_rvo_type(val):
    match val:
        case RvoType.RVO:
            return 3
        case RvoType.CRVO:
            return 1
        case RvoType.BRVO:
            return 2


def build_rvo_type(data, *, skip_output_mappings=False):
    rename_func = None if skip_output_mappings else _rename_rvo_type
    return column_from_variable(
        {
            'rvo_yesno_re': RvoType.UNKNOWN,
            'rvo_yesno_le': RvoType.UNKNOWN,
            'rvo_yesno_unk': RvoType.UNKNOWN,
        },
        data,
        transformer_func=lambda x: RvoType(x['kind']),
        renamevar_func=lambda x: f'rvo_type_{x.split("_")[-1]}',
        rename_func=rename_func,
    )


def build_ro_variables(data):
    curr = data['ro']
    results = {}
    results.update(build_rao(curr['rao']))
    results.update(build_rvo(curr['rvo']))
    results.update(build_rvo_type(curr['rvo']))
    return results
