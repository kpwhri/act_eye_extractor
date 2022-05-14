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
