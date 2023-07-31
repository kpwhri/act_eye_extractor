from enum import IntEnum

from eye_extractor.common.algo.fluid import Fluid, fluid_prioritization, rename_fluid
from eye_extractor.common.algo.treatment import Treatment
from eye_extractor.common.drug.antivegf import AntiVegf, rename_antivegf
from eye_extractor.common.severity import Risk, Severity
from eye_extractor.dr.dr_type import DrType
from eye_extractor.dr.hemorrhage_type import HemorrhageType
from eye_extractor.output.common import macula_is_wnl
from eye_extractor.output.labels import DRTreatment
from eye_extractor.output.variable import column_from_variable_binary, column_from_variable_abbr, build_lat_suffixes


def build_dr_yesno(data, *, macula_wnl=None, note_date=None):
    if macula_is_wnl(macula_wnl, note_date):
        return build_lat_suffixes('diab_retinop_yesno', 0)
    return column_from_variable_binary(data, 'diab_retinop_yesno', restrict_date=note_date)


def build_ret_micro(data, *, note_date=None):
    return column_from_variable_binary(data, 'ret_microaneurysm', restrict_date=note_date)


def build_cottonwspot(data, *, note_date=None):
    return column_from_variable_binary(data, 'cottonwspot', restrict_date=note_date)


def build_hard_exudates(data, *, note_date=None):
    return column_from_variable_binary(data, 'hardexudates', restrict_date=note_date)


def build_exudates(data, *, note_date=None):
    return column_from_variable_binary(data, 'exudates', restrict_date=note_date)


def build_ven_beading(data, *, note_date=None):
    return column_from_variable_abbr(
        'venbeading', Severity.UNKNOWN, data,
        restrict_date=note_date,
        transformer_func=Severity,
        enum_to_str=True,
    )


def build_disc_edema(data, *, note_date=None):
    return column_from_variable_binary(data, 'disc_edema_dr', restrict_date=note_date)


def build_hemorrhage(data, *, note_date=None):
    return column_from_variable_binary(data, 'hemorrhage_dr', restrict_date=note_date)


def build_hemorrhage_type(data, *, note_date=None):
    return column_from_variable_abbr(
        'hemorrhage_typ_dr', HemorrhageType.UNKNOWN, data,
        restrict_date=note_date,
        transformer_func=HemorrhageType
    )


def build_intraretinal_severity(data, *, note_date=None):
    return column_from_variable_abbr(
        'intraretinal_hem', Severity.UNKNOWN, data,
        restrict_date=note_date,
        transformer_func=Severity,
        enum_to_str=True,
    )


def build_dot_blot_severity(data, *, note_date=None):
    return column_from_variable_abbr(
        'dotblot_hem', Severity.UNKNOWN, data,
        restrict_date=note_date,
        transformer_func=Severity,
        enum_to_str=True,
    )


def build_irma(data, *, note_date=None):
    return column_from_variable_abbr(
        'irma', Severity.UNKNOWN, data,
        restrict_date=note_date,
        transformer_func=Severity,
        enum_to_str=True,
    )


def build_fluid(data, *, skip_rename_variable=False, note_date=None):
    # TODO: check if DR
    return column_from_variable_abbr(
        'fluid', Fluid.UNKNOWN, data,
        restrict_date=note_date,
        transformer_func=Fluid,
        result_func=fluid_prioritization,
        enum_to_str=True,
        renamevar_func=lambda x: x.replace('fluid', 'fluid_dr'),
        rename_func=None if skip_rename_variable else rename_fluid,
    )


def build_laser_scars(data, *, note_date=None):
    return column_from_variable_binary(data, 'dr_laser_scars', restrict_date=note_date)


def build_laser_panrentinal(data, *, note_date=None):
    return column_from_variable_binary(data, 'laserpanret_photocoag', restrict_date=note_date)


def build_focal_laser_scar_type(data, *, note_date=None):
    return column_from_variable_binary(data, 'focal_dr_laser_scar_type', restrict_date=note_date)


