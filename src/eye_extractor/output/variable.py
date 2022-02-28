def column_from_variable(results, data, compare_func=None):
    """
    Assuming values that can be graded according to a comparator functions,
        converts the results of `create_new_variable` into only that with the
        'highest' value (where 'highest' is the result of the comparator)

    :param results:
    :param data:
    :param compare_func: given two results X and Y, return True if X is better than Y
    :return:
    """
    if compare_func is None:
        compare_func = lambda x, y: x > y
    for row in data:
        for varname, value in results.items():
            if varname in row and compare_func(row[varname], value):
                results[varname] = row[varname]
    return results
