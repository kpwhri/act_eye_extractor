import re
from typing import Iterator

from sortedcontainers import SortedList
from collections import UserList

from eye_extractor.laterality import Laterality, build_laterality_table


class Section:

    def __init__(self, name, level, text, name_start_idx, name_end_idx, text_start_idx, text_end_idx):
        self.name = name
        self.level = level
        self.name_start_idx = name_start_idx
        self.name_end_idx = name_end_idx
        self.lines = [text] if isinstance(text, str) else text
        self.text_start_idx = text_start_idx
        self.text_end_idx = text_end_idx
        self.history = None
        self.lateralities = None
        self._names = None

    @property
    def start(self):
        return self.name_start_idx

    @property
    def names(self):
        if self._names is None:
            if isinstance(self.name, tuple):
                self._names = {el for s in self.name for el in s.split('_')}
            else:
                self._names = set(self.name.split('_'))
        return self._names

    @property
    def end(self):
        return self.text_end_idx

    @property
    def text(self):
        return '\n'.join(self.lines)

    @property
    def oneline(self):
        return ' '.join(self.lines)

    def iter_subsections(self):
        if isinstance(self.name, tuple):  # has multiple
            for name in self.name:
                yield Section(name, self.level, self.lines, self.name_start_idx, self.name_end_idx,
                              self.text_start_idx, self.text_end_idx)
        else:
            yield self

    def __len__(self):
        """Length is the number of characters in the section; the name is included for text replacement"""
        return self.text_end_idx - self.name_start_idx

    def __eq__(self, other):
        if isinstance(other, Section):
            return self.name_start_idx == other.name_start_idx and self.name_end_idx == other.name_end_idx
        return False

    def __lt__(self, other):
        """Sorting by 'goes first': lower start index and longer match"""
        if isinstance(other, Section):
            if self.name_start_idx == other.name_start_idx:  # section starts at the same place
                return self.name_end_idx > other.name_end_idx  # less than is the one that ends LAST (i.e., longer match)
            return self.name_start_idx < other.name_start_idx  # less than := section starts before the other
        return False

    def overlaps(self, other):
        if isinstance(other, Section):
            return self.name_start_idx <= other.name_start_idx < self.name_end_idx or self.name_start_idx <= other.name_end_idx < self.name_end_idx
        raise TypeError(f'Expected type "Section", got {type(other)}')

    def add_line(self, line, *, extra_chars=0):
        self.lines.append(line)
        self.text_end_idx += len(line) + extra_chars

    def build_laterality_table(self, laterality_func, **kwargs):
        self.lateralities = laterality_func(self.text, **kwargs)
        if 'od' in self.names:
            self.lateralities.default_laterality = Laterality.OD
        elif 'os' in self.names:
            self.lateralities.default_laterality = Laterality.OS
        elif 'ou' in self.names:
            self.lateralities.default_laterality = Laterality.OU

    def __repr__(self):
        return f'Section[{self.name}=({self.text_start_idx},{self.text_end_idx})="{self.oneline.strip()[:20]}..."]'

    def __str__(self):
        return repr(self)
        # return self.text


class SectionFunction:

    @staticmethod
    def history(section: Section):
        if section.name.endswith('hx'):
            return True
        elif section.name in {'hpi', 'problem_list', 'review_of_systems'}:
            return True
        elif section.name.startswith(('past', 'last', 'previous', 'prior')):
            return True
        # TODO: check if history is a parent
        return False


class Sections(UserList):
    # TODO: should this include the full text?

    def __init__(self, sections, extra_lines=None):
        super().__init__(sections)
        self.extra_lines = extra_lines or list()

    def iter_names(self, *names) -> Iterator[Section]:
        for name in names:
            found = False
            for section in self:
                if section.name == name:
                    yield section
                    found = True
            if not found:
                pass  # print(f'Failed to find {name}')

    def iter_funcs(self, *funcs) -> Iterator[Section]:
        for func in funcs:
            found = False
            for section in self:
                if func(section):
                    yield section
                    found = True
            if not found:
                pass  # print(f'Failed to find {func}')

    def get(self, name, default=None):
        for section in self:
            if section.name == name:
                return section
        return default

    def add(self, section: Section):
        self.data.append(section)

    def add_all(self, sections):
        self.data += sections.data

    def remove_history(self, text):
        return self.remove_type(SectionFunction.history, text)

    def replace_history(self, text):
        return self.replace_type(SectionFunction.history, text)

    def remove_type(self, section_type, text):
        return self.replace_type(section_type, text, replacement='')

    def replace_type(self, section_type, text, replacement=' '):
        """Replace specified type with empty spaces thereby deleting but keep char offsets"""
        result = []
        prev = 0
        for section in self:
            if section_type(section):
                result.append(text[prev:section.start])
                result.append(replacement * len(section))
                prev = section.end
        result.append(text[prev:])
        return ''.join(result)

    def __str__(self):
        return '\n'.join(f'* {section}' for section in self.data)

    __repr__ = __str__


