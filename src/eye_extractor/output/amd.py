from eye_extractor.amd.amd import AMD
from eye_extractor.amd.cnv import ChoroidalNeoVasc
from eye_extractor.amd.dry import DrySeverity
from eye_extractor.amd.ga import GeoAtrophy
from eye_extractor.amd.lasertype import Laser
from eye_extractor.amd.ped import PigEpiDetach
from eye_extractor.amd.scar import Scar
from eye_extractor.amd.vitamins import Vitamin
from eye_extractor.amd.wet import WetSeverity
from eye_extractor.common.algo.fluid import Fluid
from eye_extractor.common.algo.treatment import Treatment
from eye_extractor.common.drug.antivegf import rename_antivegf, AntiVegf
from eye_extractor.laterality import Laterality
from eye_extractor.output.common import macula_is_wnl
from eye_extractor.output.shared import get_default_fluid_result, build_subretfluid, build_intraretfluid, build_fluid
from eye_extractor.output.variable import column_from_variable, update_column, column_from_variable_abbr, \
    rename_variable_func, column_from_variable_binary


def build_macular_cyst(data, *, note_date=None):
    return column_from_variable_binary(data, 'macular_cyst', restrict_date=note_date, )


def build_amd_variables(data):
    curr = data['amd']
    note = data['note']
    results = {}
    results.update(build_amd(
        curr['amd'],
        is_amd=note['is_amd'],
        lat=note['default_lat'],
        macula_wnl=data['common']['macula_wnl'],
        note_date=note['date'])
    )
    results.update(get_drusen_size(curr['drusen'], note_date=note['date']))
    results.update(get_drusen_type(curr['drusen'], note_date=note['date']))
    srh = build_subretinal_hemorrhage(curr['srh'], note_date=note['date'])
    results.update(srh)
    results.update(get_pigmentary_changes(curr['pigment'], note_date=note['date']))
    fluid = build_fluid_amd(data['common']['fluid'], is_amd=note['is_amd'], note_date=note['date'])
    results.update(fluid)
    results.update(build_subretfluid_amd(data['common']['fluid'], is_amd=note['is_amd'], note_date=note['date']))
    results.update(build_intraretfluid_amd(data['common']['fluid'], is_amd=note['is_amd'], note_date=note['date']))
    results.update(build_ped(curr['ped'], note_date=note['date']))
    cnv = build_choroidalneovasc(curr['cnv'], note_date=note['date'])
    results.update(cnv)
    results.update(build_subret_fibrous(curr['scar'], note_date=note['date']))
    ga = build_geoatrophy(curr['ga'], note_date=note['date'])
    results.update(ga)
    results.update(build_dryamd_severity(curr['dry'], is_amd=note['is_amd'], note_date=note['date'], ga_result=ga))
    results.update(build_wetamd_severity(
        curr['wet'],
        cnv_result=cnv,
        srh_result=srh,
        is_amd=note['is_amd'],
        is_dr=note['is_dr'],
        fluid_result=fluid,
        note_date=note['date'],
    ))
    results.update(build_amd_vitamin(curr['vitamin'], note_date=note['date']))
    # results.update(build_lasertype(curr['lasertype']))
    results.update(build_lasertype_new(data['common']['treatment'], is_amd=note['is_amd'], note_date=note['date']))
    results.update(build_amd_antivegf(data['common']['treatment'], is_amd=note['is_amd'], note_date=note['date']))
    results.update(build_macular_cyst(curr['cyst']))
    return results


def build_amd(data, *, is_amd=None, lat=Laterality.UNKNOWN, note_date=None, macula_wnl=None):
    wnl_lat = macula_is_wnl(macula_wnl, note_date)
    if wnl_lat == Laterality.OU:
        return {
            'amd_re': AMD.NO,
            'amd_le': AMD.NO,
            'amd_unk': AMD.NO,
        }
    results = {
        'amd_re': AMD.UNKNOWN,
        'amd_le': AMD.UNKNOWN,
        'amd_unk': AMD.UNKNOWN,
    }
    if is_amd:
        if lat in {Laterality.OD, Laterality.OU}:
            results['amd_re'] = AMD.YES
        if lat in {Laterality.OU, Laterality.OU}:
            results['amd_le'] = AMD.YES
    results = column_from_variable(
        results, data,
        restrict_date=note_date,
    )
    if wnl_lat == Laterality.OD:
        results['amd_re'] = AMD.NO
    if wnl_lat == Laterality.OS:
        results['amd_le'] = AMD.NO
    return results


