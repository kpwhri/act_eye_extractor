import enum
import re
from typing import Match, Optional

from sortedcontainers import SortedList

from eye_extractor.common.date import parse_nearest_date_to_line_start
from eye_extractor.nlp.character_groups import LINE_START_CHARS


class Laterality(enum.IntEnum):
    NONE = -1  # placeholder
    OD = 1  # right
    OS = 2  # left
    OU = 3  # both/bilateral
    UNKNOWN = 0  # keep 0 so that it will test 'False'


class LateralityLocatorStrategy(enum.Enum):
    DEFAULT = 1
    LINE_BREAK = 2


LATERALITY = {
    'OD GREATER THAN OS': Laterality.OU,
    'OD > OS': Laterality.OU,
    'OD>OS': Laterality.OU,
    'OS GREATER THAN OD': Laterality.OU,
    'OS > OD': Laterality.OU,
    'OS>OD': Laterality.OU,
    'O.D. GREATER THAN O.S.': Laterality.OU,
    'O.D. > O.S.': Laterality.OU,
    'O.D.>O.S.': Laterality.OU,
    'O.S. GREATER THAN O.D.': Laterality.OU,
    'O.S. > O.D.': Laterality.OU,
    'O.S.>O.D.': Laterality.OU,
    'OD LESS THAN OS': Laterality.OU,
    'OD < OS': Laterality.OU,
    'OD<OS': Laterality.OU,
    'OS LESS THAN OD': Laterality.OU,
    'OS < OD': Laterality.OU,
    'OS<OD': Laterality.OU,
    'O.D. LESS THAN O.S.': Laterality.OU,
    'O.D. < O.S.': Laterality.OU,
    'O.D.<O.S.': Laterality.OU,
    'O.S. LESS THAN O.D.': Laterality.OU,
    'O.S. < O.D.': Laterality.OU,
    'O.S.<O.D.': Laterality.OU,
    'OD': Laterality.OD,
    'O.D.': Laterality.OD,
    'RIGHT EYE': Laterality.OD,
    'RE': Laterality.OD,
    'R.E.': Laterality.OD,
    'RIGHT': Laterality.OD,
    'R': Laterality.OD,
    'L': Laterality.OS,
    'OS': Laterality.OS,
    'O.S.': Laterality.OS,
    'LEFT EYE': Laterality.OS,
    'LE': Laterality.OS,
    'L.E.': Laterality.OS,
    'LEFT': Laterality.OS,
    'BOTH EYE': Laterality.OU,
    'BOTH EYES': Laterality.OU,
    'BOTH': Laterality.OU,
    # 'BE': Laterality.OU,  # ambiguous
    'OU': Laterality.OU,
    'O.U.': Laterality.OU,
    'BILATERAL': Laterality.OU,
}


def _build_pattern(lat):
    return '|'.join(
        k for k, v in LATERALITY.items() if v == lat
    ).replace('.', r'\.').replace(' ', r'\s+')


od_pattern = _build_pattern(Laterality.OD)
os_pattern = _build_pattern(Laterality.OS)
ou_pattern = _build_pattern(Laterality.OU)

laterality_pattern = '|'.join(LATERALITY.keys()).replace('.', r'\.').replace(' ', r'\s+')

LATERALITY_PATTERN = re.compile(
    rf'\b({laterality_pattern})\b\s*:?',
    re.IGNORECASE
)

LATERALITY_SPLIT_PATTERN = re.compile(  # for determining likely boundaries
    rf'\b({laterality_pattern}|:)\b',
    re.IGNORECASE
)

LATERALITY_PLUS_COLON_PATTERN = re.compile(
    rf'\b({laterality_pattern})\W*:'
)


def laterality_finder(text):
    for m in LATERALITY_PATTERN.finditer(text):
        yield lat_lookup(m)


