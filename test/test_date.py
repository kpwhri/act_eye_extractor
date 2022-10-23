import datetime
import re

import pytest

from eye_extractor.common.date import parse_date, parse_date_after, parse_date_before, parse_all_dates, \
    parse_nearest_date_to_line_start


@pytest.mark.parametrize('text, exp', [
    ('27 jan 2022', datetime.date(2022, 1, 27)),
    ('01/27/2022', datetime.date(2022, 1, 27)),
    ('january 2022', datetime.date(2022, 1, 17)),  # default day is '17'
    ('22 january 2022', datetime.date(2022, 1, 22)),  # default day is '17'
    ('2020', datetime.date(2020, 2, 17)),  # default day is '17'
])
def test_parse_date(text, exp):
    assert parse_date(text) == exp


@pytest.mark.parametrize('pattern, text, exp', [
    ('surgery', 'surgery 2/2012', datetime.date(2012, 2, 17)),
    ('surgery', 'surgery 2012', datetime.date(2012, 2, 17)),
])
def test_parse_date_after(pattern, text, exp):
    pat = re.compile(pattern, re.I)
    m = pat.search(text)
    assert m is not None
    dt = parse_date_after(m, text)
    assert dt == exp


@pytest.mark.parametrize('pattern, text, exp', [
    ('surgery', '2/2012 surgery', datetime.date(2012, 2, 17)),
    ('surgery', '2012 surgery', datetime.date(2012, 2, 17)),
])
def test_parse_date_before(pattern, text, exp):
    pat = re.compile(pattern, re.I)
    m = pat.search(text)
    assert m is not None
    dt = parse_date_before(m, text)
    assert dt == exp


@pytest.mark.parametrize('text, exp', [
    ('04/16/2012 that 22 january 2022', [datetime.date(2012, 4, 16), datetime.date(2022, 1, 22)]),
])
def test_parse_all_dates(text, exp):
    dates = parse_all_dates(text)
    assert [x[1] for x in dates] == exp


@pytest.mark.parametrize('start, text, exp_date', [
    (-1, '04/16/2012 this 04/17/2012 that', datetime.date(2012, 4, 17)),
    (-1, '12/5/2010 not dry 10/4/2022 dry', datetime.date(2022, 10, 4)),
    (-1, '04/16/2012\nthat', None),
    (-1, '04/16/2012¶that', None),
    (-1, '¶04/16/2012 ldkfj kdfj dkjf', datetime.date(2012, 4, 16)),
])
def test_previous_date_in_line(start, text, exp_date):
    date = parse_nearest_date_to_line_start(start, text)
    assert date == exp_date