def get_drusen_size(data, *, note_date=None):
    return column_from_variable_abbr(
        'drusen_size', -1, data,
        restrict_date=note_date,
    )


def get_drusen_type(data, *, note_date=None):
    return column_from_variable_abbr(
        'drusen_type', -1, data,
        restrict_date=note_date,
    )


def build_subretinal_hemorrhage(data, *, note_date=None):
    return column_from_variable_abbr('subretinal_hem', -1, data, restrict_date=note_date)


def get_pigmentary_changes(data, *, note_date=None):
    return column_from_variable_abbr('pigmentchanges', -1, data, restrict_date=note_date)


def build_fluid_amd(data, *, is_amd=None, skip_rename_variable=False, note_date=None):
    if is_amd is False:
        return get_default_fluid_result()
    return build_fluid(data, rename_var='fluid_amd', skip_rename_variable=skip_rename_variable, note_date=note_date)


def build_intraretfluid_amd(data, *, is_amd=None, note_date=None):
    if is_amd is False:
        return get_default_fluid_result()
    return build_intraretfluid(data, rename_var='amd_intraretfluid', note_date=note_date)


def build_subretfluid_amd(data, *, is_amd=None, note_date=None):
    if is_amd is False:
        return get_default_fluid_result()
    return build_subretfluid(data, rename_var='amd_subretfluid', note_date=note_date)


def build_ped(data, *, note_date=None):
    """Build binary pigmentary epithelial detachment variable"""
    return column_from_variable_abbr(
        'ped', PigEpiDetach.UNKNOWN, data,
        restrict_date=note_date,
        transformer_func=PigEpiDetach,
    )


def build_choroidalneovasc(data, *, note_date=None):
    """Build cnv/choroidal neovascularization as binary (yes/no/unknown)"""
    return column_from_variable_abbr(
        'choroidalneovasc', ChoroidalNeoVasc.UNKNOWN, data,
        restrict_date=note_date,
        transformer_func=ChoroidalNeoVasc,
        compare_func=lambda n, c: c == ChoroidalNeoVasc.UNKNOWN,  # take first; only update unknown
    )


def build_subret_fibrous(data, *, note_date=None):
    """Build cnv/choroidal neovascularization as binary (yes/no/unknown)"""
    return column_from_variable_abbr(
        'subret_fibrous', Scar.UNKNOWN, data,
        restrict_date=note_date,
        transformer_func=Scar,
        compare_func=lambda n, c: c == Scar.UNKNOWN,  # take first; only update unknown
        enum_to_str=True,
    )


def build_geoatrophy(data, *, note_date=None):
    """Build geographic atrophy as binary (yes/no/unknown)"""
    return column_from_variable_abbr(
        'geoatrophy', GeoAtrophy.UNKNOWN, data,
        restrict_date=note_date,
        transformer_func=GeoAtrophy,
        compare_func=lambda n, c: c == GeoAtrophy.UNKNOWN,  # take first; only update unknown
        enum_to_str=False,  # store as int
    )


def build_dryamd_severity(data, *, is_amd=None, ga_result=None, note_date=None):
    """Build dry amd severity"""
    if is_amd is False:
        return {f'dryamd_severity_{val}': DrySeverity.UNKNOWN for val in ('re', 'le', 'unk')}
    result = column_from_variable_abbr(
        'dryamd_severity', DrySeverity.UNKNOWN, data,
        restrict_date=note_date,
        transformer_func=DrySeverity,
        enum_to_str=True,
    )
    return augment_dryamd_severity(result, ga_result=ga_result)


def augment_dryamd_severity(result, *, ga_result=None):
    result = update_column(result, ga_result, [
        (GeoAtrophy.YES, 'UNKNOWN', 'YES'),
    ])
    return result


