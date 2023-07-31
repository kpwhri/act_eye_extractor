from typing import Callable

from eye_extractor.laterality import build_laterality_table


def get_variable(text: str, get_helper: Callable, *,
                 headers=None, lateralities=None, search_negated_list=False) -> list:
    """General function for extracting variables from text.

    General template for extracting variables from a given text. Requires a helper function to perform the extraction.

    :param text: Text to search for unspecified negated list items.
    :param get_helper: Helper function used to specify extraction behavior.
    :param headers:
    :param lateralities:
    :param search_negated_list: If True, search for negated lists in text.
    :return: List of all matches extracted from text.
    """
    data = []
    # Extract matches from sections / headers.
    if headers:
        pass
    # Extract matches from full text.
    if not lateralities:
        lateralities = build_laterality_table(text, search_negated_list=search_negated_list)
    for new_var in get_helper(text, lateralities, 'ALL'):
        data.append(new_var)
    return data