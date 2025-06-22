import pytest

from eye_extractor.common.noteinfo import extract_note_level_info
from eye_extractor.sections.headers import Headers
from eye_extractor.laterality import Laterality


@pytest.mark.parametrize('text, headers, exp_set, exp_lat', [
    ('Patient is being treated for glaucoma and AMD.', None, {'is_glaucoma', 'is_amd'}, Laterality.UNKNOWN),
    ('', {'CHIEF_COMPLAINT': 'diabetic retinopathy'}, {'is_dr'}, Laterality.UNKNOWN),
])
def test_extract_note_level_info(text, headers, exp_set, exp_lat):
    res = extract_note_level_info(text, headers=Headers(headers))
    positive = {k for k, v in res.items() if v is True}  # eliminiate laterality too
    assert exp_set == positive
    assert exp_lat == res['default_lat']
