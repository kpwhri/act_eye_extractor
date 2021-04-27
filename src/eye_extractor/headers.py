"""
Treat headers and their text as key-value pairs
"""
import re
from typing import Match

from eye_extractor.laterality import LATERALITY_PATTERN, LATERALITY, Laterality

HEADER_PAT = re.compile(  # built in reverse, always looks for semicolon
    r":(\s?[A-Z'/]+)+"
)

SMALL_DRUSEN_PAT = re.compile(
    r'('
    r'(very\W*)?fine'
    r'|scattered'
    r'|occasional'
    r'|rare'
    r'|few'
    r'|mild'
    r'|small(er)?'
    r'|trace'
    r'|light'
    r')(\s*\w+){3} drusen\b',
    re.I
)
INTERMEDIATE_DRUSEN_PAT = re.compile(
    r'('
    r'intermediate'
    r'|moderate'
    r')(\s*\w+){3} drusen\b',
    re.I
)
LARGE_DRUSEN_PAT = re.compile(
    r'('
    r'dense'
    r'|large'
    r'|heavy'
    r'|big'
    r')(\s*\w+){3} drusen\b',
    re.I
)

DRUSEN_PAT = re.compile(r'drusen', re.I)
HARD_DRUSEN_PAT = re.compile(r'(hard drusen)', re.I)
SOFT_DRUSEN_PAT = re.compile(r'(soft drusen)', re.I)
BOTH_DRUSEN_PAT = re.compile(r'(soft(\s*(and|,|/)\s*hard)?|hard(\s*(and|,|/)\s*soft)?) drusen', re.I)
NO_DRUSEN_PAT = re.compile(r'((no|or) drusen)', re.I)


def extract_headers_and_text(text):
    result = {}
    it = iter(x[::-1].strip() for x in HEADER_PAT.split(text[::-1])[:-1])
    for value, key in zip(it, it):
        result[key] = value.split('.')[0]
    return result


def get_laterality_for_term(lateralities, match: Match, text):
    for lat, start, end in lateralities:
        if start > match.start():  # after
            return lat
        elif len(text[end:match.start()]) < 10 and 'with' in text[end:match.start()]:
            return lat
    if lateralities:
        return lateralities[-1][1]
    return Laterality.OU  # default to both


def add_laterality_to_variable(data, laterality, variable, value):
    if laterality in {Laterality.OU, Laterality.OS}:
        data[f'{variable}_le'] = value
    if laterality in {Laterality.OU, Laterality.OD}:
        data[f'{variable}_re'] = value


def create_variable(data, text, match, lateralities, variable, value):
    lat = get_laterality_for_term(lateralities, match, text)
    add_laterality_to_variable(data, lat, variable, value)


def find_drusen(data, macula_text, lateralities):
    """
    Designed so that subsequent variables can overwrite earlier ones
    :param data:
    :param macula_text:
    :param lateralities:
    :return:
    """
    for m in DRUSEN_PAT.finditer(macula_text):
        create_variable(data, macula_text, m, lateralities, 'drusen_size', {
            'value': 4, 'term': m.group(), 'label': 'unknown', 'source': 'MACULA',
        })
        create_variable(data, macula_text, m, lateralities, 'drusen_type', {
            'value': 4, 'term': m.group(), 'label': 'unknown', 'source': 'MACULA',
        })
    for m in NO_DRUSEN_PAT.finditer(macula_text):
        create_variable(data, macula_text, m, lateralities, 'drusen_size', {
            'value': 0, 'term': m.group(), 'label': 'no', 'source': 'MACULA',
        })
        create_variable(data, macula_text, m, lateralities, 'drusen_type', {
            'value': 0, 'term': m.group(), 'label': 'no', 'source': 'MACULA',
        })

    for m in BOTH_DRUSEN_PAT.finditer(macula_text):
        create_variable(data, macula_text, m, lateralities, 'drusen_size', {
            'value': 3, 'term': m.group(), 'label': 'both', 'source': 'MACULA',
        })

    for m in HARD_DRUSEN_PAT.finditer(macula_text):
        create_variable(data, macula_text, m, lateralities, 'drusen_size', {
            'value': 1, 'term': m.group(), 'label': 'hard', 'source': 'MACULA',
        })

    for m in SOFT_DRUSEN_PAT.finditer(macula_text):
        create_variable(data, macula_text, m, lateralities, 'drusen_size', {
            'value': 2, 'term': m.group(), 'label': 'soft', 'source': 'MACULA',
        })

    for m in SMALL_DRUSEN_PAT.finditer(macula_text):
        create_variable(data, macula_text, m, lateralities, 'drusen_type', {
            'value': 1, 'term': m.group(), 'label': 'small', 'source': 'MACULA',
        })
    for m in INTERMEDIATE_DRUSEN_PAT.finditer(macula_text):
        create_variable(data, macula_text, m, lateralities, 'drusen_type', {
            'value': 2, 'term': m.group(), 'label': 'intermediate', 'source': 'MACULA',
        })
    for m in LARGE_DRUSEN_PAT.finditer(macula_text):
        create_variable(data, macula_text, m, lateralities, 'drusen_type', {
            'value': 3, 'term': m.group(), 'label': 'large', 'source': 'MACULA',
        })


def get_data_from_headers(text):
    headers = extract_headers_and_text(text)
    data = {}
    # MACULA
    if macula_text := headers.get('MACULA', None):
        lateralities = [(LATERALITY[m.group().upper()], m.start(), m.end()) for m in
                        LATERALITY_PATTERN.finditer(macula_text)]
        # drusen
        find_drusen(data, macula_text, lateralities)

    return data
