from eye_extractor.exam.gonio import Gonio
from eye_extractor.glaucoma.drops import GenericDrop
from eye_extractor.glaucoma.dx import GlaucomaType, GlaucomaDx
from eye_extractor.output.variable import column_from_variable


def build_glaucoma(data):
    results = {}
    curr = data['glaucoma']
    results.update(build_glaucoma_drops(curr['drops']))
    results.update(build_glaucoma_dx(curr['dx']))
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
        transformer_func=lambda x: GlaucomaType(x['value']),
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
