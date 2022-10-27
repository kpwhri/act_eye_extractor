import re

from eye_extractor.common.date import parse_date
from eye_extractor.laterality import LATERALITY_PLUS_COLON_PATTERN, lat_lookup, Laterality
from eye_extractor.nlp.character_groups import get_next_text_to_newline

from loguru import logger

from eye_extractor.output.variable import has_valid_date

OCT_MACULA_PAT = re.compile(
    rf'\b(?:'
    rf'oct\s*macula:'
    rf')',
    re.IGNORECASE,
)


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
        data[Laterality.UNKNOWN] = text
    return data


def find_oct_macula_sections(text, *, restrict_date=None) -> list[dict]:
    """
    Extract OCT Macula section to find components.
    :param restrict_date: limit date to this value
    :param text:
    :return: list[dict[Laterality->str|'date'->datetime.date]]
    """
    sections = []
    prev_start = None
    for m in OCT_MACULA_PAT.finditer(text):
        prev_end = m.start()
        if prev_start:
            if res := _find_oct_macula_section_laterality(
                    text[prev_start: prev_end],
                    restrict_date=restrict_date,
            ):
                sections.append(res)
        prev_start = m.end()
    if prev_start:
        if res := _find_oct_macula_section_laterality(
                text[prev_start: prev_start + 200],
                restrict_date=restrict_date,
        ):
            sections.append(res)
    return sections
