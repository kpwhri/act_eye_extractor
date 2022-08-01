import datetime
import re

import pytest

from eye_extractor.common.date import parse_date, parse_date_after, parse_date_before


@pytest.mark.parametrize('text, exp', [
    ('27 jan 2022', datetime.date(2022, 1, 27)),
    ('01/27/2022', datetime.date(2022, 1, 27)),
    ('january 2022', datetime.date(2022, 1, 17)),  # default day is '17'
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