def build_wetamd_severity(data, *, cnv_result=None, srh_result=None,
                          is_amd=None, is_dr=None, fluid_result=None, note_date=None):
    """Build wet amd severity"""
    result = column_from_variable_abbr(
        'wetamd_severity', WetSeverity.UNKNOWN, data,
        transformer_func=WetSeverity,
        enum_to_str=True,
        restrict_date=note_date,
    )
    return augment_wetamd_severity(result, cnv_result=cnv_result, srh_result=srh_result,
                                   is_amd=is_amd, is_dr=is_dr, fluid_result=fluid_result)


def augment_wetamd_severity(result, *, cnv_result=None, srh_result=None,
                            is_amd=None, is_dr=None, fluid_result=None, note_date=None):
    result = update_column(result, cnv_result, [
        (ChoroidalNeoVasc.YES, 'UNKNOWN', 'YES'),
    ])
    if is_amd and not is_dr:
        result = update_column(result, srh_result, [
            (1, 'UNKNOWN', 'YES'),
        ])
        result = update_column(result, fluid_result, [
            ({Fluid.SUBRETINAL_FLUID, Fluid.INTRARETINAL_FLUID, Fluid.SUB_AND_INTRARETINAL_FLUID},
             'UNKNOWN', 'YES')
        ])
    return result


def build_amd_vitamin(data, *, note_date=None):
    """Build amd vitamin"""
    return column_from_variable(
        {'amd_vitamin': Vitamin.UNKNOWN}, data,
        restrict_date=note_date,
        transformer_func=Vitamin,
        enum_to_str=False,
    )


def build_lasertype(data, *, note_date=None):
    """Laser type for AMD"""

    def _compare_lasertype(new, curr):
        match new, curr:
            case _, Laser.UNKNOWN:
                return True
            case _, Laser.PHOTODYNAMIC | Laser.THERMAL:
                return False
            case Laser.PHOTODYNAMIC | Laser.THERMAL, _:
                return True
            case Laser.LASER | Laser.NONE, _:
                return True
            case _:
                return False

    return column_from_variable_abbr(
        'amd_lasertype', Laser.UNKNOWN, data,
        restrict_date=note_date,
        transformer_func=Laser,
        enum_to_str=False,
        compare_func=_compare_lasertype,
    )


def build_lasertype_new(data, *, is_amd=None, note_date=None):
    """Laser type for AMD using treatment algorithm"""

    def _compare_lasertype(new, curr):
        match new, curr:
            case _, Treatment.UNKNOWN:
                return True
            case _, Treatment.PHOTODYNAMIC | Treatment.THERMAL:
                return False
            case Treatment.PHOTODYNAMIC | Treatment.THERMAL, _:
                return True
            case Treatment.LASER | Treatment.NONE, _:
                return True
            case _:
                return False

    def _rename_lasertype(val):
        match val:
            case Treatment.LASER:
                return 1
            case Treatment.PHOTODYNAMIC:
                return 2
            case Treatment.THERMAL:
                return 3
        return val.value

    if is_amd is False:
        return {f'amd_lasertype_{lat}': AntiVegf.UNKNOWN for lat in ('re', 'le', 'unk')}
    return column_from_variable_abbr(
        'tx', Treatment.UNKNOWN, data,
        restrict_date=note_date,
        renamevar_func=rename_variable_func('amd_lasertype'),
        rename_func=_rename_lasertype,
        filter_func=lambda x: x.get('category', None) in {'AMD'},
        transformer_func=Treatment,
        enum_to_str=False,
        compare_func=_compare_lasertype,
    )


def build_amd_antivegf(data, *, is_amd=None, note_date=None):
    if is_amd is False:
        return {f'amd_antivegf_{lat}': AntiVegf.UNKNOWN for lat in ('re', 'le', 'unk')}
    return column_from_variable_abbr(
        'tx', AntiVegf.UNKNOWN, data,
        renamevar_func=rename_variable_func('amd_antivegf'),
        rename_func=rename_antivegf,
        filter_func=lambda x: x.get('category', None) in {'ANTIVEGF'},
        transformer_func=AntiVegf,
        enum_to_str=False,
        restrict_date=note_date,
    )
