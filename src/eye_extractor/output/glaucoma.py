from eye_extractor.exam.gonio import Gonio
from eye_extractor.glaucoma.drops import GenericDrop
from eye_extractor.glaucoma.dx import GlaucomaType
from eye_extractor.output.variable import column_from_variable


def build_glaucoma(data):
    results = {}
    curr = data['glaucoma']
    results.update(build_glaucoma_drops(curr['drops']))
    results.update(build_glaucoma_dx(curr['dx']))
    results.update(build_gonio(curr['gonio']))
    results.update(build_cct(curr['cct']))
    return results


def build_glaucoma_drops(data):
    results = {f'glaucoma_rx_{x.name.lower()}': -1 for x in GenericDrop if x.name != 'UNKNOWN'}
    for record in data:
        for key, value in record.items():
            results[key] = value['value']
    return results


def _build_glaucoma_dx_sideeffect_func(results, varname, newvalue):
    """Set dx to GLAUCOMA if a glaucoma type found"""
    if 'glaucoma_type' in varname and newvalue != GlaucomaType.NONE:
        results[f'glaucoma_dx_{varname.split("_")[-1]}'] = GlaucomaType.GLAUCOMA


def build_glaucoma_dx(data):
    return column_from_variable(
        {
            'glaucoma_dx_re': GlaucomaType.UNKNOWN,
            'glaucoma_dx_le': GlaucomaType.UNKNOWN,
            'glaucoma_dx_unk': GlaucomaType.UNKNOWN,
            'glaucoma_type_re': GlaucomaType.UNKNOWN,
            'glaucoma_type_le': GlaucomaType.UNKNOWN,
            'glaucoma_type_unk': GlaucomaType.UNKNOWN,
        },
        data,
        transformer_func=GlaucomaType,
        enum_to_str=True,
        # compare: only update an unknown or auto-fill Glaucoma
        compare_func=lambda n, c: c in {
            GlaucomaType.UNKNOWN, GlaucomaType.GLAUCOMA,
        },
        sideeffect_func=_build_glaucoma_dx_sideeffect_func,
    )


def build_gonio(data):
    return column_from_variable(
        {
            'gonio_re': Gonio.UNKNOWN,
            'gonio_le': Gonio.UNKNOWN,
            'gonio_unk': Gonio.UNKNOWN,
        },
        data,
        transformer_func=Gonio,
        enum_to_str=True,
    )


def build_cct(data):
    return column_from_variable(
        {
            'centralcornealthickness_re': -1,
            'centralcornealthickness_le': -1,
            'centralcornealthickness_unk': -1,
        },
        data,
        compare_func=lambda new, current: current == -1,  # only update defaults
    )


def build_disc_hem(data):
    """
    Build disc hemorrhage into 1=yes, 0=no, -1=unknown
    Default comparison is used to only retain greatest (i.e., any yes)
    :param data:
    :return:
    """
    return column_from_variable(
        {
            'disc_hem_re': -1,
            'disc_hem_le': -1,
            'disc_hem_unk': -1,
        },
        data,
    )


def build_disc_notch(data):
    """
    Build disc notch into 1=yes, 0=no, -1=unknown
    Default comparison is used to only retain greatest (i.e., any yes)
    :param data:
    :return:
    """
    return column_from_variable(
        {
            'disc_notch_re': -1,
            'disc_notch_le': -1,
            'disc_notch_unk': -1,
        },
        data,
    )


def build_tilted_disc(data):
    """
    Build tilted disc into 1=yes, 0=no, -1=unknown
    Default comparison is used to only retain greatest (i.e., any yes)
    :param data:
    :return:
    """
    return column_from_variable(
        {
            'tilted_disc_re': -1,
            'tilted_disc_le': -1,
            'tilted_disc_unk': -1,
        },
        data,
    )


def build_ppa(data):
    """
    Build perpapillary atrophy into 1=yes, 0=no, -1=unknown
    Default comparison is used to only retain greatest (i.e., any yes)
    :param data:
    :return:
    """
    return column_from_variable(
        {
            'ppa_re': -1,
            'ppa_le': -1,
            'ppa_unk': -1,
        },
        data,
    )
