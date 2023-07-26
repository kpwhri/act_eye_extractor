import json
import pytest

from eye_extractor.dr.dme_yesno import DME_YESNO_PAT
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
