import json

import pytest

from eye_extractor.dr.ret_micro import get_ret_micro, RET_MICRO_PAT
from eye_extractor.headers import Headers
from eye_extractor.output.dr import build_ret_micro


# Test pattern.
_pattern_cases = [
    (RET_MICRO_PAT, 'ma', False),
    (RET_MICRO_PAT, 'retinal ma', True),
    (RET_MICRO_PAT, 'retinal microaneurysm', True),
    (RET_MICRO_PAT, 'scattered MAs', True),
    (RET_MICRO_PAT, '+single MA', True),
    (RET_MICRO_PAT, '+single TR MA', True),
]


def _get_pattern_cases():
    return [(x[0], x[1], x[2]) for x in _pattern_cases]


@pytest.mark.parametrize('pat, text, exp', _get_pattern_cases())
def test_ret_micro_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) == exp


# Test extract and build.
_ret_micro_extract_and_build_cases = [
    ('retinal microaneurysm ou', {}, 'YES NOS', 'YES NOS', 'UNKNOWN'),  # synthetic
    ('Pupillary Dilation: by MA above', {}, 'UNKNOWN', 'UNKNOWN', 'UNKNOWN'),
    ('>> Will Bowers, MA', {}, 'UNKNOWN', 'UNKNOWN', 'UNKNOWN'),
    ('Will Ma, Ophthalmic Tech', {}, 'UNKNOWN', 'UNKNOWN', 'UNKNOWN'),
    ('Signed by: Will Bowers, MA', {}, 'UNKNOWN', 'UNKNOWN', 'UNKNOWN'),
    ('Signed by: William Ian Bowers, MA', {}, 'UNKNOWN', 'UNKNOWN', 'UNKNOWN'),
    ('MA HCC 59: MAJOR DEPRESSIVE, BIPOLAR, AND PARANOID DISORDERS-', {}, 'UNKNOWN', 'UNKNOWN', 'UNKNOWN'),
    ('MA HCC 52: DEMENTIA WITHOUT COMPLICATION-', {}, 'UNKNOWN', 'UNKNOWN', 'UNKNOWN'),
    ('\n>> Will Bowers, MA\n', {}, 'UNKNOWN', 'UNKNOWN', 'UNKNOWN'),
    ('MA: OD normal 6/6 , OS normal 6/6', {}, 'UNKNOWN', 'UNKNOWN', 'UNKNOWN'),
    ('HRT II linear C/D 0.37 / 0.37 on 4/20/1492»MA: OD normal 6/6 , OS normal 6/6',
     {}, 'UNKNOWN', 'UNKNOWN', 'UNKNOWN'),
    ('Pupillary Dilation: yes, by MA', {}, 'UNKNOWN', 'UNKNOWN', 'UNKNOWN'),
    ('CC: as per MA notes;', {}, 'UNKNOWN', 'UNKNOWN', 'UNKNOWN'),
    ('Tonometry: as per MA', {}, 'UNKNOWN', 'UNKNOWN', 'UNKNOWN'),
    ('moderate retinal micro-aneurysm os', {}, 'UNKNOWN', 'MODERATE', 'UNKNOWN'),  # synthetic
    ('VERY SEVERE RETINAL MAS', {}, 'UNKNOWN', 'UNKNOWN', 'VERY SEVERE'),  # synthetic
    ('362.14 Retinal microaneurysm of left eye', {}, 'UNKNOWN', 'YES NOS', 'UNKNOWN'),
    ('Retinal microaneurysm of left eye', {}, 'UNKNOWN', 'YES NOS', 'UNKNOWN'),
    ('Retinal microaneurysms, both eyes', {}, 'YES NOS', 'YES NOS', 'UNKNOWN'),
    ('retinal microaneurysms both eyes', {}, 'YES NOS', 'YES NOS', 'UNKNOWN'),
    ("scattered MA's in macula both eyes.", {}, 'YES NOS', 'YES NOS', 'UNKNOWN'),
    ("RPE changes both eyes, CME left eye, scattered MA's in macula both eyes.", {}, 'YES NOS', 'YES NOS', 'UNKNOWN'),
    ('Retinal micro-aneurysm of both eyes', {}, 'YES NOS', 'YES NOS', 'UNKNOWN'),
    ('362.14G Retinal microaneurysm of both eyes', {}, 'YES NOS', 'YES NOS', 'UNKNOWN'),
    ('MACULA: +moderate flat confluent drusen temp to macula OU without edema, '
     'exudates+single MA on the edge of drusen and fovea in OD and OS', {}, 'YES NOS', 'YES NOS', 'UNKNOWN'),
    ('+single MA on the edge of drusen and fovea in OD and OS', {}, 'YES NOS', 'YES NOS', 'UNKNOWN'),
    ('MACULA: +moderate flat confluent drusen temp to macula OU without edema, '
     'exudates+single TR MA inf nasal off macula in OD, +TR MA nasal to macula', {}, 'YES NOS', 'UNKNOWN', 'UNKNOWN'),
    ('+single TR MA inf nasal off macula in OD', {}, 'YES NOS', 'UNKNOWN', 'UNKNOWN'),
    ("multiple retinal MA's R>L", {}, 'YES NOS', 'YES NOS', 'UNKNOWN'),
    ("multiple retinal MA's R>L\n\n-mild blepharitis, dry eye sx (no spk)", {}, 'YES NOS', 'YES NOS', 'UNKNOWN'),
    ('3. (H35.043) Retinal microaneurysm, bilateral', {}, 'YES NOS', 'YES NOS', 'UNKNOWN'),
    ('Retinal microaneurysm of right eye', {}, 'YES NOS', 'UNKNOWN', 'UNKNOWN'),
    ('Retinal microaneurysms, right', {}, 'YES NOS', 'UNKNOWN', 'UNKNOWN'),
    ('MACULA:  microaneurysms Od; within normal limits os  without edema, exudates, or hemorrhage, OU ',
     {}, 'YES NOS', 'UNKNOWN', 'UNKNOWN'),
    ('MACULA:  microaneurysms Od;', {}, 'YES NOS', 'UNKNOWN', 'UNKNOWN'),
    ('OCT   Microaneurysms superior macula od without fluid;  within normal limits os',
     {}, 'YES NOS', 'UNKNOWN', 'UNKNOWN'),
    ('Microaneurysms superior macula od without fluid', {}, 'YES NOS', 'UNKNOWN', 'UNKNOWN'),
    ('Microaneurysms superior macula od', {}, 'YES NOS', 'UNKNOWN', 'UNKNOWN'),
]


@pytest.mark.parametrize('text, headers,'
                         'exp_ret_micro_re, exp_ret_micro_le, exp_ret_micro_unk',
                         _ret_micro_extract_and_build_cases)
def test_ret_micro_extract_and_build(text,
                                     headers,
                                     exp_ret_micro_re,
                                     exp_ret_micro_le,
                                     exp_ret_micro_unk):
    pre_json = get_ret_micro(text, headers=Headers(headers))
    post_json = json.loads(json.dumps(pre_json, default=str))
    result = build_ret_micro(post_json)
    assert result['ret_microaneurysm_re'] == exp_ret_micro_re
    assert result['ret_microaneurysm_le'] == exp_ret_micro_le
    assert result['ret_microaneurysm_unk'] == exp_ret_micro_unk

