import json
import pytest

from eye_extractor.dr.venous_beading import get_ven_beading, VEN_BEADING_PAT
from eye_extractor.output.dr import build_ven_beading
from eye_extractor.sections.document import create_doc_and_sections
from eye_extractor.sections.patterns import SectionName

# Test pattern.
_pattern_cases = [
    (VEN_BEADING_PAT, 'Venous beading', True),
    (VEN_BEADING_PAT, 'VB', True),
    (VEN_BEADING_PAT, 'venous beading;', True),
]


def _get_pattern_cases():
    return [(x[0], x[1], x[2]) for x in _pattern_cases]


@pytest.mark.parametrize('pat, text, exp', _get_pattern_cases())
def test_ven_beading_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) == exp


# Test extract and build.
_ven_beading_extract_and_build_cases = [
    ('venous beading ou', {}, 'YES NOS', 'YES NOS', 'UNKNOWN'),
    ('mild VB OU', {}, 'MILD', 'MILD', 'UNKNOWN'),
    ('Mild - moderate venous beading OD', {}, 'MODERATE', 'UNKNOWN', 'UNKNOWN'),
    ('no venous beading ou', {}, 'NONE', 'NONE', 'UNKNOWN'),
    ('moderate VB OS', {}, 'UNKNOWN', 'MODERATE', 'UNKNOWN'),
    ('severe venous beading', {}, 'UNKNOWN', 'UNKNOWN', 'SEVERE'),
    ('VB severity=3Q OS', {}, 'UNKNOWN', 'Q3', 'UNKNOWN'),
    ('venous beading temporal and inferior quadrant OD', {}, 'Q2', 'UNKNOWN', 'UNKNOWN'),
    ('nasal quadrant, VB', {}, 'UNKNOWN', 'UNKNOWN', 'Q1'),
    ('VB in all quadrants ou', {}, 'Q4', 'Q4', 'UNKNOWN'),
    ('(-)heme, MA, HE, CWS, VB, IRMA, NVE OU', {}, 'NONE', 'NONE', 'UNKNOWN'),
    ('OU: No Microaneurysms/hemes, cotton-wool spots, exudates, IRMA, Venous beading',
     {}, 'NONE', 'NONE', 'UNKNOWN'),
    ('no venous beading;', {}, 'UNKNOWN', 'UNKNOWN', 'NONE'),
    ('Vessels: moderate A/V crossing changes, no venous beading',
     {}, 'UNKNOWN', 'UNKNOWN', 'NONE'),
    ('Vessels: Normal', {}, 'UNKNOWN', 'UNKNOWN', 'UNKNOWN'),
    ('Macula: focal OU; no CSME; ERM OS Vessels: good caliber and crossings; no venous beading; no plaques or emboli',
     {
         SectionName.MACULA: 'focal OU; no CSME; ERM OS',
         SectionName.VESSELS: 'good caliber and crossings; no venous beading; no plaques or emboli'
     },
     'UNKNOWN', 'UNKNOWN', 'NONE'),
    ('¶Macula: no CSME mild ERM OD ¶Vessels: good caliber and crossings; no venous beading; no plaques or emboli',
     {
         SectionName.MACULA: 'no CSME mild ERM OD',
         SectionName.VESSELS: 'good caliber and crossings; no venous beading; no plaques or emboli'
     },
     'UNKNOWN', 'UNKNOWN', 'NONE'),
    # Unless specified, all conditions in negated list are OU.
    # Since no laterality specified, laterality should be OU.
    ('no CWS, MA, IRMA, VB', {}, 'NONE', 'NONE', 'UNKNOWN'),
    ('(-) MAs, Venous Beading, IRMA, CWS', {}, 'NONE', 'NONE', 'UNKNOWN'),
    ('Vessels: good caliber, color, and crossings OU, no plaques or emboli OU (-) MAs, Venous Beading, IRMA, CWS',
     {}, 'NONE', 'NONE', 'UNKNOWN'),
    ('Macula: flat, dry (-)heme, MA, HE, CWS, VB, IRMA, NVE OD, ERM OS', {}, 'NONE', 'NONE', 'UNKNOWN'),
    ('Macula: flat, dry (-)heme, MA, HE, CWS, VB, IRMA, NVE OD, ERM OS',
     {
         SectionName.VESSELS: 'flat, dry (-)heme, MA, HE, CWS, VB, IRMA, NVE OD, ERM OS'
     },
     'NONE', 'NONE', 'UNKNOWN'),
    ('',
     {
         SectionName.MACULA: 'flat, dry (-)heme, MA, HE, CWS, VB, IRMA, NVE OD, ERM OS'
     },
     'NONE', 'NONE', 'UNKNOWN'),

]


@pytest.mark.parametrize('text, sections, exp_venbeading_re, exp_venbeading_le, exp_venbeading_unk',
                         _ven_beading_extract_and_build_cases)
def test_ven_beading_extract_and_build(text,
                                       sections,
                                       exp_venbeading_re,
                                       exp_venbeading_le,
                                       exp_venbeading_unk):
    doc = create_doc_and_sections(text, sections)
    pre_json = get_ven_beading(doc)
    post_json = json.loads(json.dumps(pre_json))
    result = build_ven_beading(post_json)
    assert result['venbeading_re'] == exp_venbeading_re
    assert result['venbeading_le'] == exp_venbeading_le
    assert result['venbeading_unk'] == exp_venbeading_unk
