import re

from eye_extractor.nlp.character_groups import LINE_START_CHARS_RX

NEWLINE_SECTION_PAT = re.compile(
    rf'(?:[{LINE_START_CHARS_RX}]|^)(?P<header>[ \t\w/\-.]+)[:-]\W',
)

SKIP_SECTIONS = frozenset({'OD', 'OS'})


def get_index_of_next_section_start(text, start_index, *, max_length=None,
                                    stop_before_regex=None, skip_sections=SKIP_SECTIONS):
    """
    Find the start of the next section.
    :param text:
    :param start_index:
    :param max_length:
    :param stop_before_regex:
    :param skip_sections:
    :return:
    """
    if stop_before_regex:  # check for end boundary
        if m := stop_before_regex.search(text[start_index:]):
            if not max_length or m.start() < max_length:
                max_length = m.start()
    # look for next section
    for m in NEWLINE_SECTION_PAT.finditer(text, pos=start_index):
        if max_length and m.start() - start_index > max_length:
            return max_length
        section_name = m.group('header').strip().upper()
        if section_name in skip_sections:
            continue
        else:
            return m.start()  # return start of entire pattern
    return None
