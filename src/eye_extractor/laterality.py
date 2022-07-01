import enum
import re
from typing import Match


class Laterality(enum.IntEnum):
    OD = 1  # right
    OS = 2  # left
    OU = 3  # both/bilateral
    UNKNOWN = 4


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
    rf'\b({laterality_pattern})\b',
    re.IGNORECASE
)

LATERALITY_SPLIT_PATTERN = re.compile(  # for determining likely boundaries
    rf'\b({laterality_pattern}|:)\b',
    re.IGNORECASE
)


def laterality_finder(text):
    for m in LATERALITY_PATTERN.finditer(text):
        yield LATERALITY[m.group().upper()]


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


def build_laterality_table(text):
    lats = []
    for m in LATERALITY_PATTERN.finditer(text):
        is_lat = m.group() != ':'
        lats.append(
            (LATERALITY[m.group().upper()] if is_lat else None, m.start(), m.end(), is_lat)
        )
    return lats


def get_previous_laterality_from_table(table, index):
    for name, start, end, is_lat in reversed(table):
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


def create_variable(data, text, match, lateralities, variable, value):
    lat = get_laterality_for_term(lateralities, match, text)
    add_laterality_to_variable(data, lat, variable, value)


def create_new_variable(text, match, lateralities, variable, value):
    data = {}
    create_variable(data, text, match, lateralities, variable, value)
    return data


def get_laterality_for_term(lateralities, match: Match, text):
    """Get laterality for a particular match by its index, so `match` must have been found in `text`"""
    return get_laterality_by_index(lateralities, match.start(), text)


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
