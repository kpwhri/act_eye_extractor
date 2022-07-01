"""
`column_from_variable` automates the construction of variables in the output table
    that have been built with `create_new_variable`.

Example use case.
Let's suppose we have the input text 'PCIOL od, ac iol os'
    and we want to identify PCIOL and ACIOL.
The data from the extract method looks something like the below.
    Note particularly this is a list, so if multiple values are found the 'best' will be determined
    by the larger (`compare_func`, defaults to new > old, which will compare IntEnum values)
[
    {'intraocular_lens_re':
        {'value': <IolLens.PCIOL: 2>,  # NB: this is an IntEnum
         'term': 'PCIOL',
         'label': 'yes',
         'regex': 'PCIOL_PAT',
         'source': 'LENS'}
        },
    {'intraocular_lens_le':
        {'value': <IolLens.ACIOL: 4>,  # NB: this is an IntEnum
         'term': 'ac iol',
         'label': 'yes',
         'regex': 'ACIOL_PAT',
         'source': 'LENS'
        }
]

The `column_from_variable` will create a simple results dict that looks like:
* {'intraocular_lens_re': 'PCIOL', 'intraocular_lens_le': 'ACIOL'}

When it is written and subsequently read from json output, it is identical, except that the
    IntEnums have been converted to ints:
        * 'value': <IolLens.PCIOL: 2> -> 'value': 2
        * 'value': <IolLens.ACIOL: 4> -> 'value': 4

For the building, each of the elements in the list (n=2 in this case), are read into this function:
    column_from_variable(
        {  # initialize values; note IolLens.UNKNOWN = -1, so it will ALWAYS be replaced by something else
            'intraocular_lens_re': IolLens.UNKNOWN,
            'intraocular_lens_le': IolLens.UNKNOWN,
        },
        data,
        transformer_func=lambda x: IolLens(x['value']),  # x['value'] gets the 2/4 and converts it back to Enum
        enum_to_str=True,  # convert the IolLens enum values to strings (e.g., 'PCIOL', and 'ACIOL') to be
                           #   written to output file; default is to write the integer value if it is an Enum
    )

When checking to see if the default (IolLens.UNKNOWN) should be updated, we can modify its behavior.
* Input value from dict (from json). By default, will just grab the value or x['value'] if it's a dict:
    {'intraocular_lens_re': 4}  -> value
    {'intraocular_lens_re': {'value': 4}}  -> x['value']]
    - use `transformer_func` to modify:
        To convert the first (above) from int to IntEnum: lambda x: IolLens(x)
        To convert the second (above) from int to IntEnum: lambda x: IolLens(x['value'])

* To change the column/variable name (we've been looking at the variable name `intraocular_lens_re|le`).
    - use `convert_func` (defaults to lambda n: n; returns the new variable name)
        To convert 'intraocular_lens_re' to an abbreviated form for the output, use, e.g.:
            lambda x: x.replace('intraocular_lens', 'iol')

* To only include certain elements (e.g., in cataract severity, we want to look at each cataract type individually)
    - use `filter_func` to specify what to include (returns a bool)
        To only include values > 3 (ACIOL, but no PCIOL): lambda x: x > 3

* If you want to change how values are compared, use `compare_func` (returns bool)
    Suppose that if PCIOL (value=2) and ACIOL (value=4), you want to modify to PCIOL_ACIOL
            (this is hypothetical, but used for FLUID)
        compare_func=lambda new, current: new > current or current.value == 4 and new.value == 2
            `new > current` will return true if ACIOL is the new item and PCIOL is the old since 4 > 2
            `current.value == 4 and new.value == 2` will return true if PCIOL (2) is the new item and ACIOL is the old (4)
    You will then need to use the `result_func` to actually merge the values (see next)

* If you want to then merge ACIOL and PCIOL into ACIOL_PCIOL:
    1. first `compare_func` must be used to say that a change is required
    2. second, `result_func` (discussed here) will merge the two variables
    result_func=lambda new, current: IolLens.ACIOL_PCIOL if {new, current} == {IolLens.ACIOL, IolLens.PCIOL} else new
    NB: These can get very complicated, so it might be worth extracting to a separate function:
    def _result_func(new, current):
        if {new, current} == {IolLens.ACIOL, IolLens.PCIOL}:
            return IolLens.ACIOL_PCIOL
        else:  # we can only reach here if either ACIOL/PCIOL or if new > current due to compare_func
            return new

* If you want to rename the final outputs, like to lowercase the enum values
    By default, IntEnum will return its value (int/numeric)
    Specify `enum_to_str` to return its name (str)
    - use `rename_func` (returns string of new name)
        To return 'pciol' instead of 'PCIOL', specify:
            rename_func=lambda x: x.name.lower(),

"""
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

    :param convert_func: change the variable/column name from what it was supplied; this is what variable will be output
    :param filter_func: returns bool; only consider values in which this returns True
    :param rename_func: rename the final values after doing all processing
    :param enum_to_str: if result is enum, convert to string; otherwise, convert to int value
    :param transformer_func: function to return serialized results to desired object
        most commonly this might be an IntEnum
    :param result_func: function that gives the new result (e.g., new intenum, etc.)
    :param results: initial values
    :param data: dict-like (read from json)
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
    for row in data:  # for each element in list read from json file
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
