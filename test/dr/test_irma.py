import json
import pytest

from eye_extractor.dr.irma import get_irma, IRMA_PAT
from eye_extractor.sections.document import create_doc_and_sections
from eye_extractor.sections.headers import Headers
from eye_extractor.output.dr import build_irma
from eye_extractor.sections.patterns import SectionName

# Test pattern.
_pattern_cases = [
    (IRMA_PAT, 'IRMA', True),
    (IRMA_PAT, 'intraretinal microvascular abnormality', True),
]


def _get_pattern_cases():
    return [(x[0], x[1], x[2]) for x in _pattern_cases]


@pytest.mark.parametrize('pat, text, exp', _get_pattern_cases())
def test_irma_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) == exp


# Test extract and build.
_irma_extract_and_build_cases = [
    ('OD: area of IRMA just nasal to disc', {}, 'YES NOS', 'UNKNOWN', 'UNKNOWN'),
    ('mild IRMA OU', {}, 'MILD', 'MILD', 'UNKNOWN'),
    ('Mild - moderate IRMA OD', {}, 'MODERATE', 'UNKNOWN', 'UNKNOWN'),
    ('no intraretinal microvascular abnormality ou', {}, 'NONE', 'NONE', 'UNKNOWN'),
    ('moderate IRMA OS', {}, 'UNKNOWN', 'MODERATE', 'UNKNOWN'),
    ('severe intraretinal microvascular abnormality', {}, 'UNKNOWN', 'UNKNOWN', 'SEVERE'),
    ('IRMA severity=3Q OS', {}, 'UNKNOWN', 'Q3', 'UNKNOWN'),
    ('IRMA temporal and inferior quadrant OD', {}, 'Q2', 'UNKNOWN', 'UNKNOWN'),
    ('nasal quadrant, IRMA', {}, 'UNKNOWN', 'UNKNOWN', 'Q1'),
    ('IRMA in all quadrants ou', {}, 'Q4', 'Q4', 'UNKNOWN'),
    ('has small area of IRMA right eye', {}, 'YES NOS', 'UNKNOWN', 'UNKNOWN'),
    ('(-)heme, MA, HE, CWS, VB, IRMA, NVE OU', {}, 'NONE', 'NONE', 'UNKNOWN'),
    ('¶Irma Smith CSN:', {}, 'UNKNOWN', 'UNKNOWN', 'UNKNOWN'),
    ('OU: No Microaneurysms/hemes, cotton-wool spots, exudates, IRMA',
     {}, 'NONE', 'NONE', 'UNKNOWN'),
    ('Vessels: good caliber, color, and crossings OU, no plaques or emboli OU (-) MAs, Venous Beading, IRMA, CWS',
     {}, 'NONE', 'NONE', 'UNKNOWN'),
    # Unless specified, all conditions in negated list are OU.
    # Since no laterality specified, laterality should be OU.
    ('no CWS, MA, IRMA', {}, 'NONE', 'NONE', 'UNKNOWN'),
    ('(-) MAs, Venous Beading, IRMA, CWS', {}, 'NONE', 'NONE', 'UNKNOWN'),
    ('Macula: flat, dry (-)heme, MA, HE, CWS, VB, IRMA, NVE OD, ERM OS', {}, 'NONE', 'NONE', 'UNKNOWN'),
    ('Macula: flat, dry (-)heme, MA, HE, CWS, VB, IRMA, NVE OD, ERM OS',
     {
         SectionName.MACULA: 'flat, dry (-)heme, MA, HE, CWS, VB, IRMA, NVE OD, ERM OS'
     },
     'NONE', 'NONE', 'UNKNOWN'),
    ('',
     {
         SectionName.MACULA: 'flat, dry (-)heme, MA, HE, CWS, VB, IRMA, NVE OD, ERM OS'
     },
     'NONE', 'NONE', 'UNKNOWN'),
]


@pytest.mark.parametrize('text, sections, exp_irma_re, exp_irma_le, exp_irma_unk',
                         _irma_extract_and_build_cases)
def test_irma_extract_and_build(text,
                                sections,
                                exp_irma_re,
                                exp_irma_le,
                                exp_irma_unk):
    doc = create_doc_and_sections(text, sections)
    pre_json = get_irma(doc)
    post_json = json.loads(json.dumps(pre_json))
    result = build_irma(post_json)
    assert result['irma_re'] == exp_irma_re
    assert result['irma_le'] == exp_irma_le
    assert result['irma_unk'] == exp_irma_unk