class SectionsBuilder:

    def __init__(self, laterality_func=None):
        self.data = SortedList()
        self.laterality_func = laterality_func
        self._extra_content = None

    def get_extra_content(self):
        """Get lines not part of any section, must run `build` first"""
        if self._extra_content is None:
            raise ValueError(f'Must run `build` before requesting extra content not assigned to any section.')
        return self._extra_content

    def add(self, section: Section):
        self.data.add(section)

    def _find_lateralities(self, lst):
        if self.laterality_func is not None:
            for section in lst:
                section.build_laterality_table(self.laterality_func)
        return lst

    def add_section(self, name, level, text, name_start_idx, name_end_idx, text_start_idx, text_end_idx):
        section = Section(name, level, text, name_start_idx, name_end_idx, text_start_idx, text_end_idx)
        self.add(section)

    def build(self, text):
        """Compile segments into a single united sections"""
        lst = list(self.data)
        if lst:
            lst = self._remove_overlaps(lst)
            lst = self._grow_sections(lst, text)
            lst = self._find_lateralities(lst)
            # combined sections (e.g., "lens, lids:" -> "lens" & "lids")
            lst = self._divide_sections(lst)
        return Sections(lst, self._extra_content)

    def _remove_overlaps(self, lst: list[Section]):
        """Remove overlapping sections"""
        result = [lst[0]]
        i = 0
        for j in range(1, len(lst)):
            if self._is_overlapping(lst[i], lst[j]):
                pass  # lst[j] is a submatch
            else:
                result.append(lst[j])
                i = j
        return result

    def _is_overlapping(self, s1: Section, s2: Section):
        return s1.overlaps(s2)

    def _grow_sections(self, lst, text):
        self._extra_content = []
        history = []
        for i, curr in enumerate(lst):
            if i == 0:
                for line in text[: curr.name_start_idx].split('\n'):
                    if line.strip():
                        self._extra_content.append(line)
            # find the max index which this section can have (e.g., the start of next
            if i == len(lst) - 1:  # is last element
                next_start_idx = len(text)  # section ends at end of text
            elif curr.level == 1:
                # for top-level sections, find next top level section (if exists)
                for j in range(i + 1, len(lst)):  # start looking at next section for top-level section
                    if lst[j].level == 1:
                        next_start_idx = lst[j].name_start_idx
                        break
                else:  # if there is no subsequent top-level section
                    next_start_idx = len(text)  # set to end of text

            else:
                next_start_idx = lst[i + 1].name_start_idx
            mid_text_lines = text[curr.text_end_idx: next_start_idx].split('\n')
            # heuristics
            empty_line_cnt = 0
            skip_chars = 0
            for line_num, line in enumerate(mid_text_lines):
                if line_num == 0 and line == '':
                    continue  # skip first line
                if not line.strip():
                    empty_line_cnt += 1  # every line has implicit \n, so cutoff should be one ''
                    skip_chars += len(line) + 1
                elif empty_line_cnt >= 1:
                    # only allow two empty newlines, otherwise not part of section
                    self._extra_content.append(line)
                    continue
                else:  # has content
                    empty_line_cnt = 0
                    # TODO: are there any heuristics to not add it?

                    curr.add_line(line, extra_chars=skip_chars + 1)
            curr.history = history
            history.append(curr.name)
        return lst

    def is_major_section(self, m, text):
        if m.group('content').strip():
            return False  # content, so header not on own line
        if m2 := re.search(r'\w', text[m.end('content'):]):
            if text[m.end('content'): m2.start()].count('\n') >= 2:
                return False  # may be major, but has two empty newlines so lacks content
        return True

    def _divide_sections(self, lst):
        res = []
        for section in lst:
            for sect in section.iter_subsections():
                res.append(sect)
        return res


def get_sections(text, patterns, newline_chars=None):
    if newline_chars:
        for newline_char in newline_chars:
            text = text.replace(newline_char, '\n')
    builder = SectionsBuilder()
    for cat, level, pat in patterns:
        for m in pat.finditer(text):
            if builder.is_major_section(m, text):
                level = 1
            builder.add_section(cat, level, m.group('content'), m.start('name'), m.end('name'), m.start('content'),
                                m.end('content'))
    sections = builder.build(text)
    return sections


def get_sections_from_dict(section_dict: dict | None) -> Sections:
    """
    Quickly initialize a Sections object: Mainly for testing.
    Args:
        section_dict:

    Returns:
        Sections
    """
    section_dict = section_dict or dict()
    section_list = []
    last_idx = 0
    default_level = 2
    for sect_name, sect_text in section_dict.items():
        name_start_idx = last_idx
        name_end_idx = name_start_idx + len(sect_name)
        text_start_idx = name_end_idx + 3
        text_end_idx = text_start_idx + len(sect_text)
        section = Section(sect_name.lower(), default_level, sect_text, name_start_idx, name_end_idx,
                          text_start_idx, text_end_idx)
        section.build_laterality_table(build_laterality_table)
        section_list.append(section)
        last_idx = text_end_idx + 3
    return Sections(section_list)
