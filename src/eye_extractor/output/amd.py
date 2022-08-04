from eye_extractor.amd.cnv import ChoroidalNeoVasc
from eye_extractor.amd.dry import DrySeverity
from eye_extractor.amd.fluid import FluidAMD, fluid_prioritization
from eye_extractor.amd.ga import GeoAtrophy
from eye_extractor.amd.lasertype import Laser
from eye_extractor.amd.ped import PigEpiDetach
from eye_extractor.amd.scar import Scar
from eye_extractor.amd.vitamins import Vitamin
from eye_extractor.amd.wet import WetSeverity
from eye_extractor.common.algo.treatment import Treatment
from eye_extractor.output.laterality import laterality_from_int
from eye_extractor.laterality import Laterality
from eye_extractor.output.variable import column_from_variable


def build_amd_variables(data):
    curr = data['amd']
    results = {}
    results.update(get_amd(curr['amd']))
    results.update(get_drusen(curr['drusen']))
    results.update(get_subretinal_hemorrhage(curr['srh']))
    results.update(get_pigmentary_changes(curr['pigment']))
    results.update(get_fluid_from_variable(curr['fluid']))
    results.update(build_ped(curr['ped']))
    results.update(build_choroidalneovasc(curr['cnv']))
    results.update(build_subret_fibrous(curr['scar']))
    results.update(build_geoatrophy(curr['ga']))
    results.update(build_dryamd_severity(curr['dry']))
    results.update(build_wetamd_severity(curr['wet']))
    results.update(build_amd_vitamin(curr['vitamin']))
    results.update(build_lasertype(curr['lasertype']))
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
    results = {}
    for k, v in data.items():
        results[k] = v['label'].upper()
    return results


def get_subretinal_hemorrhage(data):
    return column_from_variable({
        'subretinal_hem_re': -1,
        'subretinal_hem_le': -1,
    }, data)


def get_pigmentary_changes(data):
    return column_from_variable({
        'pigmentchanges_re': -1,
        'pigmentchanges_le': -1,
    }, data)


def get_fluid_from_variable(data):
    return column_from_variable(
        {
            'fluid_amd_re': FluidAMD.UNKNOWN,
            'fluid_amd_le': FluidAMD.UNKNOWN,
            'fluid_amd_unk': FluidAMD.UNKNOWN,
        },
        data,
        transformer_func=FluidAMD,
        result_func=fluid_prioritization,
        enum_to_str=True,
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


def build_wetamd_severity(data):
    """Build wet amd severity"""
    return column_from_variable(
        {
            'wetamd_severity_re': WetSeverity.UNKNOWN,
            'wetamd_severity_le': WetSeverity.UNKNOWN,
            'wetamd_severity_unk': WetSeverity.UNKNOWN,
        },
        data,
        transformer_func=WetSeverity,
        enum_to_str=True,
    )


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
