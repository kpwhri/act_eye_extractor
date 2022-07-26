from eye_extractor.amd.cnv import ChoroidalNeoVasc
from eye_extractor.amd.fluid import FluidAMD, fluid_prioritization
from eye_extractor.amd.ped import PigEpiDetach
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
