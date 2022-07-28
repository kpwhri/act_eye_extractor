from eye_extractor.amd.cnv import ChoroidalNeoVasc
from eye_extractor.amd.dry import DrySeverity
from eye_extractor.amd.fluid import FluidAMD, fluid_prioritization
from eye_extractor.amd.ga import GeoAtrophy
from eye_extractor.amd.ped import PigEpiDetach
from eye_extractor.amd.scar import Scar
from eye_extractor.amd.wet import WetSeverity
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
