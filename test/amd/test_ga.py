import json

import pytest

from eye_extractor.amd.ga import GA_PAT, extract_geoatrophy
from eye_extractor.sections.document import create_doc_and_sections
from eye_extractor.output.amd import build_geoatrophy


@pytest.mark.parametrize('pat, text, exp', [
    (GA_PAT, 'ga', True),
    (GA_PAT, 'gauge', False),
    (GA_PAT, 'geographic atrophy', True),
])
def test_ga_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) is exp


@pytest.mark.parametrize('text, sections, exp_geoatrophy_re, exp_geoatrophy_le, exp_geoatrophy_unk', [
    ('', {'MACULA': 'ga'}, -1, -1, 1),
    ('', {'MACULA': 'no ga'}, -1, -1, 0),
    ('', {'MACULA': 'w/o ga'}, -1, -1, 0),
])
def test_ga_extract_build(text, sections, exp_geoatrophy_re, exp_geoatrophy_le, exp_geoatrophy_unk):
    doc = create_doc_and_sections(text, sections)
    pre_json = extract_geoatrophy(doc)
    post_json = json.loads(json.dumps(pre_json))
    result = build_geoatrophy(post_json)
    assert result['geoatrophy_re'] == exp_geoatrophy_re
    assert result['geoatrophy_le'] == exp_geoatrophy_le
    assert result['geoatrophy_unk'] == exp_geoatrophy_unk