def simplify_lateralities(lats):
    """Simplify lateralities (e.g., OD, OS -> OU"""
    lats = set(lats)
    if Laterality.OD in lats and Laterality.OS in lats:
        return Laterality.OU
    elif Laterality.OD in lats:
        return Laterality.OD
    elif Laterality.OS in lats:
        return Laterality.OS
    else:
        return Laterality.UNKNOWN


def lat_lookup(m, *, group=0):
    return LATERALITY[
        ' '.join(x.strip() for x in m.group(group).upper().strip().strip(':').strip().split())
    ]


def build_laterality_table(text):
    latloc = LateralityLocator()
    for m in LATERALITY_PATTERN.finditer(text):
        is_lat = m.group().endswith(':')
        latloc.add(lat_lookup(m), m.start(), m.end(), is_lat)
    return latloc


def get_previous_laterality_from_table(table, index):
    for name, start, end, is_lat in reversed(table.lateralities):
        if is_lat and end < index:
            return name, start, end
    return Laterality.UNKNOWN, None, None


def get_immediate_next_laterality_from_table(table, index, max_skips=1):
    """

    :param table:
    :param index:
    :param max_skips: how many colons to skip
    :return:
    """
    found_skips = 0
    for name, start, end, is_lat in table:
        if start > index:  # after our target word
            if is_lat:
                return name, start, end
            else:
                found_skips += 1
                if found_skips > max_skips:
                    return Laterality.UNKNOWN, None, None
    return Laterality.UNKNOWN, None, None


def get_immediate_next_or_prev_laterality_from_table(table, index, *, max_skips=1):
    lat, start, end = get_immediate_next_laterality_from_table(table, index, max_skips=max_skips)
    if lat == Laterality.UNKNOWN:
        lat, start, end = get_previous_laterality_from_table(table, index)
    return lat, start, end


def create_variable(data, text, match, lateralities, variable, value, *, known_laterality=None):
    # dates: this will probably significantly increase processing time
    if isinstance(value, dict) and value.get('date', None) is None:  # skip if alternative way of finding date
        value['date'] = parse_nearest_date_to_line_start(match.start(), text)
    # laterality
    lat = known_laterality
    if not known_laterality or known_laterality == Laterality.UNKNOWN:
        lat = get_laterality_for_term(
            lateralities or build_laterality_table(text),
            match,
            text
        )
    add_laterality_to_variable(data, lat, variable, value)


def create_new_variable(text, match, lateralities, variable, value, *, known_laterality=None):
    """
    Create a new variable (usually passed to a list called data). Wrapper around `create_variable`.

    :param text:
    :param match:
    :param lateralities:
    :param variable:
    :param value: dict with the following values (most are optional, but these are best practice):
        * value: numerical representation (or IntEnum)
        * label: text interpretation of 'value'
        * term: m.group() (or provide wider context for debugging)
        * source: section or other information
        * prioritiy: int >= 0: use to sort relative priority where the larger value is more important

    :param known_laterality:
    :return:
    """
    data = {}
    # assign 'value' to each of the lateralities, suffixing '_re', '_le', '_unk'
    create_variable(data, text, match, lateralities, variable, value,
                    known_laterality=known_laterality)
    return data


def get_laterality_for_term(lateralities, match: Match, text, *, strategy=LateralityLocatorStrategy.DEFAULT):
    """Get laterality for a particular match by its index, so `match` must have been found in `text`"""
    return lateralities.get_by_index(match.start(), text, strategy=strategy)


class LatLocation:

    def __init__(self, laterality: Laterality, start: int, end: int, is_section_start: bool):
        self.laterality = laterality
        self.start = start
        self.end = end
        self.is_section_start = is_section_start

    def __getitem__(self, item):
        match item:
            case 0:
                return self.laterality
            case 1:
                return self.start
            case 2:
                return self.end
            case 3:
                return self.is_section_start
        raise ValueError(f'Unrecognized index: {item}')

    def __repr__(self):
        return f'LatLocation:{self.laterality.name},{self.start}:{self.end},{1 if self.is_section_start else 0}'

    def __str__(self):
        return repr(self)

    def __iter__(self):
        yield self.laterality
        yield self.start
        yield self.end
        yield self.is_section_start


