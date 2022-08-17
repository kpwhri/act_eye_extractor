import datetime
import json

import pytest

from eye_extractor.exam.rnfl import TABLE_HEADER_PAT, TABLE_ROW_PAT, extract_rnfl_values
from eye_extractor.output.exam import build_rnfl


@pytest.mark.parametrize('pat, text, exp', [
    (TABLE_HEADER_PAT, 'RNFL  SUP  INF  NAS  TEMP  GLOBAL', True),
    (TABLE_ROW_PAT, 'OD 107g 138g 90g 75g 103g', True),
    (TABLE_ROW_PAT, 'OS 107g 138g 90g 75g 103g', True),
    (TABLE_ROW_PAT, 'OS 107g 138g 90g N/q 103g', True),
])
def test_rnfl_patterns(pat, text, exp):
    assert bool(pat.search(text)) == exp


@pytest.mark.parametrize(
    'text, headers, rnfloct_globalscore_re, rnfloct_globalscore_le, '
    'rnfloct_temporal_sup_re, rnfloct_temporal_sup_le, '
    'rnfloct_temporal_re, rnfloct_temporal_le, '
    'rnfloct_temporal_inf_re, rnfloct_temporal_inf_le, '
    'rnfloct_nasal_inf_re, rnfloct_nasal_inf_le, '
    'rnfloct_nasal_re, rnfloct_nasal_le, '
    'rnfloct_nasal_sup_re, rnfloct_nasal_sup_le, '
    'rnfloct_thinning_re, rnfloct_thinning_le, rnfloct_thinning_unk', [
        ('5-11-1912 RNFL Sup Inf Nas Temp Global OD 107g 138g 90g 75g 103g OS 123g 108g 194g N/q 117g', {},
         103, 117, 107, 123, 75, -1, 138, 108, -1, -1, 90, 194, -1, -1, -1, -1, -1),
        ('RNFL Sup Inf Nas Temp Global OD 93y 79r 55g 70g 75y stable OS 76r 92y 56g 58g 70r Thinning inf rim', {},
         75, 70, 93, 76, 70, 58, 79, 92, -1, -1, 55, 56, -1, -1, -1, 1, -1),
        ('RNFL no thinning', {},
         -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0),
])
def test_rnfl_extract_build(text, headers, rnfloct_globalscore_re, rnfloct_globalscore_le, rnfloct_temporal_sup_re,
                            rnfloct_temporal_sup_le, rnfloct_temporal_re, rnfloct_temporal_le, rnfloct_temporal_inf_re,
                            rnfloct_temporal_inf_le, rnfloct_nasal_inf_re, rnfloct_nasal_inf_le, rnfloct_nasal_re,
                            rnfloct_nasal_le, rnfloct_nasal_sup_re, rnfloct_nasal_sup_le, rnfloct_thinning_re,
                            rnfloct_thinning_le, rnfloct_thinning_unk):
    pre_json = extract_rnfl_values(text, headers=headers)
    post_json = json.loads(json.dumps(pre_json))
    result = build_rnfl(post_json, note_date=datetime.datetime(2020, 1, 1))
    assert result.get('rnfloct_globalscore_re', -1) == rnfloct_globalscore_re
    assert result.get('rnfloct_globalscore_le', -1) == rnfloct_globalscore_le
    assert result.get('rnfloct_temporal_sup_re', -1) == rnfloct_temporal_sup_re
    assert result.get('rnfloct_temporal_sup_le', -1) == rnfloct_temporal_sup_le
    assert result.get('rnfloct_temporal_re', -1) == rnfloct_temporal_re
    assert result.get('rnfloct_temporal_le', -1) == rnfloct_temporal_le
    assert result.get('rnfloct_temporal_inf_re', -1) == rnfloct_temporal_inf_re
    assert result.get('rnfloct_temporal_inf_le', -1) == rnfloct_temporal_inf_le
    assert result.get('rnfloct_nasal_inf_re', -1) == rnfloct_nasal_inf_re
    assert result.get('rnfloct_nasal_inf_le', -1) == rnfloct_nasal_inf_le
    assert result.get('rnfloct_nasal_re', -1) == rnfloct_nasal_re
    assert result.get('rnfloct_nasal_le', -1) == rnfloct_nasal_le
    assert result.get('rnfloct_nasal_sup_re', -1) == rnfloct_nasal_sup_re
    assert result.get('rnfloct_nasal_sup_le', -1) == rnfloct_nasal_sup_le
    assert result.get('rnfloct_thinning_re', -1) == rnfloct_thinning_re
    assert result.get('rnfloct_thinning_le', -1) == rnfloct_thinning_le
    assert result.get('rnfloct_thinning_unk', -1) == rnfloct_thinning_unk
