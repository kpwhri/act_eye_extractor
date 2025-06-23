import json
import pytest

from eye_extractor.dr.cws import CWS_PAT, get_cottonwspot
from eye_extractor.sections.document import create_doc_and_sections
from eye_extractor.output.dr import build_cottonwspot
from eye_extractor.sections.patterns import SectionName

# Test pattern.
_pattern_cases = [
    (CWS_PAT, 'CWS', True),
    (CWS_PAT, 'cotton-wool spots', True),
    (CWS_PAT, 'soft exudate', True),
]


def _get_pattern_cases():
    return [(x[0], x[1], x[2]) for x in _pattern_cases]


@pytest.mark.parametrize('pat, text, exp', _get_pattern_cases())
def test_cws_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) == exp


# Test extract and build.
_cws_extract_and_build_cases = [
    ('No d/b hemes, CWS or NVE OU', {}, 0, 0, -1),
    ('there is an isolated CWS in the superior temp. arcade of the RE.', {}, 1, -1, -1),
    ('Peripheral fundus: breaks R/L with BIO view; BUT, there is an isolated CWS in the superior temp. arcade of the '
     'RE.', {}, 1, -1, -1),
    ('PERIPHERAL RETINA: flat; no holes or breaks, R/L, with BIO view; no NVZE noted; isolated CWS, LE', {}, -1, 1, -1),
    ('MACULA: clr OU\nno hem, no exud, no CWS OU', {}, 0, 0, -1),
    ('MACULA: clr OU\nno hem, no exud, no\nCWS OU', {}, 0, 0, -1),
    ('', {SectionName.MACULA: 'clr OU\nno hem, no exud, no CWS OU'}, 0, 0, -1),
    ('MACULA: RT: there was one soft exudate superior to the macula, LT: normal appearance.', {}, 1, -1, -1),
    ('VESSELS: Soft exudates Inf arcade OS', {}, -1, 1, -1),
    ('PERIPHERAL RETINA: […] there is a small, quarter disc diameter area of what looks like 3 small soft exudates',
     {}, -1, -1, 1),
    # Unless specified, all conditions in negated list are OU.
    # Laterality specified.
    ('Vessels: (-) MAs, Venous Beading, IRMA, CWS OU', {}, 0, 0, -1),
    # Since no laterality specified, laterality should be OU.
    ('No Microaneurysms/hemes, cotton-wool spots, exudates, IRMA, Venous beading, NVE',
     {}, 0, 0, -1),
    ('Vessels: (-) MAs, Venous Beading, IRMA, CWS', {}, 0, 0, -1),
    ('Periphery: RE trace BDR; LE with extensive PRP, but no NVZE/hg/CWS/HE noted today\n', {}, 0, 0, -1),
    # 'or' counts as separator in two item negated list, laterality should be OU.
    ('Vessels: scattered MA/dot hgs, but no CWS or HE;', {}, 0, 0, -1),
]


@pytest.mark.parametrize('text, sections, exp_cottonwspot_re, exp_cottonwspot_le, exp_cottonwspot_unk',
                         _cws_extract_and_build_cases)
def test_cws_extract_and_build(text,
                               sections,
                               exp_cottonwspot_re,
                               exp_cottonwspot_le,
                               exp_cottonwspot_unk):
    doc = create_doc_and_sections(text, sections)
    pre_json = get_cottonwspot(doc)
    post_json = json.loads(json.dumps(pre_json))
    result = build_cottonwspot(post_json)
    assert result['cottonwspot_re'] == exp_cottonwspot_re
    assert result['cottonwspot_le'] == exp_cottonwspot_le
    assert result['cottonwspot_unk'] == exp_cottonwspot_unk