class LateralityLocator:
    DEFAULT_COUNT_LETTERS = {
        ',': 1,
        '.': 2,
    } | {x: 3 for x in LINE_START_CHARS}

    def __init__(self, lateralities: list[LatLocation] = None, *, default_laterality=Laterality.UNKNOWN):
        if lateralities:
            self.lateralities = SortedList(lateralities, key=lambda x: x[1])
        else:
            self.lateralities = SortedList([], key=lambda x: x[1])
        self.default_laterality = default_laterality

    def add_laterality(self, laterality: LatLocation):
        self.lateralities.add(laterality)

    def add(self, laterality: Laterality, start: int, end: int, is_section_start: bool):
        self.lateralities.add(LatLocation(laterality, start, end, is_section_start))

    def get_previous_section(self, match_start, text, *, exclude_intervening_headers=True) -> Optional[LatLocation]:
        prev_lat_section = None
        for i, lat in enumerate(self.lateralities):
            if lat.is_section_start:
                if lat.start > match_start:  # laterality after match index
                    if prev_lat_section:
                        if exclude_intervening_headers:
                            if text[lat.start: match_start].count(':') > 1:
                                return None
                        return prev_lat_section
                    return None  # outside of any laterality header (and followed by one)
                else:
                    prev_lat_section = lat
        return prev_lat_section

    def get_previous_next_non_section(self, match_start, text) -> tuple[Optional[LatLocation], Optional[LatLocation]]:
        """Get tuple of previous and next matches; ignore previous if previous section header is closer"""
        last_found_lat = None
        for i, lat in enumerate(self.lateralities):
            if lat.is_section_start:
                if lat.start == match_start:
                    return lat, None
                elif lat.start < match_start:  # laterality before match index
                    last_found_lat = lat  # reset this value
                else:  # laterality section first after match index, so no after
                    return last_found_lat, None
            else:
                if lat.start == match_start:
                    return lat, None
                elif lat.start < match_start:  # before, so store it
                    last_found_lat = lat
                else:  # after, return this and the previous
                    return last_found_lat, lat
        return last_found_lat, None  # nothing found after

    def count_before(self, match_start, text, lat: LatLocation, value) -> int:
        """Count from laterality to match: number of `value` from `lat.start` to `match_start`"""
        return self.count_all(text[lat.start:match_start], value)

    def count_after(self, match_start, text, lat: LatLocation, value) -> int:
        """Count from match to laterality: number of `value` between `match_start` and `lat.start`"""
        return self.count_all(text[match_start:lat.start], value)

    def count_all(self, text, value):
        return sum([value.get(letter, 1) if isinstance(value, dict) else 1 for letter in text if letter in value])

    def distance(self, match_start, lat: LatLocation) -> int:
        return abs(match_start - lat.start)

    def narrow_search_window(self, match_start, text, *, min_count=2, value=LINE_START_CHARS):
        match_start, text = self.narrow_search_window_pre(match_start, text, min_count=min_count, value=value)
        match_start, text = self.narrow_search_window_post(match_start, text, min_count=min_count, value=value)
        return match_start, text

    def narrow_search_window_pre(self, match_start, text, min_count=2, value=LINE_START_CHARS):
        i = match_start - 1
        while min_count > 0:
            if text[i] in value:
                min_count -= 1
        return match_start - i, text[i:]

    def narrow_search_window_post(self, match_start, text, min_count=2, value=LINE_START_CHARS):
        i = match_start + 1
        while min_count > 0:
            if text[i] in value:
                min_count -= 1
        return match_start, text[:i]

    def get_by_index(self, match_start, text, *,
                     strategy=LateralityLocatorStrategy.DEFAULT,
                     next_max=60, prev_max=100):
        match strategy:
            case LateralityLocatorStrategy.DEFAULT:
                return self._get_by_index_default(match_start, text, next_max=next_max, prev_max=prev_max)
            case LateralityLocatorStrategy.LINE_BREAK:
                match_start, text = self.narrow_search_window(match_start, text, min_count=2, value=LINE_START_CHARS)
                return self._get_by_index_default(match_start, text, next_max=next_max, prev_max=prev_max)
            case _:
                return self._get_by_index_default(match_start, text, next_max=next_max, prev_max=prev_max)

    def _get_by_index_default_helper_check_prev_lat(self, match_start, text, prev_lat, next_lat, count_letters,
                                                    prev_dist, next_max):
        """Refactored repeatedly-called method."""
        prev_commas = self.count_before(match_start, text, prev_lat, count_letters)
        if next_lat and (next_dist := self.distance(match_start, next_lat)) < next_max:
            next_commas = self.count_after(match_start, text, next_lat, count_letters)
            if next_commas == prev_commas:
                return prev_lat.laterality if prev_dist < next_dist else next_lat.laterality
            return prev_lat.laterality if prev_commas < next_commas else next_lat.laterality
        return prev_lat.laterality

    def _get_by_index_default(self, match_start, text, *, next_max=60, prev_max=100,
                              count_letters=DEFAULT_COUNT_LETTERS):
        prev_section_lat = self.get_previous_section(match_start, text)
        prev_lat, next_lat = self.get_previous_next_non_section(match_start, text)
        if prev_section_lat and (prev_section_dist := self.distance(match_start, prev_section_lat)) < prev_max:
            if prev_lat and (prev_dist := self.distance(match_start, prev_lat)) < prev_max:
                return self._get_by_index_default_helper_check_prev_lat(
                    match_start, text, prev_lat, next_lat, count_letters, prev_dist, next_max
                )
            elif next_lat and (next_dist := self.distance(match_start, next_lat)) < next_max:
                next_commas = self.count_after(match_start, text, next_lat, count_letters)
                prev_section_commas = self.count_before(match_start, text, prev_section_lat, count_letters)
                if next_commas == prev_section_commas:
                    return prev_section_lat.laterality
                return prev_section_lat.laterality if prev_section_commas < next_commas else next_lat.laterality
            return prev_section_lat.laterality
        else:
            if prev_lat and (prev_dist := self.distance(match_start, prev_lat)) < prev_max:
                return self._get_by_index_default_helper_check_prev_lat(
                    match_start, text, prev_lat, next_lat, count_letters, prev_dist, next_max
                )
            elif next_lat and (next_dist := self.distance(match_start, next_lat)) < next_max:
                return next_lat.laterality
        return self.default_laterality

    def __iter__(self):
        return iter(self.lateralities)


def get_laterality_by_index(lateralities, match_start, text):
    # lateralities: tuple of identified lateralities as: LateralityEnum, start_index, end_index, has ':' after
    prev_lat = None
    for lat, lat_start, lat_end, is_section_start in lateralities:
        if is_section_start:
            if lat_start > match_start:  # laterality is after the match
                if prev_lat:  # after and previous laterality found
                    return prev_lat
                return Laterality.UNKNOWN
            else:
                prev_lat = lat
        else:  # not followed by colon
            if len(text[lat_end:match_start]) < 10 and 'with' in text[lat_end:match_start]:
                return lat
    if lateralities:
        return lateralities[-1][0]
    return Laterality.OU  # default to both


def add_laterality_to_variable(data, laterality, variable, value):
    if laterality in {Laterality.OU, Laterality.OS}:
        data[f'{variable}_le'] = value
    if laterality in {Laterality.OU, Laterality.OD}:
        data[f'{variable}_re'] = value
    if laterality not in {Laterality.OU, Laterality.OD, Laterality.OS}:
        data[f'{variable}_unk'] = value
