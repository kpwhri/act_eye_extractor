from eye_extractor.amd.cnv import ChoroidalNeoVasc
from eye_extractor.amd.dry import DrySeverity
from eye_extractor.common.algo.fluid import Fluid, fluid_prioritization, rename_fluid, rename_intraretfluid, \
    rename_subretfluid
from eye_extractor.amd.ga import GeoAtrophy
from eye_extractor.amd.lasertype import Laser
from eye_extractor.amd.ped import PigEpiDetach
from eye_extractor.amd.scar import Scar
from eye_extractor.amd.vitamins import Vitamin
from eye_extractor.amd.wet import WetSeverity
from eye_extractor.common.algo.treatment import Treatment
from eye_extractor.common.drug.antivegf import rename_antivegf, AntiVegf
from eye_extractor.output.laterality import laterality_from_int
from eye_extractor.laterality import Laterality
from eye_extractor.output.variable import column_from_variable, update_column


def build_amd_variables(data):
    curr = data['amd']
    results = {}
    results.update(get_amd(curr['amd']))
    results.update(get_drusen(curr['drusen']))
    srh = get_subretinal_hemorrhage(curr['srh'])
    results.update(srh)
    results.update(get_pigmentary_changes(curr['pigment']))
    fluid = build_fluid(data['common']['fluid'])
    results.update(fluid)
    results.update(build_subretfluid(data['common']['fluid']))
    results.update(build_intraretfluid(data['common']['fluid']))
    results.update(build_ped(curr['ped']))
    cnv = build_choroidalneovasc(curr['cnv'])
    results.update(cnv)
    results.update(build_subret_fibrous(curr['scar']))
    results.update(build_geoatrophy(curr['ga']))
    results.update(build_dryamd_severity(curr['dry']))
    results.update(build_wetamd_severity(
        curr['wet'],
        cnv_result=cnv,
        srh_result=srh,
        is_amd=None,
        is_dr=None,
        fluid_result=fluid,
    ))
    results.update(build_amd_vitamin(curr['vitamin']))
    # results.update(build_lasertype(curr['lasertype']))
    results.update(build_lasertype_new(data['common']['treatment']))
    results.update(build_amd_antivegf(data['common']['treatment']))
    return results


def get_amd(data):
    results = {
        'amd_re': 8,
        'amd_le': 8,
    }
    for item in data:
        laterality = laterality_from_int(item['laterality'])
        if {Laterality.OS, Laterality.OU} & {laterality}:
            results['amd_le'] = min(1, results['amd_le'])
        elif laterality:  # any mention
            results['amd_le'] = min(0, results['amd_le'])
        if {Laterality.OD, Laterality.OU} & {laterality}:
            results['amd_re'] = min(1, results['amd_re'])
        elif laterality:  # any mention
            results['amd_re'] = min(0, results['amd_re'])
    return results


def get_drusen(data):
    results = {
        'drusen_size_le': 'UNKNOWN',
        'drusen_size_re': 'UNKNOWN',
        'drusen_size_unk': 'UNKNOWN',
        'drusen_type_le': 'UNKNOWN',
        'drusen_type_re': 'UNKNOWN',
        'drusen_type_unk': 'UNKNOWN',
    }
    for k, v in data.items():
        results[k] = v['label'].upper()  # the last one is most specific, so overwrite
    return results


def get_subretinal_hemorrhage(data):
    return column_from_variable({
        'subretinal_hem_re': -1,
        'subretinal_hem_le': -1,
        'subretinal_hem_unk': -1,
    }, data)


def get_pigmentary_changes(data):
    return column_from_variable({
        'pigmentchanges_re': -1,
        'pigmentchanges_le': -1,
        'pigmentchanges_unk': -1,
    }, data)


def build_fluid(data, *, skip_rename_variable=False):
    # TODO: check if AMD
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
        renamevar_func=lambda x: x.replace('fluid', 'fluid_amd'),
        rename_func=None if skip_rename_variable else rename_fluid
    )


def build_intraretfluid(data):
    # TODO: check if AMD
    return column_from_variable(
        {
            'fluid_re': Fluid.UNKNOWN,
            'fluid_le': Fluid.UNKNOWN,
            'fluid_unk': Fluid.UNKNOWN,
        },
        data,
        transformer_func=Fluid,
        result_func=fluid_prioritization,
        filter_func=lambda x: x in {
            Fluid.INTRARETINAL_FLUID, Fluid.NO_INTRARETINAL_FLUID,
            Fluid.SUB_AND_INTRARETINAL_FLUID, Fluid.NO_SUB_AND_INTRARETINAL_FLUID,
        },
        enum_to_str=True,
        renamevar_func=lambda x: x.replace('fluid', 'amd_intraretfluid'),
        rename_func=rename_intraretfluid,
    )


def build_subretfluid(data):
    # TODO: check if AMD
    return column_from_variable(
        {
            'fluid_re': Fluid.UNKNOWN,
            'fluid_le': Fluid.UNKNOWN,
            'fluid_unk': Fluid.UNKNOWN,
        },
        data,
        transformer_func=Fluid,
        result_func=fluid_prioritization,
        filter_func=lambda x: x in {
            Fluid.SUBRETINAL_FLUID, Fluid.NO_SUBRETINAL_FLUID,
            Fluid.SUB_AND_INTRARETINAL_FLUID, Fluid.NO_SUB_AND_INTRARETINAL_FLUID,
        },
        enum_to_str=True,
        renamevar_func=lambda x: x.replace('fluid', 'amd_subretfluid'),
        rename_func=rename_subretfluid,
    )


