import pytest

from eye_extractor.amd.drusen import find_drusen
from eye_extractor.common.json import dumps_and_loads_json
from eye_extractor.output.amd import get_drusen_size, get_drusen_type


@pytest.mark.parametrize('text, exp_size_le, exp_size_re, exp_type_le, exp_type_re, note_date', [
    ('WNL OU', -1, -1, -1, -1, None),
    ('drusen and RPE drop out OU', 4, 4, 4, 4, None),
])
def test_drusen(text, exp_size_le, exp_size_re, exp_type_le, exp_type_re, note_date):
    pre_json = find_drusen(text)
    post_json = dumps_and_loads_json(pre_json)
    size_result = get_drusen_size(post_json)
    type_result = get_drusen_type(post_json)
    # size
    assert size_result['drusen_size_le'] == exp_size_le
    assert size_result['drusen_size_re'] == exp_size_re
    # type
    assert type_result['drusen_type_le'] == exp_type_le
    assert type_result['drusen_type_re'] == exp_type_re
