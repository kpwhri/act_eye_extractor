import re

from loguru import logger


class ValidatorError(Exception):
    pass


def is_int(val, *error_messages):
    if not isinstance(val, int):
        raise ValidatorError(f'Value {val} is not an int: {", ".join(error_messages)}')


def is_date(val, *error_messages):
    if not isinstance(val, str) or not re.match(r'\d{4}-\d{2}-\d{2}', val):
        raise ValidatorError(f'Value {val} is not a valid date: {", ".join(error_messages)}')


def is_in_range(start, end):
    def _is_in_range(val, *error_messages):
        is_int(val, *error_messages)
        if start <= val <= end:
            pass
        else:
            raise ValidatorError(f'Value {val} is not in range {start}, {end}: {", ".join(error_messages)}')

    return _is_in_range


def contains(*choices):
    def _contains(val, *error_messages):
        if val not in choices:
            raise ValidatorError(f'Value {val} is not in choices {", ".join(choices)}: {", ".join(error_messages)}')

    return _contains


def validate_columns_in_row(column_dict, data, *, strict=False, id_col=None):
    if id_col:
        id_col = str(data[id_col])
    else:
        id_col = ''
    for col, val in data.items():
        for validator in column_dict[col]:
            try:
                validator(val, id_col)
            except ValidatorError as ve:
                logger.exception(ve)
                if strict:
                    raise ve
