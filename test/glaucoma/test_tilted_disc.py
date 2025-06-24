import json

import pytest

from eye_extractor.glaucoma.tilted_disc import TILTED_PLUS_PAT, extract_tilted_disc, TILTED_PAT
from eye_extractor.output.glaucoma import build_tilted_disc
from eye_extractor.sections.document import create_doc_and_sections


@pytest.mark.parametrize('pat, text, exp', [
    (TILTED_PLUS_PAT, 'myopia tilted', True),
    (TILTED_PLUS_PAT, 'tilted myopic disc', True),
    (TILTED_PLUS_PAT, 'discs tilted', True),
    (TILTED_PAT, 'tilted', True),
    (TILTED_PAT, 'tilting', True),
])
def test_tilted_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) == exp


@pytest.mark.parametrize('text, sections, exp_tilted_disc_re, exp_tilted_disc_le, exp_tilted_disc_unk', [
    ('myopia tilted', None, -1, -1, 1),
    ('tilted myopic disc ou', None, 1, 1, -1),
    ('no tilted discs', None, -1, -1, 0),
    ('head tilted back', None, -1, -1, -1),
    ('tilting his glasses', None, -1, -1, -1),
    ('tilted and saucered IT OS', None, -1, 1, -1),
])
def test_tilted_extract_and_build(text, sections, exp_tilted_disc_re, exp_tilted_disc_le, exp_tilted_disc_unk):
    doc = create_doc_and_sections(text, sections)
    pre_json = extract_tilted_disc(doc)
    post_json = json.loads(json.dumps(pre_json))
    result = build_tilted_disc(post_json)
    assert result['tilted_disc_re'] == exp_tilted_disc_re
    assert result['tilted_disc_le'] == exp_tilted_disc_le
    assert result['tilted_disc_unk'] == exp_tilted_disc_unk
