import re

from loguru import logger


class ValidatorError(Exception):
    pass


def equals(*options):
    """Exactly equals one of these options"""
    options = set(options)

    def _equals(val, *error_messages):
        if val in options:
            pass
        else:
            raise ValidatorError(f'Value {val} not in {options}: {", ".join(error_messages)}')

    return _equals


def is_int(val, *error_messages):
    if not isinstance(val, int):
        raise ValidatorError(f'Value {val} is not an int: {", ".join(error_messages)}')


def is_date(val, *error_messages):
    if not isinstance(val, str) or not re.match(r'\d{4}-\d{2}-\d{2}', val):
        raise ValidatorError(f'Value {val} is not a valid date: {", ".join(error_messages)}')


def is_string(val, *error_messages):
    if not isinstance(val, str):
        raise ValidatorError(f'Value {val} is not a valid string: {", ".join(error_messages)}')


def is_upper(val, *error_messages):
    is_string(val, *error_messages)
    if re.search(r'[a-z]', val):
        raise ValidatorError(f'Value {val} is not an uppercased string: {", ".join(error_messages)}')


def is_in_range(start, end):
    """Inclusive range check"""

    def _is_in_range(val, *error_messages):
        is_int(val, *error_messages)
        if start <= val <= end:
            pass
        else:
            raise ValidatorError(f'Value {val} is not in int range {start}, {end}: {", ".join(error_messages)}')

    return _is_in_range


def is_float_in_range(start, end):
    """Inclusive range check"""

    def _is_float_in_range(val, *error_messages):
        if start <= val <= end:
            pass
        else:
            raise ValidatorError(f'Value {val} is not in float range {start}, {end}: {", ".join(error_messages)}')

    return _is_float_in_range


def contains(*choices):
    def _contains(val, *error_messages):
        if val not in choices:
            raise ValidatorError(f'Value {val} is not in choices {", ".join(choices)}: {", ".join(error_messages)}')

    return _contains


def is_string_in_enum(*enums):
    """Check for elementst converted using `enum_to_string` argument in `column_to_variable`

    enums: IntEnum elements
    """
    def _is_string_in_enum(val, *error_messages):
        for enum in enums:
            for item in enum:
                if val == item.name.replace('_', ' '):
                    return True
        raise ValidatorError(
            f'Value {val} not in enum names for {", ".join(str(x) for x in enums)}: {", ".join(error_messages)}'
        )
    return _is_string_in_enum


def is_int_in_enum(*enums):
    """Check for elementst converted using `enum_to_string` argument in `column_to_variable`

    enums: IntEnum elements
    """
    def _is_int_in_enum(val, *error_messages):
        for enum in enums:
            for item in enum:
                if val == item.value:
                    return True
        raise ValidatorError(
            f'Value {val} not in enum values for {", ".join(str(x) for x in enums)}: {", ".join(error_messages)}'
        )
    return _is_int_in_enum


def validate_columns_in_row(column_dict, data, *, strict=False, id_col=None, logical_or=True):
    if id_col:
        id_col = str(data[id_col])
    else:
        id_col = ''
    if logical_or:
        _validate_columns_in_row_or(column_dict, data, strict=strict, id_col=id_col)
    else:
        _validate_columns_in_row_and(column_dict, data, strict=strict, id_col=id_col)


def _validate_columns_in_row_or(column_dict, data, *, strict=False, id_col=None):
    """OR the various columns -- only one must match"""
    for col, val in data.items():
        curr_errors = []
        if col not in column_dict:
            logger.warning(f'Missing column: {col}. Add to output list in `columns.py`.')
            continue
        for validator in column_dict[col]:
            try:
                validator(val, id_col)
            except ValidatorError as ve:
                curr_errors.append(ve)
            else:
                curr_errors = None
                break
        if curr_errors:
            logger.error(f'For column {col}: {", ".join(str(ve) for ve in curr_errors)}')
            if strict:
                raise curr_errors[-1]


def _validate_columns_in_row_and(column_dict, data, *, strict=False, id_col=None):
    """AND the various columns -- all must match"""
    for col, val in data.items():
        for validator in column_dict[col]:
            try:
                validator(val, id_col)
            except ValidatorError as ve:
                logger.error(f'For column {col}: {str(ve)}')
                if strict:
                    raise ve