def build_grid_laser_scar_type(data, *, note_date=None):
    return column_from_variable_binary(data, 'grid_dr_laser_scar_type', restrict_date=note_date)


def build_macular_laser_scar_type(data, *, note_date=None):
    return column_from_variable_binary(data, 'macular_dr_laser_scar_type', restrict_date=note_date)


def build_neovasc(data, *, note_date=None):
    return column_from_variable_binary(data, 'neovasc_yesno', restrict_date=note_date)


def build_nva(data, *, note_date=None):
    return column_from_variable_binary(data, 'nva_yesno', restrict_date=note_date)


def build_nvi(data, *, note_date=None):
    return column_from_variable_binary(data, 'nvi_yesno', restrict_date=note_date)


def build_nvd(data, *, note_date=None):
    return column_from_variable_binary(data, 'nvd_yesno', restrict_date=note_date)


def build_nve(data, *, note_date=None):
    return column_from_variable_binary(data, 'nve_yesno', restrict_date=note_date)


def build_dr_type(data, *, note_date=None):
    return column_from_variable_abbr(
        'diabretinop_type', DrType.UNKNOWN, data,
        restrict_date=note_date,
    )


def build_npdr_severity(data, *, note_date=None):
    return column_from_variable_abbr(
        'nonprolifdr', Severity.UNKNOWN, data,
        restrict_date=note_date,
        enum_to_str=True,
        transformer_func=Severity,
    )


def build_pdr_severity(data, *, note_date=None):
    return column_from_variable_abbr(
        'prolifdr', Risk.UNKNOWN, data,
        restrict_date=note_date,
        enum_to_str=True,
        transformer_func=Risk,
    )


def _rename_dr_tx(val: IntEnum):
    # convert to output values
    match val:
        case Treatment.FOCAL:
            return DRTreatment.FOCAL.value
        case Treatment.SURGERY:
            return DRTreatment.SURGERY.value  # surgery
        case val if 311 <= val.value <= 319:
            return DRTreatment.INJECTIONS.value  # injections
        case Treatment.PRP:
            return DRTreatment.PRP.value
        case Treatment.OBSERVE:
            return DRTreatment.OBSERVE.value  # observe
        case val if val.value > 0:
            return DRTreatment.OTHER.value  # other
    return val.value


def build_dr_tx(data, *, note_date=None):
    # TODO: check if DR
    return column_from_variable_abbr(
        'tx', Treatment.UNKNOWN, data,
        restrict_date=note_date,
        renamevar_func=lambda x: f'drtreatment_{x.split("_")[-1]}',
        rename_func=_rename_dr_tx,
        enum_to_str=True,
        filter_func=lambda x: x.get('category', None) in {'DR', 'ALL', 'LASER', 'ANTIVEGF'},
        transformer_func=Treatment,
    )


def build_dme_yesno(data, *, note_date=None):
    return column_from_variable_binary(data, 'dmacedema_yesno', restrict_date=note_date)


def build_sig_edema(data, *, note_date=None):
    return column_from_variable_binary(data, 'dmacedema_clinsignif', restrict_date=note_date)


def build_oct_cme(data, *, note_date=None):
    return column_from_variable_binary(data, 'oct_centralmac', restrict_date=note_date)


def _rename_dme_tx(val: IntEnum):
    # convert to output values
    match val:
        case val if 311 <= val.value <= 319:
            return 4  # injections
        case val if 121 <= val.value <= 123:
            return 2  # focal, grid, macular
        case Treatment.PHOTODYNAMIC:
            return 2  # photodynamic therapy
        case Treatment.OBSERVE:
            return 1  # observe
        case val if val.value > 0:
            return 5  # other
    return val.value


