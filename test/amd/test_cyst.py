import pytest

from eye_extractor.amd.cyst import extract_macular_cyst
from eye_extractor.common.json import dumps_and_loads_json
from eye_extractor.headers import Headers
from eye_extractor.output.amd import build_macular_cyst


@pytest.mark.parametrize(
    'text, headers, exp_macular_cyst_re, exp_macular_cyst_le, exp_macular_cyst_unk, note_date', [
        ('', {'MACULA': 'cyst od'}, 1, -1, -1, None),
        ('OCT\nOD: sm cyst\nOS: stable', {}, 1, -1, -1, None),
        ('¶ OCT¶OS: sm cyst¶OD: no cyst', {}, 0, 1, -1, None),
    ])
def test_macular_cyst_extract_build(text, headers, exp_macular_cyst_re,
                                    exp_macular_cyst_le, exp_macular_cyst_unk, note_date):
    pre_json = extract_macular_cyst(text, headers=Headers(headers))
    post_json = dumps_and_loads_json(pre_json)
    result = build_macular_cyst(post_json, note_date=note_date)
    assert result['macular_cyst_re'] == exp_macular_cyst_re
    assert result['macular_cyst_le'] == exp_macular_cyst_le
    assert result['macular_cyst_unk'] == exp_macular_cyst_unk
