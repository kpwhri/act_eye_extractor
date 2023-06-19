from enum import IntEnum

from eye_extractor.common.algo.fluid import Fluid, fluid_prioritization, rename_fluid, rename_intraretfluid, \
    rename_subretfluid
from eye_extractor.common.algo.treatment import Treatment
from eye_extractor.common.drug.antivegf import AntiVegf, rename_antivegf
from eye_extractor.output.common import macula_is_wnl
from eye_extractor.output.variable import column_from_variable_binary, column_from_variable_abbr, build_lat_suffixes
from eye_extractor.ro.rvo import RvoType


def build_rao(data, *, macula_wnl=None, note_date=None):
    if macula_is_wnl(macula_wnl, note_date):
        return build_lat_suffixes('rao_yesno', 0)
    return column_from_variable_binary(data, 'rao_yesno', restrict_date=note_date)


def build_rvo(data, *, macula_wnl=None, note_date=None):
    if macula_is_wnl(macula_wnl, note_date):
        return build_lat_suffixes('rvo_yesno', 0)
    return column_from_variable_binary(data, 'rvo_yesno', restrict_date=note_date)


def _rename_rvo_type(val):
    match val:
        case RvoType.RVO:
            return 3
        case RvoType.CRVO:
            return 1
        case RvoType.BRVO:
            return 2
    return val.value


def build_rvo_type(data, *, skip_output_mappings=False, note_date=None):
    rename_func = None if skip_output_mappings else _rename_rvo_type
    return column_from_variable_abbr(
        'rvo_yesno', RvoType.UNKNOWN, data,
        restrict_date=note_date,
        transformer_func=lambda x: RvoType(x['kind']),
        renamevar_func=lambda x: f'rvo_type_{x.split("_")[-1]}',
        rename_func=rename_func,
    )


def _rename_rvo_treatment(val: IntEnum):
    # convert to output values
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


def build_rvo_treatment(data, *, note_date=None):
    # TODO: check is RVO

    return column_from_variable_abbr(
        'tx', Treatment.UNKNOWN, data,
        restrict_date=note_date,
        renamevar_func=lambda x: f'rvo_treatment_{x.split("_")[-1]}',
        rename_func=_rename_rvo_treatment,
        filter_func=lambda x: x.get('category', None) in {'RVO', 'ALL', 'LASER', 'ANTIVEGF'},
        transformer_func=Treatment,
        enum_to_str=False,
    )


def build_rvo_antivegf(data, *, note_date=None):
    # TODO: check is RVO

    return column_from_variable_abbr(
        'tx_re', AntiVegf.UNKNOWN, data,
        restrict_date=note_date,
        renamevar_func=lambda x: f'rvo_antivegf_{x.split("_")[-1]}',
        rename_func=rename_antivegf,
        filter_func=lambda x: x.get('category', None) in {'ANTIVEGF'},
        transformer_func=AntiVegf,
        enum_to_str=False,
    )


def build_fluid(data, *, skip_rename_variable=False, note_date=None):
    # TODO: check if RVO
    return column_from_variable_abbr(
        'fluid', Fluid.UNKNOWN, data,
        restrict_date=note_date,
        transformer_func=Fluid,
        result_func=fluid_prioritization,
        enum_to_str=True,
        renamevar_func=lambda x: x.replace('fluid', 'fluid_rvo'),
        rename_func=None if skip_rename_variable else rename_fluid
    )


def build_intraretfluid(data, *, note_date=None):
    # TODO: check if RVO
    return column_from_variable_abbr(
        'fluid', Fluid.UNKNOWN, data,
        restrict_date=note_date,
        transformer_func=Fluid,
        result_func=fluid_prioritization,
        filter_func=lambda x: x in {
            Fluid.INTRARETINAL_FLUID, Fluid.NO_INTRARETINAL_FLUID,
            Fluid.SUB_AND_INTRARETINAL_FLUID, Fluid.NO_SUB_AND_INTRARETINAL_FLUID,
        },
        enum_to_str=True,
        renamevar_func=lambda x: x.replace('fluid', 'rvo_intraretfluid'),
        rename_func=rename_intraretfluid,
    )


def build_subretfluid(data, *, note_date=None):
    # TODO: check if RVO
    return column_from_variable_abbr(
        'fluid', Fluid.UNKNOWN, data,
        restrict_date=note_date,
        transformer_func=Fluid,
        result_func=fluid_prioritization,
        filter_func=lambda x: x in {
            Fluid.SUBRETINAL_FLUID, Fluid.NO_SUBRETINAL_FLUID,
            Fluid.SUB_AND_INTRARETINAL_FLUID, Fluid.NO_SUB_AND_INTRARETINAL_FLUID,
        },
        enum_to_str=True,
        renamevar_func=lambda x: x.replace('fluid', 'rvo_subretfluid'),
        rename_func=rename_subretfluid,
    )


def build_ro_variables(data):
    curr = data['ro']
    note = data['note']
    results = {}
    # RAO
    results.update(build_rao(curr['rao'], macula_wnl=data['common']['macula_wnl'], note_date=note['date']))
    # RVO
    results.update(build_rvo(curr['rvo'], macula_wnl=data['common']['macula_wnl'], note_date=note['date']))
    results.update(build_rvo_type(curr['rvo'], note_date=note['date']))
    results.update(build_rvo_treatment(data['common']['treatment'], note_date=note['date']))
    results.update(build_rvo_antivegf(data['common']['treatment'], note_date=note['date']))
    results.update(build_fluid(data['common']['treatment'], note_date=note['date']))
    results.update(build_subretfluid(data['common']['treatment'], note_date=note['date']))
    results.update(build_intraretfluid(data['common']['treatment'], note_date=note['date']))
    return results
