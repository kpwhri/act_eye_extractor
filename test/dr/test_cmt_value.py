import json
import pytest

from eye_extractor.dr.cmt_value import CMT_VALUE_PAT, get_cmt_value
from eye_extractor.output.dr import build_cmt_value

# Test pattern.
_pattern_cases = [
    (CMT_VALUE_PAT, 'CMT 244', True),
    (CMT_VALUE_PAT, 'Central macular thickness: 234 um', True),
    (CMT_VALUE_PAT, 'CMT OD: 265', True),
    (CMT_VALUE_PAT, 'OS:300', True),
]


def _get_pattern_cases():
    return [(x[0], x[1], x[2]) for x in _pattern_cases]


@pytest.mark.parametrize('pat, text, exp', _get_pattern_cases())
def test_cmt_value_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) == exp


# Test extract and build.
_cmt_value_extract_and_build_cases = [
    ('OD: erm, CMT 291; OS: erm, CMT 280', {}, 291, 280, -1),
    ('OD CMT 329; +ERM,  OS CMT 465; +ERM;', {}, 329, 465, -1),
    ('CMT OD: 219', {}, 219, -1, -1),
    ('CMT OD:265 OS:224', {}, 265, 224, -1),
    ('OS: REMAINS DRY CMT 244', {}, -1, 244, -1),
    ('CMT OD:300 possible epiretinal membrane OS:294 mild epiretinal membrane',
     {}, 300, 294, -1),
    ('OD: mild moderate irregularity, no edema, CMT 290; OS: moderate retinal irregularity , no edema, '
     'mild epiretinal membrane , CMT 282',
     {}, 290, 282, -1),
    ('Central macular thickness: 234 um', {}, -1, -1, 234),
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
]


@pytest.mark.parametrize('text, headers, exp_dmacedema_cmt_re, exp_dmacedema_cmt_le, exp_dmacedema_cmt_unk',
                         _cmt_value_extract_and_build_cases)
def test_cmt_value_extract_and_build(text,
                                     headers,
                                     exp_dmacedema_cmt_re,
                                     exp_dmacedema_cmt_le,
                                     exp_dmacedema_cmt_unk):
    pre_json = get_cmt_value(text)
    post_json = json.loads(json.dumps(pre_json))
    result = build_cmt_value(post_json)
    assert result['dmacedema_cmt_re'] == exp_dmacedema_cmt_re
    assert result['dmacedema_cmt_le'] == exp_dmacedema_cmt_le
    assert result['dmacedema_cmt_unk'] == exp_dmacedema_cmt_unk
