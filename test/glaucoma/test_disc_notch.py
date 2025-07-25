import json

import pytest

from eye_extractor.glaucoma.disc_notch import NOTCH_PAT, extract_disc_notch
from eye_extractor.output.glaucoma import build_disc_notch
from eye_extractor.sections.document import create_doc_and_sections


@pytest.mark.parametrize('pat, text, exp', [
    (NOTCH_PAT, 'no notch', True),
    (NOTCH_PAT, 'no disc notches', True),
])
def test_notch_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) == exp


@pytest.mark.parametrize('text, sections, exp_disc_notch_re, exp_disc_notch_le, exp_disc_notch_unk', [
    ('no notching', None, -1, -1, 0),
    ('inferior notch was discovered OS', None, -1, 1, -1),
    ('sup notch OU', None, 1, 1, -1),
    ('slight notching superiorly', None, -1, -1, 1),
])
def test_notch_extract_and_build(text, sections, exp_disc_notch_re, exp_disc_notch_le, exp_disc_notch_unk):
    doc = create_doc_and_sections(text, sections)
    pre_json = extract_disc_notch(doc)
    post_json = json.loads(json.dumps(pre_json))
    result = build_disc_notch(post_json)
    assert result['disc_notch_re'] == exp_disc_notch_re
    assert result['disc_notch_le'] == exp_disc_notch_le
    assert result['disc_notch_unk'] == exp_disc_notch_unk
