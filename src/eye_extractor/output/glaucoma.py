from eye_extractor.common.algo.treatment import Treatment
from eye_extractor.common.drug.drops import GenericDrop
from eye_extractor.exam.gonio import Gonio
from eye_extractor.glaucoma.dx import GlaucomaType
from eye_extractor.glaucoma.exfoliation import Exfoliation
from eye_extractor.glaucoma.preglaucoma import Preglaucoma
from eye_extractor.glaucoma.tx import GlaucomaTreatment
from eye_extractor.output.variable import column_from_variable, has_valid_date, column_from_variable_abbr


def build_glaucoma(data):
    results = {}
    if not data.get('glaucoma', None):
        return results
    curr = data['glaucoma']
    note = data['note']
    results.update(build_glaucoma_drops(curr['drops'], note_date=note['date']))
    results.update(build_glaucoma_dx(curr['dx'], note_date=note['date']))
    results.update(build_gonio(curr.get('gonio', None), note_date=note['date']))
    results.update(build_cct(curr.get('cct', None), note_date=note['date']))
    results.update(build_disc_hem(curr.get('disc_hem', None), note_date=note['date']))
    results.update(build_disc_notch(curr.get('disc_notch', None), note_date=note['date']))
    results.update(build_tilted_disc(curr.get('tilted_disc', None), note_date=note['date']))
    results.update(build_ppa(curr.get('ppa', None), note_date=note['date']))
    # results.update(build_tx(curr.get('tx', None)))
    results.update(build_tx_new(data['common']['treatment'], note_date=note['date']))
    results.update(build_exfoliation(curr.get('exfoliation', None), note_date=note['date']))
    results.update(build_preglaucoma_dx(curr.get('preglaucoma', None), note_date=note['date']))
    results.update(build_disc_pallor(curr.get('disc_pallor', None), note_date=note['date']))
    return results


def build_glaucoma_drops(data, *, note_date=None):
    results = {f'glaucoma_rx_{x.name.lower()}': -1 for x in GenericDrop if x.name != 'UNKNOWN'}
    for record in data:
        for key, value in record.items():
            if has_valid_date(note_date, value):
                results[key] = value['value']
    return results


def _build_glaucoma_dx_sideeffect_func(results, varname, newvalue):
    """Set dx to GLAUCOMA if a glaucoma type found"""
    if 'glaucoma_type' in varname and newvalue != GlaucomaType.NONE:
        results[f'glaucoma_dx_{varname.split("_")[-1]}'] = GlaucomaType.GLAUCOMA


def build_glaucoma_dx(data, *, note_date=None):
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
        restrict_date=note_date,
        transformer_func=GlaucomaType,
        enum_to_str=True,
        # compare: only update an unknown or auto-fill Glaucoma
        compare_func=lambda n, c: c in {
            GlaucomaType.UNKNOWN, GlaucomaType.GLAUCOMA,
        },
        sideeffect_func=_build_glaucoma_dx_sideeffect_func,
    )


def build_gonio(data, *, note_date=None):
    return column_from_variable_abbr(
        'gonio', Gonio.UNKNOWN, data,
        restrict_date=note_date,
        transformer_func=Gonio,
        enum_to_str=True,
    )


def build_cct(data, *, note_date=None):
    return column_from_variable_abbr(
        'centralcornealthickness', -1, data,
        restrict_date=note_date,
        compare_func=lambda new, current: current == -1,  # only update defaults
    )


def build_disc_hem(data, *, note_date=None):
    """
    Build disc hemorrhage into 1=yes, 0=no, -1=unknown
    Default comparison is used to only retain greatest (i.e., any yes)
    :param note_date:
    :param data:
    :return:
    """
    return column_from_variable_abbr(
        'disc_hem', -1, data,
        restrict_date=note_date,
    )


def build_disc_notch(data, *, note_date=None):
    """
    Build disc notch into 1=yes, 0=no, -1=unknown
    Default comparison is used to only retain greatest (i.e., any yes)
    :param note_date:
    :param data:
    :return:
    """
    return column_from_variable_abbr(
        'disc_notch', -1, data,
        restrict_date=note_date,
    )


def build_tilted_disc(data, *, note_date=None):
    """
    Build tilted disc into 1=yes, 0=no, -1=unknown
    Default comparison is used to only retain greatest (i.e., any yes)
    :param note_date:
    :param data:
    :return:
    """
    return column_from_variable_abbr(
        'tilted_disc', -1, data,
        restrict_date=note_date,
    )


def build_ppa(data, *, note_date=None):
    """
    Build perpapillary atrophy into 1=yes, 0=no, -1=unknown
    Default comparison is used to only retain greatest (i.e., any yes)
    :param note_date:
    :param data:
    :return:
    """
    return column_from_variable_abbr(
        'ppa', -1, data,
        restrict_date=note_date,
    )


def build_tx(data, *, note_date=None):
    """
    Build treatment plan into GlacuomaTreatment variable
    Default comparison is used to only retain greatest (i.e., any yes)
    :param note_date:
    :param data:
    :return:
    """
    return column_from_variable_abbr(
        'glaucoma_tx', GlaucomaTreatment.UNKNOWN, data,
        restrict_date=note_date,
        transformer_func=GlaucomaTreatment,
        enum_to_str=True,
        # compare: only update an unknown
        compare_func=lambda n, c: c in {
            GlaucomaTreatment.UNKNOWN, GlaucomaTreatment.NONE
        },
    )


def build_tx_new(data, *, note_date=None):
    """
    Build treatment plan into Treatment variable
    Default comparison is used to only retain greatest (i.e., any yes)
    :param note_date:
    :param data:
    :return:
    """
    # TODO: check if this note is about glaucoma
    return column_from_variable_abbr(
        'tx', Treatment.UNKNOWN, data,
        restrict_date=note_date,
        filter_func=lambda x: x.get('category', 'ALL') in {'ALL', 'GLAUCOMA'},
        renamevar_func=lambda x: f'glaucoma_{x}',
        transformer_func=Treatment,
        enum_to_str=True,
        # compare: only update an unknown
        compare_func=lambda n, c: c in {
            Treatment.UNKNOWN, Treatment.NONE
        },
    )


def build_exfoliation(data, *, note_date=None):
    """
    Build exfoliation (non-glaucoma)
    Default comparison is used to only retain greatest (i.e., any yes)
    :param note_date:
    :param data:
    :return:
    """
    return column_from_variable_abbr(
        'exfoliation', Exfoliation.UNKNOWN,
        data,
        restrict_date=note_date,
        transformer_func=Exfoliation,
    )


def build_preglaucoma_dx(data, *, note_date=None):
    """
    Build exfoliation (non-glaucoma)
    Default comparison is used to only retain greatest (i.e., any yes)
    :param note_date:
    :param data:
    :return:
    """
    return column_from_variable_abbr(
        'preglaucoma', Preglaucoma.UNKNOWN, data,
        restrict_date=note_date,
        enum_to_str=True,
        transformer_func=Preglaucoma,
        compare_func=lambda n, c: c in {
            Preglaucoma.UNKNOWN, Preglaucoma.NONE
        },
    )


def build_disc_pallor(data, *, note_date=None):
    """
    Build disc notch into 1=yes, 0=no, -1=unknown
    Default comparison is used to only retain greatest (i.e., any yes)
    :param note_date:
    :param data:
    :return:
    """
    return column_from_variable_abbr(
        'disc_pallor_glaucoma', -1, data,
        restrict_date=note_date,
    )
