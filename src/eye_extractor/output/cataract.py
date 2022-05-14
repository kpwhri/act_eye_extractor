from eye_extractor.cataract.cataract_type import CataractType
from eye_extractor.output.variable import column_from_variable, column_from_variable_binary


def build_cataract_variables(data):
    curr = data['cataract']
    results = {}
    results.update(build_cataract(curr))
    results.update(build_cataract_type(curr))
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
        transformer_func=CataractType,
    )


def build_nscataract_severity(data):
    return column_from_variable(
        {
            'nscataract_severity_re': -1,
            'nscataract_severity_le': -1,
        },
        data,
        transformer_func=lambda n: n['severity'],
        filter_func=lambda n: n['value'] == CataractType.NS.value,
        convert_func=lambda n: f'cataract_type_{n[-2:]}',
    )
