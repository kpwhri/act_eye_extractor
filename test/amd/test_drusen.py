import datetime

import pytest

from eye_extractor.amd.drusen import find_drusen
from eye_extractor.common.json import dumps_and_loads_json
from eye_extractor.output.amd import get_drusen_size, get_drusen_type


@pytest.mark.parametrize('text, exp_size_re, exp_size_le, exp_type_re, exp_type_le, note_date', [
    ('WNL OU', -1, -1, -1, -1, None),
    ('w/o drusen ou', 0, 0, 0, 0, None),
    ('drusen and RPE drop out OU', 4, 4, 4, 4, None),
    ('OD: extensive drusen', 3, -1, 4, -1, None),
    ('OD: 10/2/2011 extensive drusen', -1, -1, -1, -1, datetime.date(2011, 10, 9)),
    ('OD: 10/2/2011 no drusen 10/9/2011 extensive drusen', 3, -1, 4, -1, datetime.date(2011, 10, 9)),
    ('OD: 10/9/2011 no drusen 10/2/2011 extensive drusen', 0, -1, 0, -1, datetime.date(2011, 10, 9)),
    ('OD: no drusen OS: lots of drusen', 0, 3, 0, 4, None),
    ('intermediate drusen od, heavy drusen os', 2, 3, 4, 4, None),
])
def test_drusen(text, exp_size_re, exp_size_le, exp_type_re, exp_type_le, note_date):
    pre_json = find_drusen(text)
    post_json = dumps_and_loads_json(pre_json)
    size_result = get_drusen_size(post_json, note_date=note_date)
    type_result = get_drusen_type(post_json, note_date=note_date)
    # size
    assert size_result['drusen_size_le'] == exp_size_le
    assert size_result['drusen_size_re'] == exp_size_re
    # type
    assert type_result['drusen_type_le'] == exp_type_le
    assert type_result['drusen_type_re'] == exp_type_re
