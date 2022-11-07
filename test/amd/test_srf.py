from datetime import date

import pytest

from eye_extractor.common.algo.fluid import extract_fluid
from eye_extractor.common.json import dumps_and_loads_json
from eye_extractor.headers import Headers
from eye_extractor.output.amd import build_subretfluid_amd


@pytest.mark.parametrize('text, headers, srf_re, srf_le, srf_unk, note_date', [
    ('resolved SRF OD', None, 0, -1, -1, None),
    ('OCT resolved SRF OD', None, 0, -1, -1, date(2022, 2, 20)),
])
def test_amd(text, headers, srf_re, srf_le, srf_unk, note_date):
    pre_json = extract_fluid(text, headers=Headers(headers))
    post_json = dumps_and_loads_json(pre_json)
    result = build_subretfluid_amd(post_json, note_date=note_date)
    assert result['amd_subretfluid_re'] == srf_re
    assert result['amd_subretfluid_le'] == srf_le
    assert result['amd_subretfluid_unk'] == srf_unk
