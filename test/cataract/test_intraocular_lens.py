import json

import pytest

from eye_extractor.cataract.intraocular_lens import PCIOL_PAT, ACIOL_PAT, SIOL_PAT, PSEUDO_PAT, APHAKIA_PAT, IOL_PAT, \
    extract_iol_lens
from eye_extractor.sections.document import create_doc_and_sections
from eye_extractor.output.cataract import build_intraocular_lens
from eye_extractor.sections.patterns import SectionName


@pytest.mark.parametrize('pat, text, exp_match', [
    (PCIOL_PAT, 'pc iol', True),
    (PCIOL_PAT, 'pciol', True),
    (ACIOL_PAT, 'ac iol', True),
    (ACIOL_PAT, 'aciol', True),
    (SIOL_PAT, 'siol', True),
    (PSEUDO_PAT, 'pseudophakia', True),
    (APHAKIA_PAT, 'aphakia', True),
    (IOL_PAT, 'iol', True),
])
def test_iol_patterns(pat, text, exp_match):
    assert bool(pat.search(text)) == exp_match


@pytest.mark.parametrize('lens_text, exp_intraocular_lens_re, exp_intraocular_lens_le, exp_intraocular_lens_unk', [
    ('PCIOL od, ac iol os', 'PCIOL', 'ACIOL', 'UNKNOWN'),
    ('no PCIOL od', 'NO', 'UNKNOWN', 'UNKNOWN'),
    ('no PCIOL', 'UNKNOWN', 'UNKNOWN', 'NO'),
])
def test_extract_and_build_iol_lens(lens_text, exp_intraocular_lens_re,
                                    exp_intraocular_lens_le, exp_intraocular_lens_unk):
    doc = create_doc_and_sections('', section_dict={SectionName.LENS: lens_text})
    res = extract_iol_lens(doc)
    from_json = json.loads(json.dumps(res, default=str))
    variables = build_intraocular_lens(from_json)
    assert variables['intraocular_lens_re'] == exp_intraocular_lens_re
    assert variables['intraocular_lens_le'] == exp_intraocular_lens_le
    assert variables['intraocular_lens_unk'] == exp_intraocular_lens_unk
