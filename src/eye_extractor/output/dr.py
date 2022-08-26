from enum import IntEnum

from eye_extractor.common.algo.fluid import Fluid, fluid_prioritization, rename_fluid
from eye_extractor.common.algo.treatment import Treatment
from eye_extractor.common.drug.antivegf import AntiVegf, rename_antivegf
from eye_extractor.dr.dr_type import DrType
from eye_extractor.dr.hemorrhage_type import HemorrhageType
from eye_extractor.output.variable import column_from_variable, column_from_variable_binary


def build_dr(data):
    return column_from_variable_binary(data, 'diab_retinop_yesno')


def build_ret_micro(data):
    return column_from_variable_binary(data, 'ret_microaneurysm')


def build_cottonwspot(data):
    return column_from_variable_binary(data, 'cottonwspot')


def build_hard_exudates(data):
    return column_from_variable_binary(data, 'hardexudates')


# Categorical variable
# def build_ven_beading(data):
#     return column_from_variable(
#         {
#             f'venbeading_re': -1,
#             f'venbeading_le': -1,
#         },
#         data,
#         transformer_func=lambda n: n['severity'],
#         filter_func=lambda n: n['value'] in {ctype.value for ctype in cataracttypes},
#         convert_func=lambda n: f'cataract_type_{n[-2:]}',
#     )

def build_disc_edema(data):
    return column_from_variable_binary(data, 'disc_edema_dr')


def build_hemorrhage(data):
    return column_from_variable_binary(data, 'hemorrhage_dr')


def build_hemorrhage_type(data):
    return column_from_variable({
            f'hemorrhage_typ_dr_re': HemorrhageType.UNKNOWN,
            f'hemorrhage_typ_dr_le': HemorrhageType.UNKNOWN,
            f'hemorrhage_typ_dr_unk': HemorrhageType.UNKNOWN,
        },
        data,
        transformer_func=HemorrhageType
    )


# def build_irma(data):
#     return column_from_variable({
#             f'venbeading_re': -1,
#             f'venbeading_le': -1,
#         },
#         data)


def build_fluid(data, *, skip_rename_variable=False):
    # TODO: check if DR
    return column_from_variable(
        {
            'fluid_re': Fluid.UNKNOWN,
            'fluid_le': Fluid.UNKNOWN,
            'fluid_unk': Fluid.UNKNOWN,
        },
        data,
        transformer_func=Fluid,
        result_func=fluid_prioritization,
        enum_to_str=True,
        renamevar_func=lambda x: x.replace('fluid', 'fluid_dr'),
        rename_func=None if skip_rename_variable else rename_fluid
    )


def build_laser_scars(data):
    return column_from_variable_binary(data, 'dr_laser_scars')


def build_laser_panrentinal(data):
    return column_from_variable_binary(data, 'laserpanret_photocoag')


def build_focal_laser_scar_type(data):
    return column_from_variable_binary(data, 'focal_dr_laser_scar_type')


def build_grid_laser_scar_type(data):
    return column_from_variable_binary(data, 'grid_dr_laser_scar_type')


def build_macular_laser_scar_type(data):
    return column_from_variable_binary(data, 'macular_dr_laser_scar_type')


def build_neovasc(data):
    return column_from_variable_binary(data, 'neovasc_yesno')


def build_nva(data):
    return column_from_variable_binary(data, 'nva_yesno')


def build_nvi(data):
    return column_from_variable_binary(data, 'nvi_yesno')


# def build_nvd(data):
#     return column_from_variable({
#             f'venbeading_re': -1,
#             f'venbeading_le': -1,
#         },
#         data)


# def build_nve(data):
#     return column_from_variable({
#             f'venbeading_re': -1,
#             f'venbeading_le': -1,
#         },
#         data)


def build_dr_type(data):
    return column_from_variable({
            f'diabretinop_type_re': DrType.UNKNOWN,
            f'diabretinop_type_le': DrType.UNKNOWN,
            f'diabretinop_type_unk': DrType.UNKNOWN,
        },
        data)


