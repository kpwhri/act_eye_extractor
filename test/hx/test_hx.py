import pytest

from eye_extractor.history.common import find_end


@pytest.mark.parametrize('text, exp', [
    ('blah blah dr: yes gonioscopy: when', 'gonioscopy: when'),
    ('blah blah dr: YES gonioscopy: when', 'gonioscopy: when'),
    ('blah blah dr: amd: gonioscopy: when', 'gonioscopy: when'),
    ('blah blah diabetic retinopathy/dr: amd: gonioscopy: when', 'gonioscopy: when'),
])
def test_find_end(text, exp):
    idx = find_end(text, 0)
    assert text[idx:] == exp
