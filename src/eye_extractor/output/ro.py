from enum import IntEnum

from eye_extractor.common.algo.treatment import Treatment
from eye_extractor.common.drug.antivegf import AntiVegf, rename_antivegf
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


def _rename_rvo_treatment(val: IntEnum):
    # convert to output values
    print(val, val.value)
    match val:
        case val if 300 <= val.value <= 309:
            return 4  # steroids
        case val if 311 <= val.value <= 319:
            return 3  # antivegf
        case val if 100 <= val.value <= 199:
            return 2  # laser
        case Treatment.OBSERVE:
            return 1  # observe
        case val if val.value > 0:
            return 5  # other
    return val.value


def build_rvo_treatment(data):
    # TODO: check is RVO

    return column_from_variable(
        {
            'tx_re': Treatment.UNKNOWN,
            'tx_le': Treatment.UNKNOWN,
            'tx_unk': Treatment.UNKNOWN,
        },
        data,
        renamevar_func=lambda x: f'rvo_treatment_{x.split("_")[-1]}',
        rename_func=_rename_rvo_treatment,
        filter_func=lambda x: x.get('category', None) in {'RVO', 'ALL', 'LASER', 'ANTIVEGF'},
        transformer_func=Treatment,
        enum_to_str=False,
    )


def build_rvo_antivegf(data):
    # TODO: check is RVO

    return column_from_variable(
        {
            'tx_re': AntiVegf.UNKNOWN,
            'tx_le': AntiVegf.UNKNOWN,
            'tx_unk': AntiVegf.UNKNOWN,
        },
        data,
        renamevar_func=lambda x: f'rvo_antivegf_{x.split("_")[-1]}',
        rename_func=rename_antivegf,
        filter_func=lambda x: x.get('category', None) in {'ANTIVEGF'},
        transformer_func=AntiVegf,
        enum_to_str=False,
    )


def build_ro_variables(data):
    curr = data['ro']
    results = {}
    # RAO
    results.update(build_rao(curr['rao']))
    # RVO
    results.update(build_rvo(curr['rvo']))
    results.update(build_rvo_type(curr['rvo_type']))
    results.update(build_rvo_treatment(data['common']['treatment']))
    results.update(build_rvo_antivegf(data['common']['treatment']))
    return results
