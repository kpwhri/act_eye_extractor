from enum import Enum


def column_from_variable(results, data, *, compare_func=None, transformer_func=None,
                         result_func=None, convert_func=None, filter_func=None,
                         rename_func=None, enum_to_str=False):
    """
    Assuming values that can be graded according to a comparator functions,
        converts the results of `create_new_variable` into only that with the
        'highest' value (where 'highest' is the result of the comparator)

    Compare_func asks 'given the existing value and this new value, should we change something (T/F)
    Result_func asks 'given the existing value and this new value, what should be the result?'

    :param convert_func:
    :param filter_func:
    :param rename_func:
    :param enum_to_str: if result is enum, convert to string; otherwise, convert to int value
    :param transformer_func: function to return serialized results to desired object
        most commonly this might be an IntEnum
    :param result_func: function that gives the new result (e.g., new intenum, etc.)
    :param results:
    :param data:
    :param compare_func: given two results X and Y, return True if X is better than Y
    :return:
    """
    if compare_func is None:
        compare_func = lambda n, c: n > c  # default to New > Current
    if result_func is None:
        result_func = lambda n, c: n  # default to return New value
    if transformer_func is None:
        # no deserialization required (or created with `create_variable` function)
        transformer_func = lambda n: n['value'] if isinstance(n, dict) else n
    if filter_func is None:  # inclusion criteria
        filter_func = lambda n: n
    if convert_func is None:  # if using different names (want different output name)
        convert_func = lambda n: n
    if rename_func is None:  # final renaming of variable after processing
        if enum_to_str:  # convert result enum to string value, replace underscore
            rename_func = lambda n: n.name.replace('_', ' ') if isinstance(n, Enum) else n
        else:
            rename_func = lambda n: n.value if isinstance(n, Enum) else n
    for row in data:
        for varname, curr_value in results.items():
            target_varname = convert_func(varname)
            if target_varname not in row:
                continue
            if not filter_func(row[target_varname]):  # apply inclusion criteria in filter func
                continue
            new_value = transformer_func(row[target_varname])
            if compare_func(new_value, curr_value):
                results[varname] = result_func(new_value, curr_value)
    return {varname: rename_func(value) for varname, value in results.items()}


def column_from_variable_binary(data, label):
    return column_from_variable({f'{label}_le': -1, f'{label}_re': -1}, data)
