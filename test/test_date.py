import datetime

import pytest

from eye_extractor.common.date import parse_date


@pytest.mark.parametrize('text, exp', [
    ('27 jan 2022', datetime.date(2022, 1, 27)),
    ('01/27/2022', datetime.date(2022, 1, 27)),
    ('january 2022', datetime.date(2022, 1, 17)),  # default day is '17'
])
def test_parse_date(text, exp):
    assert parse_date(text) == exp
