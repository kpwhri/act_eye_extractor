import json
import pytest

from eye_extractor.common.get_variable import get_variable
from eye_extractor.dr.dme_yesno import DME_YESNO_PAT, get_dme_yesno
from eye_extractor.headers import Headers
from eye_extractor.output.dr import build_dme_yesno

# Test pattern.
_pattern_cases = [
    (DME_YESNO_PAT, 'DME', True),
    (DME_YESNO_PAT, 'diabetic macular edema', True),
    (DME_YESNO_PAT, 'csme', True),
    (DME_YESNO_PAT, 'diabetic retinopathy of right eye with macular edema', True),
    (DME_YESNO_PAT, 'diabetic retinopathy of left eye with macular edema', True),
]


def _get_pattern_cases():
    return [(x[0], x[1], x[2]) for x in _pattern_cases]


@pytest.mark.parametrize('pat, text, exp', _get_pattern_cases())
def test_dme_yesno_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) == exp


# Test extract and build.
_dme_yesno_extract_and_build_cases = [
    ('Patient presents with: Diabetic macular edema E11.311', {}, -1, -1, 1),
    ('OS: CMT 163, druse, RPE atrophy, no DME', {}, -1, 0, -1),
    ('evaluation of recurrent DME OD', {}, 1, -1, -1),
    ('received periodic Avastin OD for DME.', {}, 1, -1, -1),
    ('', {'ASSESSMENT': '(E11.3211) Mild nonproliferative diabetic retinopathy of right eye with macular edema'},
     1, -1, -1),
    ('Hx; Avastin OD for DME', {}, 0, -1, -1),
    ('• Mild nonproliferative diabetic retinopathy of right eye with macular edema', {}, 1, -1, -1),
    ('Next, this week. s/p persistant R DME.', {}, 1, -1, -1),
    # '-persistant' -> 'no persistant' in '_handle_negation_with_punctuation'
    # Can't fix, -[noun] is meant as negation elsewhere.
    pytest.param('A:-persistant DME OD', {}, 1, -1, -1, marks=pytest.mark.skip(reason="'-' interpreted as negator")),
    ('CMT 256 with tr drusen & steepened contour OS. No DME OU', {}, 0, 0, -1),
    ('ASSESSMENT: hx of dme', {}, -1, -1, 0),
    ('', {'ASSESSMENT': 'hx of dme'}, -1, -1, 0),
    ('(E11.9) Diabetes mellitus type 2 without retinopathy - hx of DME OS', {}, -1, 0, -1),
    ('OD: CMT 203; no DME\nOS: CMT 324: no DME', {}, 0, 0, -1),
    ('OD: no DME\nOS: no DME, ERM', {}, 0, 0, -1),
    ('»Comment: no DME seen today,', {}, -1, -1, 0),
    ('MACULA: no csme od; 1+edema temporal macula OS with exudates', {}, 0, -1, -1),
    ('', {'MACULA': 'no csme od; 1+edema temporal macula OS with exudates'}, 0, -1, -1),
    # ('defer CE given risk of exacerbating DME', {}, -1, -1, -1),
    ('maculas without DME OU', {}, 0, 0, -1),
    ('MACULA: without DME OU', {}, 0, 0, -1),
    ('', {'MACULA': 'without DME OU'}, 0, 0, -1),
    ('Macula: no DME noted', {}, -1, -1, 0),
    ('', {'Macula': 'no DME noted'}, -1, -1, 0),
    ('Macula:\nOD: clear, no significant edema, hg or RPE changes, (-)DME\n'
     'OS: clear, no significant edema, hg or RPE changes, (-)DME', {}, 0, 0, -1),
    ('', {'Macula': 'OD: clear, no significant edema, hg or RPE changes, (-)DME\n'
     'OS: clear, no significant edema, hg or RPE changes, (-)DME'}, 0, 0, -1),
    ('PLAN: findings reviewed; likely cnvm although cannot r/o DME or small BRVO.', {}, -1, -1, -1),
    ('', {'PLAN': 'findings reviewed; likely cnvm although cannot r/o DME or small BRVO.'}, -1, -1, -1),
    ('Hx of DME OU', {}, 0, 0, -1),
    ('', {'SUBJECTIVE': 'The patient notes vision is stable. Hx of DME OU.'}, 0, 0, -1),
    ('Diabetic macular edema', {}, -1, -1, 1),
    ('Diabetic macular edema OS', {}, -1, 1, -1),
    ('1. DM with Hx DME OU', {}, 0, 0, -1),
    ('»H/o NPDR with DME OU', {}, 0, 0, -1),
    ('Indication: DME', {}, -1, -1, -1),
    ('2.DM2 with h/o NPDR & DME OU', {}, 0, 0, -1),
    ('Possible early DME OS', {}, -1, -1, -1),
    ('MACULA: blot heme superior arcade OD, no CSME OU.', {}, 0, 0, -1),
    ('', {'MACULA': 'blot heme superior arcade OD, no CSME OU.'}, 0, 0, -1),
    # TODO: Resolve laterality issues to pass below tests.
    # ('Stromal edema OD causing mild blurring of vision. No diabetic macular edema.', {}, -1, -1, 0),
    # ('Yes- Diabetes: Hx BDR, Hx DME - right eye: sp PRP OD', {}, 0, -1, -1),  # not discovering `next_lat`
    # `_get_by_index_default` doesn't detect three intervening commas.
    # ('Macula: no DME, but minimal, dry RPE changes, LE; no gray membranes;', {}, -1, -1, 0),
]


@pytest.mark.parametrize('text, headers, '
                         'exp_dmacedema_yesno_re, exp_dmacedema_yesno_le, exp_dmacedema_yesno_unk',
                         _dme_yesno_extract_and_build_cases)
def test_dme_yesno_extract_and_build(text,
                                     headers,
                                     exp_dmacedema_yesno_re,
                                     exp_dmacedema_yesno_le,
                                     exp_dmacedema_yesno_unk):
    pre_json = get_dme_yesno(text, headers=Headers(headers))
    post_json = json.loads(json.dumps(pre_json, default=str))
    result = build_dme_yesno(post_json)
    assert result['dmacedema_yesno_re'] == exp_dmacedema_yesno_re
    assert result['dmacedema_yesno_le'] == exp_dmacedema_yesno_le
    assert result['dmacedema_yesno_unk'] == exp_dmacedema_yesno_unk
