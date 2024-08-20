"""
Treat headers and their text as key-value pairs
"""
import re

from eye_extractor.amd.drusen import find_drusen
from eye_extractor.laterality import LATERALITY_PATTERN, LATERALITY
from eye_extractor.nlp.character_groups import LINE_START_CHARS_RX

HEADER_PAT = re.compile(  # built in reverse, always looks for semicolon
    r":(\s?[A-Z'/]+)+"
)

Section = str
SectionText = str


# TODO: have headers store laterality state
# TODO: have headers store text hierarchically MACULA: djfslkdj OD: drusen -> MACULA: 'd... OD: drusen'
class Headers:

    def __init__(self, *initialdicts, text=None):
        self.data = []
        self.text = text  # if not None, use this text for missing headers
        self.searched = {}  # store previous lookups
        for initialdict in initialdicts:
            if initialdict:
                self.add(initialdict)

    def remove(self, func):
        """Remove text (e.g., boilerplate) using a function"""
        if self.text:
            self.text = func(self.text)
        self.data = [{k: func(v) for k, v in d.items()} for d in self.data]

    def set_text(self, text):
        """Setting a base text allows expanded search if target header was not found."""
        self.text = text

    def add(self, d):
        if isinstance(d, dict):
            self.data.append(
                {x.replace(' ', '_').upper(): y for x, y in d.items()}
            )
        elif isinstance(d, Headers):
            self.data += d.data

    def iterate(self, *headers: Section) -> tuple[Section, SectionText]:
        for header in headers:
            found = False
            for d in self.data:
                if text := d.get(header, None):
                    yield header, text
                    found = True
                    break
            if not found:
                if search_result := self.search(header):
                    yield header, search_result

    def get(self, header: Section, default=None) -> SectionText:
        for d in self.data:
            if header in d:
                return d[header]
        return default

    def search(self, header: Section):
        """Search for missing section headers"""
        if not self.text:
            return None
        if header not in self.searched:
            header_rx = header.replace('_', r'\W*')
            section_text = None
            if m := re.search(rf'(?:[{LINE_START_CHARS_RX}]|^)\s*{header_rx}\s*[:-]', self.text, re.I):
                m2 = re.search(rf'[A-Za-z]\s*:', self.text[m.end():])
                if m2:
                    end = m2.start() + m.end()
                else:
                    end = m.end() + 100
                section_text = self.text[m.end(): end]
            self.searched[header] = section_text
        return self.searched[header]

    def __bool__(self):
        return bool(self.data and sum(len(x) for x in self.data) > 0)


def extract_headers_and_text(text, *, search_missing_headers=False):
    """
    Search for headers in text using the `HEADER_PAT`.

    :param text:
    :param search_missing_headers: set `True` to allow for searching additional patterns
    :return: Header
    """
    result = {}
    it = iter(x[::-1].strip() for x in HEADER_PAT.split(text[::-1])[:-1])  # why skip first / last element?
    for value, key in zip(it, it):
        result[key] = value.split('.')[0]
    headers = Headers(result)
    if search_missing_headers:
        headers.set_text(text)
    return headers


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
