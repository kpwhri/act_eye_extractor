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
    rf'(?:patient\s*)?active\s*problem\s*list'
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


def _find_history_sections(text):
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


def remove_history_sections(text):
    """
    Remove entire history sections from text.
    :param text:
    :return:
    """
    results = []
    prev_end = 0
    for _1, start_index, _, end_index in _find_history_sections(text):
        results.append(text[prev_end: start_index])
        prev_end = end_index
    results.append(text[prev_end:])
    return ''.join(results)
