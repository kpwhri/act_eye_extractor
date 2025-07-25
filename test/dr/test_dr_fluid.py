import json
import pytest

from eye_extractor.common.algo.fluid import extract_fluid
from eye_extractor.sections.document import create_doc_and_sections
from eye_extractor.output.dr import build_fluid
from eye_extractor.sections.patterns import SectionName


# Patterns tested in 'amd/test_fluid.py'


@pytest.mark.parametrize('text, sections, exp_fluid_re, exp_fluid_le, exp_fluid_unk', [
    ('', {SectionName.MACULA: 'subretinal fluid od'}, 'SUBRETINAL FLUID', 'UNKNOWN', 'UNKNOWN'),
    ('', {SectionName.MACULA: 'with fluid and exudates'}, 'UNKNOWN', 'UNKNOWN', 'INTRARETINAL FLUID'),
    ('no SRF/IRF OS', {}, 'UNKNOWN', 'NO SUB AND INTRARETINAL FLUID', 'UNKNOWN'),
    ('No heme or fluid od', {}, 'NO INTRARETINAL FLUID', 'UNKNOWN', 'UNKNOWN'),
    ('no IRF OU', {}, 'NO INTRARETINAL FLUID', 'NO INTRARETINAL FLUID', 'UNKNOWN')
])
def test_dr_fluid_extract_and_build(text, sections, exp_fluid_re, exp_fluid_le, exp_fluid_unk):
    doc = create_doc_and_sections(text, sections)
    pre_json = extract_fluid(doc)
    post_json = json.loads(json.dumps(pre_json))
    result = build_fluid(post_json, skip_rename_variable=True)
    assert result['fluid_dr_re'] == exp_fluid_re
    assert result['fluid_dr_le'] == exp_fluid_le
    assert result['fluid_dr_unk'] == exp_fluid_unk
