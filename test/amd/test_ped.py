import json

import pytest

from eye_extractor.amd.ped import PED_PAT, extract_ped
from eye_extractor.sections.document import create_doc_and_sections
from eye_extractor.output.amd import build_ped


@pytest.mark.parametrize('pat, text, exp', [
    (PED_PAT, 'pigment epithelial detachment', True),
    (PED_PAT, 'detachment of the retinal pigment epithelium', True),
    (PED_PAT, 'ped', True),
    (PED_PAT, 'PEDs', True),
    (PED_PAT, 'RPED', True),
])
def test_ped_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) is exp


@pytest.mark.parametrize('text, sections, exp_ped_re, exp_ped_le, exp_ped_unk', [
        ('', {'MACULA': 'retinal pigment epithelial detachment and drusen'}, -1, -1, 1),
        ('', {'MACULA': 'no PED OD'}, 0, -1, -1),
        ('', {'MACULA': 'OU: PEDs'}, 1, 1, -1),
        ('', {'MACULA': '-PED'}, -1, -1, 0),
    ])
def test_ped_extract_build(text, sections, exp_ped_re, exp_ped_le, exp_ped_unk, ):
    doc = create_doc_and_sections(text, sections)
    pre_json = extract_ped(doc)
    post_json = json.loads(json.dumps(pre_json))
    result = build_ped(post_json)
    assert result['ped_re'] == exp_ped_re
    assert result['ped_le'] == exp_ped_le
    assert result['ped_unk'] == exp_ped_unk
