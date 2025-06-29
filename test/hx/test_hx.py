import pytest

from eye_extractor.history.common import find_end
from eye_extractor.sections.history import HISTORY_SECTION_PAT


@pytest.mark.parametrize('text, exp', [
    ('blah blah dr: yes gonioscopy: when', 'gonioscopy: when'),
    ('blah blah dr: YES gonioscopy: when', 'gonioscopy: when'),
    ('blah blah dr: amd: gonioscopy: when', 'gonioscopy: when'),
    ('blah blah diabetic retinopathy/dr: amd: gonioscopy: when', 'gonioscopy: when'),
])
def test_find_end(text, exp):
    idx = find_end(text, 0)
    assert text[idx:] == exp


@pytest.mark.parametrize('text, exp', [
    ('\npast ocular history of: disciform scar od', True),
])
def test_hx_section_pat(text, exp):
    m = HISTORY_SECTION_PAT.search(text)
    assert bool(m) == True
