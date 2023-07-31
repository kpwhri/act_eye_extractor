import json
import pytest

from eye_extractor.common.get_variable import get_variable
from eye_extractor.dr.dme_yesno import DME_YESNO_PAT, get_dme_yesno
from eye_extractor.headers import Headers
from eye_extractor.output.dr import build_dme_yesno

# Test pattern.
_pattern_cases = [
    (DME_YESNO_PAT, 'DME', True),
    (DME_YESNO_PAT, 'diabetic macular edema', True),
    (DME_YESNO_PAT, 'csme', True),
    (DME_YESNO_PAT, 'diabetic retinopathy of right eye with macular edema', True),
    (DME_YESNO_PAT, 'diabetic retinopathy of left eye with macular edema', True),
]


def _get_pattern_cases():
    return [(x[0], x[1], x[2]) for x in _pattern_cases]


@pytest.mark.parametrize('pat, text, exp', _get_pattern_cases())
def test_dme_yesno_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) == exp


# Test extract and build.
_dme_yesno_extract_and_build_cases = [
    ('Patient presents with: Diabetic macular edema E11.311', {}, -1, -1, 1),

]


@pytest.mark.parametrize('text, headers, '
                         'exp_dmacedema_yesno_re, exp_dmacedema_yesno_le, exp_dmacedema_yesno_unk',
                         _dme_yesno_extract_and_build_cases)
def test_dme_yesno_extract_and_build(text,
                                     headers,
                                     exp_dmacedema_yesno_re,
                                     exp_dmacedema_yesno_le,
                                     exp_dmacedema_yesno_unk):
    pre_json = get_variable(text, get_dme_yesno, headers=Headers(headers))
    post_json = json.loads(json.dumps(pre_json))
    result = build_dme_yesno(post_json)
    assert result['dmacedema_yesno_re'] == exp_dmacedema_yesno_re
    assert result['dmacedema_yesno_le'] == exp_dmacedema_yesno_le
    assert result['dmacedema_yesno_unk'] == exp_dmacedema_yesno_unk
