"""
Treat headers and their text as key-value pairs
"""
from collections import UserDict
import re

from eye_extractor.amd.drusen import find_drusen
from eye_extractor.laterality import LATERALITY_PATTERN, LATERALITY

HEADER_PAT = re.compile(  # built in reverse, always looks for semicolon
    r":(\s?[A-Z'/]+)+"
)

Section = str
SectionText = str


# TODO: have headers store laterality state
# TODO: have headers store text hierarchically MACULA: djfslkdj OD: drusen -> MACULA: 'd... OD: drusen'
class Headers(UserDict):
    def iterate(self, *headers: Section) -> tuple[Section, SectionText]:
        for header in headers:
            if text := self.data.get(header, None):
                yield header, text


def extract_headers_and_text(text):
    result = {}
    it = iter(x[::-1].strip() for x in HEADER_PAT.split(text[::-1])[:-1])
    for value, key in zip(it, it):
        result[key] = value.split('.')[0]
    return Headers(result)


def get_data_from_headers(text):
    headers = extract_headers_and_text(text)
    data = {}
    # MACULA
    if macula_text := headers.get('MACULA', None):
        lateralities = [(LATERALITY[m.group().upper()], m.start(), m.end(), True) for m in
                        LATERALITY_PATTERN.finditer(macula_text)]
        # drusen
        data |= find_drusen(macula_text, lateralities)

    return data
