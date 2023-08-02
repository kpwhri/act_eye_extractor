import re

from eye_extractor.history.common import find_end
from eye_extractor.nlp.character_groups import LINE_START_CHARS_RX
from eye_extractor.sections.utils import get_index_of_next_section_start

history = r'(?:hist(?:ory)?|hx)'
medical = r'(?:ocular|eye|optical|med(?:ical)?|eye\W*health)'
past = r'(?:past|personal)'

HISTORY_SECTION_PAT = re.compile(
    rf'\b(?:'
    rf'review\s*of\s*symptoms'
    rf'|review\s*of\s*systems'
    rf'|systems\s*review'
    rf'|social\s*{history}'
    rf'|(?:{past}\s*)?{medical}\s*{history}(?:\s*(?:of|includes))?'
    rf'|pm\s*{history}(?:\s*of)?'
    rf'|fam(?:ily)?\s*(?:{medical}\s*)?{history}(?:\s*of)?'
    rf'|past\s*(?:\w+\W*){{,6}}'
    rf'|family\s*{history}\s*of\s*any\s*eye\s*or\s*medical\s*diseases'
    rf')[:-]',
    re.I
)

PROBLEM_LIST = re.compile(
    rf'(?:'
    rf'(?:patient\s*)?active\s*problem\s*list[^A-Za-z0-9]+'
    rf')',
    re.I
)

STOP_BEFORE_REGEX = re.compile(
    rf'(?:'
    rf'signed\s*by'
    rf'|date'
    rf'|time'
    rf'|(?:patient\s*)?active\s*problem\s*list'
    rf'|[{LINE_START_CHARS_RX} ]{{2}}'
    rf')',
    re.I
)

PROBLEM_LIST_STOP_BEFORE = re.compile(
    rf'(?:'
    rf'[{LINE_START_CHARS_RX}][^A-Za-z0-9{LINE_START_CHARS_RX}]*[{LINE_START_CHARS_RX}]'
    rf'|===='
    rf'|ALLERGIES|PATIENT HISTORY|Current Medications|REVIEW OF SYSTEMS|Medical History'
    rf')',
    # case sensitive
)


def get_problem_list(text):
    """
    Iterator for problem list and surrounding text; distinguished by result[-1] (true=is_problem_list)
    :param text:
    :return: (text, start_header, end_header, end_section_text, is_problem_list: bool)
    """
    prev_end = 0
    for m in PROBLEM_LIST.finditer(text):
        yield text[prev_end: m.start()], prev_end, prev_end, m.start(), False
        end_index = get_index_of_next_section_start(
            text, m.end(), max_length=1500, stop_before_regex=PROBLEM_LIST_STOP_BEFORE,
        )
        yield m.group().strip(), m.start(), m.end(), end_index, True
        prev_end = end_index
    yield text[prev_end:], prev_end, prev_end, len(text), False


def get_problem_list_for_json(text):
    """
    DEBUG: get problem list and text
    :param text:
    :return:
    """
    problist = []
    textlist = []
    for header, start, start_sect, end_sect, is_problist in get_problem_list(text):
        if is_problist:
            problist.append({header: text[start_sect: end_sect]})
        else:
            textlist.append(text[start_sect: end_sect])
    return {
        'problem_list': problist,
        'text': textlist,
    }


def remove_problem_list(text):
    """

    :param text:
    :return: text with problem list section removed
    """
    return '\n'.join(sect for sect, *_, is_problist in get_problem_list(text) if not is_problist)



def _find_history_sections(text, include_problem_list=True):
    """
    Retrieve offsets for history sections of note.
    Uses two methods to find the widest window.
    :param text:
    :return: yields matched_section_name, start_index (incl header), start_index, end_index
    """
    for m in HISTORY_SECTION_PAT.finditer(text):
        end_index = get_index_of_next_section_start(
            text, m.end(), max_length=1000, stop_before_regex=STOP_BEFORE_REGEX
        )
        end_index2 = find_end(text, m.end())
        yield m.group().strip().strip(':'), m.start(), m.end(), max(end_index, end_index2)
    if include_problem_list:
        for *other, is_problist in get_problem_list(text):
            if is_problist:
                yield other


def retrieve_history_sections(text):
    """
    Retrieve history sections as dicts
    :param text:
    :return: yields {name: section name, text: text in section (not including header value)}
    """
    for section_name, _, start_index, end_index in _find_history_sections(text):
        yield {
            'name': section_name,
            'text': text[start_index: end_index]
        }


def remove_history_sections(text, include_problem_list=True):
    """
    Remove entire history sections from text.
    :param include_problem_list:
    :param text:
    :return:
    """
    results = []
    prev_end = 0
    for _1, start_index, _, end_index in _find_history_sections(text, include_problem_list=include_problem_list):
        results.append(text[prev_end: start_index])
        prev_end = end_index
    results.append(text[prev_end:])
    return ''.join(results)


def get_history_sections_to_be_removed(text):
    """
    DEBUG: retrieve history sections to be removed along with associated text
    :param text:
    :return:
    """
    results = []
    hx_sections = []
    prev_end = 0
    prev_start = None
    for _1, start_index, _, end_index in _find_history_sections(text):
        if prev_end > 0:
            hx_sections.append(text[prev_start: prev_end])
        results.append(text[prev_end: start_index])
        prev_end = end_index
        prev_start = start_index
    results.append(text[prev_end:])
    if prev_end > 0:
        hx_sections.append(text[prev_start: prev_end])
    return {
        'hx': hx_sections,
        'text': results,
    }