def build_dme_tx(data, *, note_date=None):
    # TODO: check if DME
    return column_from_variable_abbr(
        'tx', Treatment.UNKNOWN, data,
        restrict_date=note_date,
        renamevar_func=lambda x: f'dmacedema_tx_{x.split("_")[-1]}',
        rename_func=_rename_dme_tx,
        filter_func=lambda x: x.get('category', None) in {'DR', 'ALL', 'LASER', 'ANTIVEGF'},
        transformer_func=Treatment,
        enum_to_str=False,
    )


def build_dmacedema_antivegf(data, *, note_date=None):
    # TODO: check if DME
    return column_from_variable_abbr(
        'tx', AntiVegf.UNKNOWN, data,
        restrict_date=note_date,
        renamevar_func=lambda x: f'dmacedema_antivegf_{x.split("_")[-1]}',
        rename_func=rename_antivegf,
        filter_func=lambda x: x.get('category', None) in {'ANTIVEGF'},
        transformer_func=AntiVegf,
        enum_to_str=False,
    )


def build_cmt_value(data, *, note_date=None):
    # TODO: check if DME
    return column_from_variable_abbr(
        'dmacedema_cmt', -1, data,
        restrict_date=note_date,
    )


def build_dr_variables(data):
    curr = data['dr']
    note = data['note']
    results = {}
    results.update(build_dr_yesno(curr['dr_yesno'], macula_wnl=data['common']['macula_wnl'], note_date=note['date']))
    results.update(build_ret_micro(curr['binary_vars'], note_date=note['date']))
    results.update(build_cottonwspot(curr['cottonwspot'], note_date=note['date']))
    results.update(build_hard_exudates(curr['exudates'], note_date=note['date']))
    results.update(build_exudates(curr['exudates'], note_date=note['date']))
    results.update(build_disc_edema(curr['binary_vars'], note_date=note['date']))
    results.update(build_ven_beading(curr['venous_beading'], note_date=note['date']))
    results.update(build_hemorrhage(curr['binary_vars'], note_date=note['date']))
    results.update(build_hemorrhage_type(curr['hemorrhage_type'], note_date=note['date']))
    results.update(build_intraretinal_severity(curr['hemorrhage_type'], note_date=note['date']))
    results.update(build_dot_blot_severity(curr['hemorrhage_type'], note_date=note['date']))
    results.update(build_irma(curr['irma'], note_date=note['date']))
    results.update(build_fluid(data['common']['treatment'], note_date=note['date']))
    results.update(build_laser_scars(curr['binary_vars'], note_date=note['date']))
    results.update(build_laser_panrentinal(curr['binary_vars'], note_date=note['date']))
    results.update(build_focal_laser_scar_type(curr['laser_scar_type'], note_date=note['date']))
    results.update(build_grid_laser_scar_type(curr['laser_scar_type'], note_date=note['date']))
    results.update(build_macular_laser_scar_type(curr['laser_scar_type'], note_date=note['date']))
    results.update(build_neovasc(curr['binary_vars'], note_date=note['date']))
    results.update(build_nva(curr['nv_types'], note_date=note['date']))
    results.update(build_nvi(curr['nv_types'], note_date=note['date']))
    results.update(build_nvd(curr['nv_types'], note_date=note['date']))
    results.update(build_nve(curr['nv_types'], note_date=note['date']))
    results.update(build_dr_type(curr['dr_type'], note_date=note['date']))
    results.update(build_npdr_severity(curr['dr_type'], note_date=note['date']))
    results.update(build_pdr_severity(curr['pdr'], note_date=note['date']))
    results.update(build_dr_tx(data['common']['treatment'], note_date=note['date']))
    results.update(build_dme_yesno(curr['dme_yesno'], note_date=note['date']))
    results.update(build_sig_edema(curr['binary_vars'], note_date=note['date']))
    results.update(build_oct_cme(curr['binary_vars'], note_date=note['date']))
    results.update(build_dme_tx(data['common']['treatment'], note_date=note['date']))
    results.update(build_dmacedema_antivegf(data['common']['treatment'], note_date=note['date']))
    results.update(build_cmt_value(curr['cmt_value'], note_date=note['date']))
    return results
