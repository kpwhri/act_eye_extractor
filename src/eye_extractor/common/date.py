import datetime
import re
from typing import Match

from loguru import logger

from dateutil.parser import parse, ParserError

from eye_extractor.nlp.character_groups import LINE_START_CHARACTERS, get_previous_text_to_newline

month_name = r'(?:\b(?P<month_name>jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*\b)'
month = r'(?P<month>\d{1,2})'
day = r'(?P<day>\d{1,2})'
year = r'(?P<year>\d{2,4})'
long_year = r'(?P<year>\d{4})'

DATE_PAT1 = re.compile(
    rf'\b(?:'
    rf'{month}\W+{day}\W+{year}'  # 02/04/2022
    rf')\b',
    re.I
)
DATE_PAT2 = re.compile(
    rf'\b(?:'
    rf'{day}\W+(?:{month_name})\W+{year}'  # 4 February 2022
    rf')\b',
    re.I
)
DATE_PAT3 = re.compile(
    rf'\b(?:'
    rf'(?:{month_name})\W+{day}\W+{year}'  # February 4, 2022
    rf')\b',
    re.I
)
DATE_PAT4 = re.compile(
    rf'\b(?:'
    rf'(?:{month_name}|{month})\W+{long_year}'  # February 2022 | 02/2022
    rf')\b',
    re.I
)

DATE_PAT5 = re.compile(
    r'\b(?P<year>\d{4})\b'
)

MONTHS = {
    'jan': 1,
    'feb': 2,
    'mar': 3,
    'apr': 4,
    'may': 5,
    'jun': 6,
    'jul': 7,
    'aug': 8,
    'sep': 9,
    'oct': 10,
    'nov': 11,
    'dec': 12,
    None: 2,  # default to feb
}


def parse_date(text):
    """Look for date in text and return datetime object"""
    for pat in [DATE_PAT1, DATE_PAT2, DATE_PAT3, DATE_PAT4, DATE_PAT5]:
        if m := pat.search(text):
            data = m.groupdict()
            curr_day = data.get('day', 17)  # default to 17, close to mid-month
            curr_month = data.get('month', None) or MONTHS[data.get('month_name', None)]
            curr_year = data.get('year')
            try:
                return datetime.date(int(curr_year), int(curr_month), int(curr_day))
            except Exception as e:
                logger.error(f'Failed to parse datetime: {m.group()} with {str(e)}')
    try:
        return parse(text, fuzzy=True)
    except ParserError as e:
        return None  # date wasn't required in this string


def parse_all_dates(text):
    """Look for date in text and return datetime object"""
    dates = []
    for i, pat in enumerate([DATE_PAT1, DATE_PAT2, DATE_PAT3, DATE_PAT4, DATE_PAT5], start=1):
        if i == 4 and len(dates) > 0:
            break  # don't rely on month only
        if i == 5 and len(dates) > 0:
            break  # don't just rely on year-only
        for m in pat.finditer(text):
            data = m.groupdict()
            curr_day = data.get('day', 17)  # default to 17, close to mid-month
            curr_month = data.get('month', None) or MONTHS[data.get('month_name', None)]
            curr_year = data.get('year')
            if i == 5:  # if only year found
                try:
                    curr = parse(text[m.end() - 20: m.end() + 1], fuzzy=True)
                except ParserError as e:
                    logger.error(f'Failed to parse datetime (just year) in: {text[m.end() - 20: m.end() + 1]}')
                    continue
            else:
                try:
                    curr = datetime.date(int(curr_year), int(curr_month), int(curr_day))
                except Exception as e:
                    logger.error(f'Failed to parse datetime: {m.group()} with {str(e)}')
                    continue
            dates.append((m.start(), curr))
    return sorted(dates)  # sort by index


def date_as_string(dt):
    return dt.strftime('%Y-%m-%d') if dt is not None else None


def parse_date_before(m: Match, text, *, characters=20, as_string=False):
    """Look for date after a particular match"""
    dt = parse_date(text[max(0, m.start() - characters): m.start()])
    return date_as_string(dt) if as_string else dt


def parse_date_after(m: Match, text, *, characters=20, as_string=False):
    """Look for date before a regex match"""
    dt = parse_date(text[m.end(): m.end() + characters])
    return date_as_string(dt) if as_string else dt


def parse_nearest_date_to_line_start(start, text, *, line_start_chars=LINE_START_CHARACTERS):
    """Get most recent date in current line."""
    if line_start_chars:
        line = get_previous_text_to_newline(start, text, line_start_chars=line_start_chars)
    else:
        line = text
    dates = parse_all_dates(line)
    if dates:
        return dates[-1][1]  # return most recent date
    return None
