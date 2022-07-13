from eye_extractor.cataract.cataract_type import CataractType
from eye_extractor.cataract.intraocular_lens import IolLens
from eye_extractor.cataract.posterior_cap_opacity import PosteriorCapsuleOpacity
from eye_extractor.output.variable import column_from_variable, column_from_variable_binary


def build_cataract_variables(data):
    curr = data['cataract']
    results = {}
    results.update(build_cataract(curr['cataract']))
    results.update(build_cataract_type(curr['cataract_type']))
    results.update(build_nscataract_severity(curr['cataract_type']))
    results.update(build_cortcataract_severity(curr['cataract_type']))
    results.update(build_pscataract_severity(curr['cataract_type']))
    results.update(build_intraocular_lens(curr['intraocular_lens']))
    results.update(build_posterior_cap_opacity(curr['posterior_cap_opacity']))
    return results


def build_cataract(data):
    return column_from_variable_binary(data, 'cataractiol_yesno')


def build_cataract_type(data):
    return column_from_variable(
        {
            'cataract_type_re': CataractType.UNKNOWN,
            'cataract_type_le': CataractType.UNKNOWN,
        },
        data,
        transformer_func=lambda x: CataractType(x['value']) if isinstance(x, dict) else CataractType(x),
    )


def build_nscataract_severity(data):
    return build_cataract_severity(data, 'ns', CataractType.NS)


def build_cortcataract_severity(data):
    return build_cataract_severity(data, 'cort', CataractType.CS, CataractType.ACS)


def build_pscataract_severity(data):
    return build_cataract_severity(data, 'ps', CataractType.PSC)


def build_cataract_severity(data, label, *cataracttypes):
    return column_from_variable(
        {
            f'{label}cataract_severity_re': -1,
            f'{label}cataract_severity_le': -1,
        },
        data,
        transformer_func=lambda n: float(n['severity']),
        filter_func=lambda n: n['value'] in {ctype.value for ctype in cataracttypes},
        convert_func=lambda n: f'cataract_type_{n[-2:]}',
    )


def build_intraocular_lens(data):
    return column_from_variable(
        {
            'intraocular_lens_re': IolLens.UNKNOWN,
            'intraocular_lens_le': IolLens.UNKNOWN,
        },
        data,
        transformer_func=lambda x: IolLens(x['value']),
        enum_to_str=True,
    )


def build_posterior_cap_opacity(data):
    return column_from_variable(
        {
            'posterior_cap_opacity_re': PosteriorCapsuleOpacity.NO_INDICATION,
            'posterior_cap_opacity_le': PosteriorCapsuleOpacity.NO_INDICATION,
        },
        data,
        transformer_func=lambda x: PosteriorCapsuleOpacity(x['value']),
        rename_func=lambda x: {
            'P1': '1+',
            'P2': '2+',
            'P3': '3+',
            'P4': '4+',
            'TRACE': 'tr',
        }.get(x.name, x.name.lower().replace('_', ' '))
    )
