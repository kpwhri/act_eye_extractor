import re

from eye_extractor.common.date import parse_date
from eye_extractor.laterality import LATERALITY_PLUS_COLON_PATTERN, lat_lookup, Laterality
from eye_extractor.nlp.character_groups import get_next_text_to_newline, get_previous_text_to_newline, \
    get_previous_index_of_newline, get_next_index_of_newline, LINE_START_CHARS_RX

from loguru import logger

from eye_extractor.output.variable import has_valid_date
from eye_extractor.sections.utils import get_index_of_next_section_start

OCT_MACULA_PAT = re.compile(
    rf'(?:'
    rf'\boct\s*macula:'
    rf'|[{LINE_START_CHARS_RX}]\s*oct\b'
    rf'|^oct\b'
    rf')',
    re.IGNORECASE,
)

SECTION_PAT = re.compile(r'[A-Za-z]{2}:')


def _find_oct_macula_section_laterality(text, *, restrict_date=None):
    data = {}
    date = parse_date(text[:50])
    if not has_valid_date(restrict_date, data):
        return None
    prev_start = None
    prev_lat = None
    for m in LATERALITY_PLUS_COLON_PATTERN.finditer(text):
        if prev_start:
            data[prev_lat] = {'text': text[prev_start: m.start()], 'date': date}
        prev_start = m.end()
        prev_lat = lat_lookup(m, group=1)
    if prev_start:
        data[prev_lat] = {'text': get_next_text_to_newline(prev_start, text), 'date': date}
    if not data and text:  # didn't find lateralities
        logger.warning(f'No lateralities in OCT MACULA section: {text}')
        data[Laterality.UNKNOWN] = {'text': text, 'date': date}
    return data


def find_oct_macula_sections(text, *, restrict_date=None) -> list[dict]:
    """
    Extract OCT Macula section to find components.
    :param restrict_date: limit date to this value
    :param text:
    :return: list[dict[Laterality->str|'date'->datetime.date]]
    """
    sections = []
    for m in OCT_MACULA_PAT.finditer(text):
        end_index = get_index_of_next_section_start(text, m.end(), max_length=200)
        if res := _find_oct_macula_section_laterality(
                text[m.start(): end_index],
                restrict_date=restrict_date,
        ):
            sections.append(res)
    return sections


def _get_start_of_next_section(text, pos, end_oct):
    last_macula_oct = pos
    # look for start of next section
    for m in SECTION_PAT.finditer(text, pos=last_macula_oct):
        if m.group().lower().strip(':') in {'od', 'os'}:
            pos = m.end()  # found new section start, but want to include od/os in the group
            end_oct = get_next_index_of_newline(pos, text)
            continue
        else:  # end of od/os sections
            substring = text[pos + 5:m.start()]
            end_oct = pos + 5 + get_previous_index_of_newline(len(substring), substring)
            break
    return end_oct


def remove_macula_oct(text):
    result = []
    prev_end = 0
    for m in OCT_MACULA_PAT.finditer(text):
        end_index = get_index_of_next_section_start(text, m.end(), max_length=200)
        result.append(text[prev_end: m.start()])
        prev_end = end_index
    result.append(text[prev_end:])
    return ''.join(result)
