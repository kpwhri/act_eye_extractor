import json
import pytest

from eye_extractor.dr.dr_yesno import DR_YESNO_PAT, DR_YESNO_ABBR_PAT, get_dr_yesno
from eye_extractor.headers import Headers
from eye_extractor.output.dr import build_dr_yesno

# Test pattern.
_pattern_cases = [
    (DR_YESNO_PAT, 'diabetic retinopathy', True),
    (DR_YESNO_PAT, 'Diabetic retinopathy', True),
    (DR_YESNO_PAT, 'DIABETIC RETINOPATHY', True),
    (DR_YESNO_ABBR_PAT, 'DR', True),
    (DR_YESNO_ABBR_PAT, 'dr', True),
    (DR_YESNO_ABBR_PAT, 'BDR', True),
    (DR_YESNO_ABBR_PAT, 'bdr', True),
    (DR_YESNO_ABBR_PAT, 'BGDR', True),
    (DR_YESNO_ABBR_PAT, 'bgdr', True),
    (DR_YESNO_ABBR_PAT, 'NPDR', True),
    (DR_YESNO_ABBR_PAT, 'npdr', True),
    (DR_YESNO_ABBR_PAT, 'PDR', True),
    (DR_YESNO_ABBR_PAT, 'pdr', True),
    (DR_YESNO_ABBR_PAT, 'Dr', False),
    (DR_YESNO_ABBR_PAT, 'Dr.', False),
]


def _get_pattern_cases():
    return [(x[0], x[1], x[2]) for x in _pattern_cases]


@pytest.mark.parametrize('pat, text, exp', _get_pattern_cases())
def test_dr_yesno_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) == exp


# Test extract and build.
_dr_yesno_extract_and_build_cases = [
    ('No visible diabetic retinopathy this visit', {}, -1, -1, 0),
    ('Mild nonproliferative diabetic retinopathy OU', {}, 1, 1, -1),
    ('DR os', {}, -1, 1, -1),
    ('no dr od', {}, 0, -1, -1),
    ('NPDR ou', {}, 1, 1, -1),
    ('w/out NPDR OU', {}, 0, 0, -1),
    ('no NPDR', {}, -1, -1, 0),
    ('NONPROLIFERATIVE DIABETIC RETINOPATHY OD', {}, 1, -1, -1),
    ('proliferative Diabetic Retinopathy: YES, MILD OU', {}, 1, 1, -1),
    ('Proliferative diabetic retinopathy OS', {}, -1, 1, -1),
    ('hx of pdr od', {}, 0, -1, -1),  # historical
    ('Uncontrolled Proliferative Diabetic Retinopathy', {}, -1, -1, 1),
    ('no BDR at that time. Review shows no apparent BDR OD and inconclusive OS', {}, 0, -1, -1),
    ('confirm no BDR', {}, -1, -1, -1),
    ('no bgdr ou', {}, 0, 0, -1),
    ('no bdr ou', {}, 0, 0, -1),
    ('¶(1) No diabetic retinopathy.', {}, -1, -1, 0),
    ('NPDR : no', {}, -1, -1, 0),
    ("See DR. Bowers' April 19, 2023 exam", {}, -1, -1, -1),
    ("See DR. Cronkite's April 19, 2023 exam", {}, -1, -1, -1),
    ('recommended by Dr. Bowers', {}, -1, -1, -1),
    ('Primary Eye Care Provider: Dr, Bowers', {}, -1, -1, -1),
    ('Surgeon: dr. Bowers', {}, -1, -1, -1),
    ('ASPIRIN TABLET DR 100MG PO', {}, -1, -1, -1),
    ('I, Dr.Bowers have reviewed the documentation', {}, -1, -1, -1),
    ('eye exam w/Dr. Bowers', {}, -1, -1, -1),
    ('w/Dr Bowers', {}, -1, -1, -1),
    ('Chief complaint:Referral Dr.Bowers/Cataracts', {}, -1, -1, -1),
    ('TONOMETRY:Defer to Dr.Bowers', {}, -1, -1, -1),
    ('Please provide Dr Bowers with', {}, -1, -1, -1),
    ('S/P CE IOL OD 04/19/2023 Dr.Bowers', {}, -1, -1, -1),
    ('Dr. Bowers will interpret results.', {}, -1, -1, -1),
    ('Hx of ce with iol os by Dr. Bowers', {}, -1, -1, -1),
    ('is here for an annual eye exam per dr.Bowers, OPH MD', {}, -1, -1, -1),
    ('REFERRED BY: DR. BOWERS for pco os and cataract od.', {}, -1, -1, -1),
]


@pytest.mark.parametrize('text, headers, '
                         'exp_diab_retinop_yesno_re, exp_diab_retinop_yesno_le, exp_diab_retinop_yesno_unk',
                         _dr_yesno_extract_and_build_cases)
def test_dr_yesno_extract_and_build(text,
                                    headers,
                                    exp_diab_retinop_yesno_re,
                                    exp_diab_retinop_yesno_le,
                                    exp_diab_retinop_yesno_unk):
    pre_json = get_dr_yesno(text, headers=Headers(headers))
    post_json = json.loads(json.dumps(pre_json))
    result = build_dr_yesno(post_json)
    assert result['diab_retinop_yesno_re'] == exp_diab_retinop_yesno_re
    assert result['diab_retinop_yesno_le'] == exp_diab_retinop_yesno_le
    assert result['diab_retinop_yesno_unk'] == exp_diab_retinop_yesno_unk