# def build_npdr(data):
#     return column_from_variable({
#             f'venbeading_re': -1,
#             f'venbeading_le': -1,
#         },
#         data)


# def build_pdr(data):
#     return column_from_variable({
#             f'venbeading_re': -1,
#             f'venbeading_le': -1,
#         },
#         data)


def _rename_dr_treatment(val: IntEnum):
    # convert to output values
    match val:
        case Treatment.FOCAL:
            return 6
        case Treatment.SURGERY:
            return 4  # surgery
        case val if 311 <= val.value <= 319:
            return 3  # antivegf
        case Treatment.PRP:
            return 2
        case Treatment.OBSERVE:
            return 1  # observe
        case val if val.value > 0:
            return 5  # other
    return val.value


def build_dr_treatment(data):
    # TODO: check if DR
    return column_from_variable(
        {
            'tx_re': Treatment.UNKNOWN,
            'tx_le': Treatment.UNKNOWN,
            'tx_unk': Treatment.UNKNOWN,
        },
        data,
        renamevar_func=lambda x: f'drtreatment_{x.split("_")[-1]}',
        rename_func=_rename_dr_treatment,
        filter_func=lambda x: x.get('category', None) in {'DR', 'ALL', 'LASER', 'ANTIVEGF'},
        transformer_func=Treatment,
        enum_to_str=False,
    )


def build_edema(data):
    return column_from_variable_binary(data, 'dmacedema_yesno')


def build_sig_edema(data):
    return column_from_variable_binary(data, 'dmacedema_clinsignif')


def build_oct_cme(data):
    return column_from_variable_binary(data, 'oct_centralmac')


# def build_edema_tx(data):
#     return column_from_variable({
#             f'venbeading_re': -1,
#             f'venbeading_le': -1,
#         },
#         data)


def build_dmacedema_antivegf(data):
    # TODO: check is RVO
    return column_from_variable(
        {
            'tx_re': AntiVegf.UNKNOWN,
            'tx_le': AntiVegf.UNKNOWN,
            'tx_unk': AntiVegf.UNKNOWN,
        },
        data,
        renamevar_func=lambda x: f'dmacedema_antivegf_{x.split("_")[-1]}',
        rename_func=rename_antivegf,
        filter_func=lambda x: x.get('category', None) in {'ANTIVEGF'},
        transformer_func=AntiVegf,
        enum_to_str=False,
    )


def build_dr_variables(data):
    curr = data['dr']
    results = {}
    results.update(build_dr(curr['binary_vars']))
    results.update(build_ret_micro(curr['binary_vars']))
    results.update(build_cottonwspot(curr['binary_vars']))
    results.update(build_hard_exudates(curr['binary_vars']))
    results.update(build_disc_edema(curr['binary_vars']))
    results.update(build_hemorrhage(curr['binary_vars']))
    results.update(build_hemorrhage_type(curr['hemorrhage_type']))
    results.update(build_fluid(data['common']['treatment']))
    results.update(build_laser_scars(curr['binary_vars']))
    results.update(build_laser_panrentinal(curr['binary_vars']))
    results.update(build_focal_laser_scar_type(curr['laser_scar_type']))
    results.update(build_grid_laser_scar_type(curr['laser_scar_type']))
    results.update(build_macular_laser_scar_type(curr['laser_scar_type']))
    results.update(build_neovasc(curr['binary_vars']))
    results.update(build_nva(curr['binary_vars']))
    results.update(build_nvi(curr['binary_vars']))
    results.update(build_dr_type(curr['dr_type']))
    results.update(build_edema(curr['binary_vars']))
    results.update(build_sig_edema(curr['binary_vars']))
    results.update(build_oct_cme(curr['binary_vars']))
    results.update(build_dmacedema_antivegf[data['common']['treatment']])
    return results
