"""
Model a document text and sections.

* Get different views of text (e.g., full text vs text without history)
"""
import enum
import re

from eye_extractor.laterality import build_laterality_table
from eye_extractor.sections.oct_macula import find_oct_macula_sections, remove_macula_oct
from eye_extractor.sections.patterns import PATTERNS
from eye_extractor.sections.section_builder import SectionsBuilder, get_sections_from_dict


class TextView(enum.IntEnum):
    ALL = 0
    NO_HX = 1
    NO_OCT_MACULA = 2


class Document:

    def __init__(self, text, *, newline_chars=None, sections=None):
        """

        Args:
            text:
            newline_chars:
            sections: mainly for testing
        """
        self.orig_text = text  # has original char offsets
        self.text = self._clean_text(text, newline_chars=newline_chars)
        self.lateralities = self._build_laterality_table(self.text)
        self.sections = self._get_sections(self.text, PATTERNS)
        if sections:
            self.sections.add_all(sections)
        self.oct_macula_sections = find_oct_macula_sections(self.text)

        self._text_no_hx = None
        self._lat_table_no_hx = None
        self._text_no_oct_macula = None
        self._lat_no_oct_macula = None

        self._is_cataract_surgery = None

    @property
    def is_cataract_surgery(self):
        if self._is_cataract_surgery is None:
            for section in self.sections.iter_names('preop_dx'):
                if section.search('cataract', flags=re.I):
                    self._is_cataract_surgery = True
                    break
            else:
                self._is_cataract_surgery = False
        return self._is_cataract_surgery

    @property
    def text_no_oct_macula(self):
        if self._text_no_oct_macula is None:
            self._text_no_oct_macula = remove_macula_oct(self.text_no_hx)
        return self._text_no_oct_macula

    @property
    def lateralities_no_oct_macula(self):
        if self._lat_no_oct_macula is None:
            self._lat_no_oct_macula = self._build_laterality_table(self.text_no_oct_macula)
        return self._lat_no_oct_macula

    def get_text(self, *, view: TextView = TextView.NO_HX):
        match view:
            case TextView.NO_HX:
                return self.text_no_hx
            case TextView.NO_OCT_MACULA:
                return self.text_no_oct_macula
            case TextView.ALL:
                return self.text
            case _:
                raise ValueError(f'Unrecognized TextView: {view}.')

    def get_lateralities(self, *, view: TextView = TextView.NO_HX):
        match view:
            case TextView.NO_HX:
                return self.lateralities_no_hx
            case TextView.NO_OCT_MACULA:
                return self.lateralities_no_oct_macula
            case TextView.ALL:
                return self.lateralities
            case _:
                raise ValueError(f'Unrecognized TextView: {view}.')

    @property
    def text_no_hx(self):
        if self._text_no_hx is None:
            self._text_no_hx = self.sections.replace_history(self.text)
        return self._text_no_hx

    @property
    def lateralities_no_hx(self):
        if self._lat_table_no_hx is None:
            self._lat_table_no_hx = self._build_laterality_table(self.text_no_hx)
        return self._lat_table_no_hx

    def _build_laterality_table(self, text):
        return build_laterality_table(text)

    def _clean_text(self, text, newline_chars=None):
        if newline_chars:
            for newline_char in newline_chars:
                text = text.replace(newline_char, '\n')
        return text

    def _get_sections(self, text, patterns):
        builder = SectionsBuilder(self._build_laterality_table)
        for cat, level, pat in patterns:
            for m in pat.finditer(text):
                if builder.is_major_section(m, text):
                    level = 1
                builder.add_section(cat, level, m.group('content'),
                                    m.start('name'), m.end('name'),
                                    m.start('content'), m.end('content'))
        sections = builder.build(text)
        return sections

    def iter_sections(self, *names):
        yield from self.sections.iter_names(*names)


def create_doc_and_sections(text, section_dict: dict | None = None) -> Document:
    return Document(text, sections=get_sections_from_dict(section_dict), newline_chars='¶')
