"""Build miscellaneous variables.

"""
from eye_extractor.common.algo.fluid import Fluid, rename_intraretfluid, fluid_prioritization, rename_subretfluid, \
    rename_fluid
from eye_extractor.output.variable import column_from_variable


def build_shared_variables(data):
    results = {}
    results.update(build_fluid(data['common']['fluid']))
    results.update(build_subretfluid(data['common']['fluid']))
    results.update(build_intraretfluid(data['common']['fluid']))
    return results


def get_default_fluid_result():
    return {
        'fluid_re': Fluid.UNKNOWN,
        'fluid_le': Fluid.UNKNOWN,
        'fluid_unk': Fluid.UNKNOWN,
    }


def build_fluid(data, *, skip_rename_variable=False, rename_var='fluid'):
    default = get_default_fluid_result()
    return column_from_variable(
        default,
        data,
        transformer_func=Fluid,
        result_func=fluid_prioritization,
        enum_to_str=True,
        renamevar_func=lambda x: x.replace('fluid', rename_var),
        rename_func=None if skip_rename_variable else rename_fluid
    )


def build_intraretfluid(data, *, rename_var='intraretfluid'):
    default = get_default_fluid_result()
    return column_from_variable(
        default,
        data,
        transformer_func=Fluid,
        result_func=fluid_prioritization,
        filter_func=lambda x: x['value'] in {
            Fluid.INTRARETINAL_FLUID.value, Fluid.NO_INTRARETINAL_FLUID.value,
            Fluid.SUB_AND_INTRARETINAL_FLUID.value, Fluid.NO_SUB_AND_INTRARETINAL_FLUID.value,
        },
        renamevar_func=lambda x: x.replace('fluid', rename_var),
        rename_func=rename_intraretfluid,
    )


def build_subretfluid(data, *, rename_var='subretfluid'):
    default = get_default_fluid_result()
    return column_from_variable(
        default,
        data,
        transformer_func=Fluid,
        result_func=fluid_prioritization,
        filter_func=lambda x: x['value'] in {
            Fluid.SUBRETINAL_FLUID.value, Fluid.NO_SUBRETINAL_FLUID.value,
            Fluid.SUB_AND_INTRARETINAL_FLUID.value, Fluid.NO_SUB_AND_INTRARETINAL_FLUID.value,
        },
        renamevar_func=lambda x: x.replace('fluid', rename_var),
        rename_func=rename_subretfluid,
    )
