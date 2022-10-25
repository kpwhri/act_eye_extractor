from eye_extractor.cataract.cataract_type import CataractType
from eye_extractor.cataract.intraocular_lens import IolLens
from eye_extractor.cataract.posterior_cap_opacity import PosteriorCapsuleOpacity
from eye_extractor.output.variable import column_from_variable_binary, column_from_variable_abbr


def build_cataract_variables(data):
    curr = data['cataract']
    note = data['note']
    results = {}
    results.update(build_cataract(curr['cataract'], note_date=note['date']))
    results.update(build_cataract_type(curr['cataract_type'], note_date=note['date']))
    results.update(build_nscataract_severity(curr['cataract_type'], note_date=note['date']))
    results.update(build_cortcataract_severity(curr['cataract_type'], note_date=note['date']))
    results.update(build_pscataract_severity(curr['cataract_type'], note_date=note['date']))
    results.update(build_intraocular_lens(curr['intraocular_lens'], note_date=note['date']))
    results.update(build_posterior_cap_opacity(curr['posterior_cap_opacity'], note_date=note['date']))
    return results


def build_cataract(data, *, note_date=None):
    return column_from_variable_binary(data, 'cataractiol_yesno', restrict_date=note_date)


def build_cataract_type(data, *, note_date=None):
    return column_from_variable_abbr(
        'cataract_type', CataractType.UNKNOWN, data,
        transformer_func=CataractType,
        restrict_date=note_date,
    )


def build_nscataract_severity(data, *, note_date=None):
    return build_cataract_severity(data, 'ns', CataractType.NS, note_date=note_date)


def build_cortcataract_severity(data, *, note_date=None):
    return build_cataract_severity(data, 'cort', CataractType.CS, CataractType.ACS, note_date=note_date)


def build_pscataract_severity(data, *, note_date=None):
    return build_cataract_severity(data, 'ps', CataractType.PSC, note_date=note_date)


def build_cataract_severity(data, label, *cataracttypes, note_date=None):
    return column_from_variable_abbr(
        f'{label}cataract_severity', -1, data,
        restrict_date=note_date,
        transformer_func=lambda n: float(n['severity']),
        filter_func=lambda n: n['value'] in {ctype.value for ctype in cataracttypes},
        convert_func=lambda n: f'cataract_type_{n[-2:]}',
    )


def build_intraocular_lens(data, *, note_date=None):
    return column_from_variable_abbr(
        'intraocular_lens', IolLens.UNKNOWN, data,
        restrict_date=note_date,
        transformer_func=IolLens,
        enum_to_str=True,
    )


def build_posterior_cap_opacity(data, *, note_date=None):
    return column_from_variable_abbr(
        'posterior_cap_opacity', PosteriorCapsuleOpacity.NO_INDICATION, data,
        restrict_date=note_date,
        transformer_func=PosteriorCapsuleOpacity,
        rename_func=lambda x: {
            'P1': '1+',
            'P2': '2+',
            'P3': '3+',
            'P4': '4+',
            'TRACE': 'tr',
        }.get(x.name, x.name.lower().replace('_', ' '))
    )
