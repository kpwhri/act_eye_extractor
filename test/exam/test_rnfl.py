import pytest

from eye_extractor.exam.rnfl import TABLE_HEADER_PAT, TABLE_ROW_PAT


@pytest.mark.parametrize('pat, text, exp', [
    (TABLE_HEADER_PAT, 'RNFL  SUP  INF  NAS  TEMP  GLOBAL', True),
    (TABLE_ROW_PAT, 'OD 107g 138g 90g 75g 103g', True),
    (TABLE_ROW_PAT, 'OS 107g 138g 90g 75g 103g', True),
    (TABLE_ROW_PAT, 'OS 107g 138g 90g N/q 103g', True),
])
def test_rnfl_patterns(pat, text, exp):
    assert bool(pat.search(text)) == exp
