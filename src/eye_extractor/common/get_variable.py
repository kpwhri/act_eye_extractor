from typing import Callable

from eye_extractor.laterality import build_laterality_table
from eye_extractor.sections.document import Document


def _split_and_get_variable(text: str, get_helper: Callable, split_char: str, search_negated_list: bool = False):
    """Helper function to split text on a given character and process chunks independently.

    Given `text`, split on `split_char` and search for variables using `get_helper` on each chunk independently.

    :param text: Text to split into chunks.
    :param get_helper: Helper function used to specify extraction behavior.
    :param split_char: Single character to split `text` on.
    :return: List of all matches extracted from text chunks.
    """
    data = []
    if len(split_char) != 1:
        raise ValueError('`split_char` must be one character long.')
    for snippet in text.split(split_char):
        lateralities = build_laterality_table(snippet, search_negated_list=search_negated_list)
        for new_var in get_helper(snippet, lateralities, 'ALL'):
            data.append(new_var)

    return data


def get_variable(doc: Document, get_helper: Callable, *,
                 text: str = None, target_headers: list[str] = None, lateralities=None, search_negated_list=False,
                 split_char: str = None) -> list:
    """General function for extracting variables from text.

    General template for extracting variables from a given text. Requires a helper function to perform the extraction.

    :param doc:
    :param get_helper: Helper function used to specify extraction behavior.
    :param target_headers: Section headers to search for variable.
    :param text: if not default text, specify text and lateralities here
    :param lateralities:
    :param search_negated_list: If True, search for negated lists in text.
    :param split_char: If not None, split `text` on character and process chunks independently.
    :return: List of all matches extracted from text.
    """
    data = []
    # Extract matches from sections / headers.
    if target_headers:
        for section in doc.iter_sections(*target_headers):
            if search_negated_list:
                section_lateralities = build_laterality_table(section.text, search_negated_list=search_negated_list)
            else:
                section_lateralities = section.lateralities
            for new_var in get_helper(section.text, section_lateralities, section.name):
                data.append(new_var)
    # Extract matches from full text.
    if split_char:
        data += _split_and_get_variable(text or doc.text, get_helper, split_char, search_negated_list=search_negated_list)
    else:
        # get text and lateralities
        if text and lateralities:
            pass
        elif text:  # not lateralities
            lateralities = build_laterality_table(text, search_negated_list=search_negated_list)
        else:
            text = doc.get_text()
            if search_negated_list:
                lateralities = build_laterality_table(text, search_negated_list=search_negated_list)
            else:
                lateralities = doc.get_lateralities()

        for new_var in get_helper(text, lateralities, 'ALL'):
            data.append(new_var)

    return data
