import enum
import re
from typing import Match, Optional

from sortedcontainers import SortedList

from eye_extractor.common.date import parse_nearest_date_to_line_start


class Laterality(enum.IntEnum):
    OD = 1  # right
    OS = 2  # left
    OU = 3  # both/bilateral
    UNKNOWN = 0  # keep 0 so that it will test 'False'


LATERALITY = {
    'OD': Laterality.OD,
    'O.D.': Laterality.OD,
    'RE': Laterality.OD,
    'R.E.': Laterality.OD,
    'RIGHT': Laterality.OD,
    'R': Laterality.OD,
    'L': Laterality.OS,
    'OS': Laterality.OS,
    'O.S.': Laterality.OS,
    'LE': Laterality.OS,
    'L.E.': Laterality.OS,
    'LEFT': Laterality.OS,
    'BOTH': Laterality.OU,
    # 'BE': Laterality.OU,  # ambiguous
    'OU': Laterality.OU,
    'O.U.': Laterality.OU,
    'BILATERAL': Laterality.OU
}

od_pattern = '|'.join(k for k, v in LATERALITY.items() if v == Laterality.OD).replace('.', r'\.')
os_pattern = '|'.join(k for k, v in LATERALITY.items() if v == Laterality.OS).replace('.', r'\.')
ou_pattern = '|'.join(k for k, v in LATERALITY.items() if v == Laterality.OU).replace('.', r'\.')

laterality_pattern = '|'.join(LATERALITY.keys()).replace('.', r'\.')

LATERALITY_PATTERN = re.compile(
    rf'\b({laterality_pattern})\b\s*:?',
    re.IGNORECASE
)

LATERALITY_SPLIT_PATTERN = re.compile(  # for determining likely boundaries
    rf'\b({laterality_pattern}|:)\b',
    re.IGNORECASE
)

LATERALITY_PLUS_COLON_PATTERN = re.compile(
    rf'\b(?:{laterality_pattern})\W*:'
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
    return LATERALITY[m.group(group).upper().strip().strip(':').strip()]


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
    if isinstance(value, dict) and 'date' not in value:  # skip if alternative way of finding date
        value['date'] = parse_nearest_date_to_line_start(match.start(), text)
    # laterality
    lat = known_laterality or get_laterality_for_term(
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


def get_laterality_for_term(lateralities, match: Match, text):
    """Get laterality for a particular match by its index, so `match` must have been found in `text`"""
    return lateralities.get_by_index(match.start(), text)


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
                if lat.start < match_start:  # laterality before match index
                    last_found_lat = None  # reset this value
                else:  # laterality section first after match index, so no after
                    return last_found_lat, None
            else:
                if lat.start < match_start:  # before, so store it
                    last_found_lat = lat
                else:  # after, return this and the previous
                    return last_found_lat, lat
        return last_found_lat, None  # nothing found after

    def contains_before(self, match_start, text, lat: LatLocation, value) -> int:
        return text[lat.start:match_start].count(value)

    def contains_after(self, match_start, text, lat: LatLocation, value) -> int:
        return text[match_start:lat.start].count(value)

    def distance(self, match_start, lat: LatLocation) -> int:
        return abs(match_start - lat.start)

    def get_by_index(self, match_start, text):
        prev_section_lat = self.get_previous_section(match_start, text)
        prev_lat, next_lat = self.get_previous_next_non_section(match_start, text)
        next_max = 60
        prev_max = 100
        if prev_section_lat and (prev_section_dist := self.distance(match_start, prev_section_lat)) < prev_max:
            if prev_lat and (prev_dist := self.distance(match_start, prev_lat)) < prev_max:
                prev_commas = self.contains_before(match_start, text, prev_lat, ',')
                if next_lat and (next_dist := self.distance(match_start, prev_lat)) < next_max:
                    next_commas = self.contains_after(match_start, text, next_lat, ',')
                    if next_commas == prev_commas:
                        return prev_lat.laterality if prev_dist < next_dist else next_lat.laterality
                    return prev_lat.laterality if prev_commas < next_commas else next_lat.laterality
                return prev_lat.laterality
            elif next_lat and (next_dist := self.distance(match_start, next_lat)) < next_max:
                next_commas = self.contains_after(match_start, text, next_lat, ',')
                prev_section_commas = self.contains_before(match_start, text, prev_section_lat, ',')
                if next_commas == prev_section_commas:
                    return prev_section_lat.laterality
                return prev_section_lat.laterality if prev_section_commas < next_commas else next_lat.laterality
            return prev_section_lat.laterality
        else:
            if prev_lat and (prev_dist := self.distance(match_start, prev_lat)) < prev_max:
                prev_commas = self.contains_before(match_start, text, prev_lat, ',')
                if next_lat and (next_dist := self.distance(match_start, prev_lat)) < next_max:
                    next_commas = self.contains_after(match_start, text, next_lat, ',')
                    if next_commas == prev_commas:
                        return prev_lat.laterality if prev_dist < next_dist else next_lat.laterality
                    return prev_lat.laterality if prev_commas < next_commas else next_lat.laterality
                return prev_lat.laterality
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
