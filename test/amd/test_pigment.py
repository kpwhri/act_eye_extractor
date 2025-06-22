import pytest

from eye_extractor.amd.pigment import PIGMENTARY_PAT, get_pigmentary_changes
from eye_extractor.sections.document import create_doc_and_sections


@pytest.mark.parametrize('text, exp', [
    ('pigment dispersion', 1),
    ('RPE changes', 1),
    ('RPE disruption', 1),
    ('RPE clumping and atrophy', 1),
    ('mottled RPE', 1),
    ('mild rpe changes ou', 1),
])
def test_pigmentary_pattern(text, exp):
    assert bool(PIGMENTARY_PAT.search(text)) == exp


@pytest.mark.parametrize('text, exp_value, exp_negword', [
    ('mild pigment dispersion', 1, None),
    ('no pigment dispersion', 0, 'no'),
    ('no drusen or pigment dispersion', 0, 'no'),
    ('no evidence of drusen or pigment dispersion', 0, 'or'),
    ('w/o evidence of pigment dispersion', 0, 'without'),
])
def test_pigment_value_first_variable(text, exp_value, exp_negword):
    doc = create_doc_and_sections(text)
    data = get_pigmentary_changes(doc)
    assert len(data) > 0
    first_variable = list(data[0].values())[0]
    assert first_variable['value'] == exp_value
    assert first_variable['negated'] == exp_negword
