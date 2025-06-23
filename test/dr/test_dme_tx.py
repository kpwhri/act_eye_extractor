import json
import pytest

from eye_extractor.common.algo.treatment import extract_treatment, GRID_PAT, MACULAR_PAT
from eye_extractor.sections.document import create_doc_and_sections
from eye_extractor.output.dr import build_dme_tx
from eye_extractor.sections.patterns import SectionName

# Test pattern.
_pattern_cases = [
    (GRID_PAT, 'yes - laser grid', True),
    (GRID_PAT, 'grid laser for DME', True),
    (MACULAR_PAT, 'macular laser', True),
]


def _get_pattern_cases():
    return [(x[0], x[1], x[2]) for x in _pattern_cases]


@pytest.mark.parametrize('pat, text, exp', _get_pattern_cases())
def test_dme_tx_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) == exp


# Test extract and build.
_dme_tx_extract_and_build_cases = [
    ('', {SectionName.PLAN: 'observe'}, -1, -1, 1),
    ('grid laser for DME os', {}, -1, 2, -1),
    ('Eye surgery: yes - laser grid OD', {}, 2, -1, -1),
    ('', {SectionName.PLAN: 'repeat grid laser os'}, -1, 2, -1),
    ('', {SectionName.MACULA: 'laser OU'}, 2, 2, -1),
    ('macular laser OS.', {}, -1, 2, -1),
    ('', {SectionName.PLAN: 'macular laser'}, -1, -1, 2),
    ('injection of Avastin (Bevacizumab)', {}, -1, -1, 4),
    ('', {SectionName.PLAN: 'anti-VEGF intravitreal injections'}, -1, -1, 4),
    ('INJ AFLIBERCEPT (EYELEA)', {}, -1, -1, 4),
    ('', {SectionName.PLAN: 'continue meds'}, -1, -1, 5)
]


@pytest.mark.parametrize('text, sections, exp_dmacedema_tx_re, exp_dmacedema_tx_le, exp_dmacedema_tx_unk',
                         _dme_tx_extract_and_build_cases)
def test_dme_tx_extract_and_build(text, sections, exp_dmacedema_tx_re, exp_dmacedema_tx_le, exp_dmacedema_tx_unk):
    doc = create_doc_and_sections(text, sections)
    pre_json = extract_treatment(doc)
    post_json = json.loads(json.dumps(pre_json))
    result = build_dme_tx(post_json)
    assert result['dmacedema_tx_re'] == exp_dmacedema_tx_re
    assert result['dmacedema_tx_le'] == exp_dmacedema_tx_le
    assert result['dmacedema_tx_unk'] == exp_dmacedema_tx_unk
