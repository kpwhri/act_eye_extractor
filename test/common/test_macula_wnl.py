import datetime

import pytest

from eye_extractor.common.algo.macula_wnl import extract_macula_wnl
from eye_extractor.common.json import dumps_and_loads_json
from eye_extractor.headers import Headers
from eye_extractor.output.amd import build_amd
from eye_extractor.output.common import macula_is_wnl


@pytest.mark.parametrize('data, date, exp', [
    ({'value': 1, 'date': None}, datetime.date(2012, 12, 12), True),
    ({'value': 1, 'date': datetime.date(2012, 12, 12)}, datetime.date(2012, 12, 12), True),
    ({'value': 1, 'date': datetime.date(2012, 12, 19)}, datetime.date(2012, 12, 12), False),
])
def test_macula_is_wnl(data, date, exp):
    res = macula_is_wnl(data, date)
    assert res == exp


@pytest.mark.parametrize('text, headers, amd_re, amd_le', [
    ('', {'MACULA': 'WNL OU'}, 0, 0),
])
def test_macula_wnl_on_amd(text, headers, amd_re, amd_le):
    pre_json = extract_macula_wnl(text, headers=Headers(headers))
    post_json = dumps_and_loads_json(pre_json)
    result = build_amd(None, macula_wnl=post_json)
    assert result['amd_re'] == amd_re
    assert result['amd_le'] == amd_le
