import re

from eye_extractor.common.date import parse_date
from eye_extractor.common.negation import is_post_negated
from eye_extractor.laterality import LATERALITY_PLUS_COLON_PATTERN, lat_lookup, Laterality
from eye_extractor.nlp.character_groups import get_next_text_to_newline, LINE_START_CHARS_RX

from loguru import logger

from eye_extractor.output.variable import has_valid_date
from eye_extractor.sections.utils import get_index_of_next_section_start

optional_macula = r'(?:\s*macula)?:?'

OCT_MACULA_PAT = re.compile(
    rf'(?:'
    rf'\boct\s*macula:'
    rf'|[{LINE_START_CHARS_RX}]\s*oct{optional_macula}\b'
    rf'|^oct{optional_macula}\b'
    rf')',
    re.IGNORECASE,
)

SECTION_PAT = re.compile(r'[A-Za-z]{2}:')


def _find_oct_macula_section_laterality(text, *, restrict_date=None):
    data = {}
    date = parse_date(text[:30])
    if not has_valid_date(restrict_date, data):
        return None
    prev_start = None
    prev_lat = None
    if date and re.search(rf'{date.year}\W*OD\s', text[:35]):
        pat = re.compile(r'\b(OD|OS)\b')  # there aren't colons in this context
    else:
        pat = LATERALITY_PLUS_COLON_PATTERN  # require end colon
    for m in pat.finditer(text):
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
        if is_post_negated(m, text, terms={'today', 'done', 'visit'}):
            continue
        end_index = get_index_of_next_section_start(text, m.end(), max_length=200)
        if res := _find_oct_macula_section_laterality(
                text[m.start():end_index],
                restrict_date=restrict_date,
        ):
            sections.append(res)
    return sections


def remove_macula_oct(text):
    result = []
    prev_end = 0
    for m in OCT_MACULA_PAT.finditer(text):
        if is_post_negated(m, text, terms={'today', 'done', 'visit'}):
            continue
        end_index = get_index_of_next_section_start(text, m.end(), max_length=200)
        result.append(text[prev_end: m.start()])
        prev_end = end_index
    if prev_end is not None:
        result.append(text[prev_end:])
    return ''.join(result)
