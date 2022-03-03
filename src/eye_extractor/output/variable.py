def column_from_variable(results, data, *, compare_func=None, transformer_func=None, result_func=None):
    """
    Assuming values that can be graded according to a comparator functions,
        converts the results of `create_new_variable` into only that with the
        'highest' value (where 'highest' is the result of the comparator)

    Compare_func asks 'given the existing value and this new value, should we change something (T/F)
    Result_func asks 'given the existing value and this new value, what should be the result?'

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
        transformer_func = lambda n: n  # no deserialization required
    for row in data:
        for varname, curr_value in results.items():
            new_value = transformer_func(row[varname])
            if varname in row and compare_func(new_value, curr_value):
                results[varname] = result_func(new_value, curr_value)
    return results