def build_ped(data):
    """Build binary pigmentary epithelial detachment variable"""
    return column_from_variable(
        {
            'ped_re': PigEpiDetach.UNKNOWN,
            'ped_le': PigEpiDetach.UNKNOWN,
            'ped_unk': PigEpiDetach.UNKNOWN,
        },
        data,
        transformer_func=PigEpiDetach,
    )


def build_choroidalneovasc(data):
    """Build cnv/choroidal neovascularization as binary (yes/no/unknown)"""
    return column_from_variable(
        {
            'choroidalneovasc_re': ChoroidalNeoVasc.UNKNOWN,
            'choroidalneovasc_le': ChoroidalNeoVasc.UNKNOWN,
            'choroidalneovasc_unk': ChoroidalNeoVasc.UNKNOWN,
        },
        data,
        transformer_func=ChoroidalNeoVasc,
        compare_func=lambda n, c: c == ChoroidalNeoVasc.UNKNOWN,  # take first; only update unknown
    )


def build_subret_fibrous(data):
    """Build cnv/choroidal neovascularization as binary (yes/no/unknown)"""
    return column_from_variable(
        {
            'subret_fibrous_re': Scar.UNKNOWN,
            'subret_fibrous_le': Scar.UNKNOWN,
            'subret_fibrous_unk': Scar.UNKNOWN,
        },
        data,
        transformer_func=Scar,
        compare_func=lambda n, c: c == Scar.UNKNOWN,  # take first; only update unknown
        enum_to_str=True,
    )


def build_geoatrophy(data):
    """Build geographic atrophy as binary (yes/no/unknown)"""
    return column_from_variable(
        {
            'geoatrophy_re': GeoAtrophy.UNKNOWN,
            'geoatrophy_le': GeoAtrophy.UNKNOWN,
            'geoatrophy_unk': GeoAtrophy.UNKNOWN,
        },
        data,
        transformer_func=GeoAtrophy,
        compare_func=lambda n, c: c == GeoAtrophy.UNKNOWN,  # take first; only update unknown
        enum_to_str=False,  # store as int
    )


def build_dryamd_severity(data):
    """Build dry amd severity"""
    return column_from_variable(
        {
            'dryamd_severity_re': DrySeverity.UNKNOWN,
            'dryamd_severity_le': DrySeverity.UNKNOWN,
            'dryamd_severity_unk': DrySeverity.UNKNOWN,
        },
        data,
        transformer_func=DrySeverity,
        enum_to_str=True,
    )


def build_wetamd_severity(data, *, cnv_result=None, srh_result=None,
                          is_amd=None, is_dr=None, fluid_result=None):
    """Build wet amd severity"""
    result = column_from_variable(
        {
            'wetamd_severity_re': WetSeverity.UNKNOWN,
            'wetamd_severity_le': WetSeverity.UNKNOWN,
            'wetamd_severity_unk': WetSeverity.UNKNOWN,
        },
        data,
        transformer_func=WetSeverity,
        enum_to_str=True,
    )
    return augment_wetamd_severity(result, cnv_result=cnv_result, srh_result=srh_result,
                                   is_amd=is_amd, is_dr=is_dr, fluid_result=fluid_result)


def augment_wetamd_severity(result, *, cnv_result=None, srh_result=None,
                            is_amd=None, is_dr=None, fluid_result=None):
    result = update_column(result, cnv_result, [
        (ChoroidalNeoVasc, 'UNKNOWN', 'YES'),
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


def build_amd_vitamin(data):
    """Build amd vitamin"""
    return column_from_variable(
        {
            'amd_vitamin': Vitamin.UNKNOWN,
        },
        data,
        transformer_func=Vitamin,
        enum_to_str=False,
    )


def build_lasertype(data):
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

    return column_from_variable(
        {
            'amd_lasertype_re': Laser.UNKNOWN,
            'amd_lasertype_le': Laser.UNKNOWN,
            'amd_lasertype_unk': Laser.UNKNOWN,
        },
        data,
        transformer_func=Laser,
        enum_to_str=False,
        compare_func=_compare_lasertype,
    )


def build_lasertype_new(data):
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

    return column_from_variable(
        {
            'tx_re': Treatment.UNKNOWN,
            'tx_le': Treatment.UNKNOWN,
            'tx_unk': Treatment.UNKNOWN,
        },
        data,
        renamevar_func=lambda x: f'amd_lasertype_{x.split("_")[-1]}',
        rename_func=_rename_lasertype,
        filter_func=lambda x: x.get('category', None) in {'AMD'},
        transformer_func=Treatment,
        enum_to_str=False,
        compare_func=_compare_lasertype,
    )


def build_amd_antivegf(data):
    # TODO: check is AMD

    return column_from_variable(
        {
            'tx_re': AntiVegf.UNKNOWN,
            'tx_le': AntiVegf.UNKNOWN,
            'tx_unk': AntiVegf.UNKNOWN,
        },
        data,
        renamevar_func=lambda x: f'amd_antivegf_{x.split("_")[-1]}',
        rename_func=rename_antivegf,
        filter_func=lambda x: x.get('category', None) in {'ANTIVEGF'},
        transformer_func=AntiVegf,
        enum_to_str=False,
    )
