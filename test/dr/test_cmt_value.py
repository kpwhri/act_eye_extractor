import json
import pytest

from eye_extractor.dr.cmt_value import (
    CMT_VALUE_OD_OS_UNK_PAT,
    CMT_VALUE_OD_SEP_OS_PAT,
    get_cmt_value,
)
from eye_extractor.output.dr import build_cmt_value
from eye_extractor.sections.document import create_doc_and_sections

# Test pattern.
_pattern_cases = [
    (CMT_VALUE_OD_OS_UNK_PAT, 'CMT 244', True),
    (CMT_VALUE_OD_OS_UNK_PAT, 'Central macular thickness: 234 um', True),
    (CMT_VALUE_OD_OS_UNK_PAT, 'CMT OD: 265', True),
    (CMT_VALUE_OD_OS_UNK_PAT, 'CMT OS 250', True),
    (CMT_VALUE_OD_OS_UNK_PAT, 'CMT OD:265 OS:224', True),
    (CMT_VALUE_OD_OS_UNK_PAT, 'OD CMT 123', True),
    (CMT_VALUE_OD_OS_UNK_PAT, 'OD: erm, CMT 291; OS: erm, CMT 280', True),
    (CMT_VALUE_OD_OS_UNK_PAT, 'Tonometry: TA OD:17 OS:17', False),
    (CMT_VALUE_OD_OS_UNK_PAT, 'NCT: OD:11 OS:19', False),
    (CMT_VALUE_OD_OS_UNK_PAT, 'Applanation Tonometry: 18 OD 12 OS', False),
    (CMT_VALUE_OD_OS_UNK_PAT, 'OD: +125-240*103\nOS: +050-090*065\n', False),
    (CMT_VALUE_OD_OS_UNK_PAT, 'TONOMETRY:\nTa OD: 14 OS: 18', False),
    (CMT_VALUE_OD_SEP_OS_PAT, 'CMT OD:300 possible epiretinal membrane OS:294', True),
]


def _get_pattern_cases():
    return [(x[0], x[1], x[2]) for x in _pattern_cases]


@pytest.mark.parametrize('pat, text, exp', _get_pattern_cases())
def test_cmt_value_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) == exp


# Test extract and build.
_cmt_value_extract_and_build_cases = [
    ('CMT OD: 219', {}, 219, -1, -1),
    ('CMT OD:265 OS:224', {}, 265, 224, -1),
    ('CMT 343', {}, -1, -1, 343),
    ('Central macular thickness: 234 um', {}, -1, -1, 234),
    ('CMT OD:300 possible epiretinal membrane OS:294', {}, 300, 294, -1),
    ('OD CMT 123', {}, 123, -1, -1),
    ('OD: erm, CMT 291; OS: erm, CMT 280', {}, 291, 280, -1),
    ('OD CMT 329; +ERM,  OS CMT 465; +ERM;', {}, 329, 465, -1),
    ('OS: REMAINS DRY CMT 244', {}, -1, 244, -1),
    ('OD: mild moderate irregularity, no edema, CMT 290; OS: moderate retinal irregularity , no edema, '
     'mild epiretinal membrane , CMT 282',
     {}, 290, 282, -1),
    ('CMT OS 250', {}, -1, 250, -1),
    ('OD CMT 252, irregular RPE layer OU\nOS:CMT 210', {}, 252, 210, -1),
    ('Acuities (cc) glare OD 20/30', {}, -1, -1, -1),
    ('OD 4/12', {}, -1, -1, -1),
    ('C/D: 0.6 OD 0.8 OS', {}, -1, -1, -1),
    ('OS 1988', {}, -1, -1, -1),
    ('OD: +0.40 -1.00 x 081 20/30 ¶OS: +1.60 -2.75 x 079 20/40+1', {}, -1, -1, -1),
    ('CC: OD: 20/20 PH: OD: 20/na', {}, -1, -1, -1),
    ('¶ ¶TONOMETRY: Tappl OD 14 mmHg OS 17 mmHg', {}, -1, -1, -1),
    ('¶ ¶Pachymetry: ¶OD: 544/541/540, OS: 534/537/531', {}, -1, -1, -1),
    ('no hyphema OD*7/8/2012', {}, -1, -1, -1),
    ('Intravitreal Avastin injection OD (67028', {}, -1, -1, -1),
    ('OD ¶1/2013:', {}, -1, -1, -1),
    ('¶2) Hem PVD OD ¶3)', {}, -1, -1, -1),
    ('OD12345678', {}, -1, -1, -1),
    ('Tonometry: TA OD:17 OS:17', {}, -1, -1, -1),
    ('NCT: OD:11 OS:19', {}, -1, -1, -1),
    ('Applanation Tonometry: 18 OD 12 OS', {}, -1, -1, -1),
    ('OD: +125-240*103\nOS: +050-090X065\n', {}, -1, -1, -1),
    ('TONOMETRY:\nTa OD: 14 OS: 18', {}, -1, -1, -1),
    ('os:-.45-1.25x60', {}, -1, -1, -1),
    ('IOP by applanation OD 10 OS 17\n', {}, -1, -1, -1),
    ('low OS @ 19,17. OD @ 20 mm last 4 exams', {}, -1, -1, -1),
    ('»»Average thickness: OD: 21» OS: 89', {}, -1, -1, -1),
    ('NCT: OD: 12 OS: 12', {}, -1, -1, -1),
]


@pytest.mark.parametrize('text, sections, exp_dmacedema_cmt_re, exp_dmacedema_cmt_le, exp_dmacedema_cmt_unk',
                         _cmt_value_extract_and_build_cases)
def test_cmt_value_extract_and_build(text,
                                     sections,
                                     exp_dmacedema_cmt_re,
                                     exp_dmacedema_cmt_le,
                                     exp_dmacedema_cmt_unk):
    doc = create_doc_and_sections(text, sections)
    pre_json = get_cmt_value(doc)
    post_json = json.loads(json.dumps(pre_json, default=str))
    result = build_cmt_value(post_json)
    assert result['dmacedema_cmt_re'] == exp_dmacedema_cmt_re
    assert result['dmacedema_cmt_le'] == exp_dmacedema_cmt_le
    assert result['dmacedema_cmt_unk'] == exp_dmacedema_cmt_unk
