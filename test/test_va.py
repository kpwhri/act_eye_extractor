import json

import pytest

from eye_extractor.build_table import get_va
from eye_extractor.va.extractor2 import vacc_numbercorrect_le, extract_va
from eye_extractor.va.rx import get_manifest_rx, BCV_PAT


@pytest.mark.parametrize('text, exp', [
    ('SNELLEN VISUAL ACUITY    CC   OD: 20/   OS: 20/  SC   OD: 20/40 OS:20/30+1  PH   OD: 20/40 OS:20/', -1),
])
def test_vacc_le(text, exp):
    assert vacc_numbercorrect_le(text) == exp


@pytest.mark.parametrize(
    'text, sphere_re, cylinder_re, axis_re, add_re, denom_re, correct_re, '
    'sphere_le, cylinder_le, axis_le, add_le, denom_le, correct_le',
    [
        ('''Manifest Refraction: OD: +1.50 -1.00 x 122 20/70 OS: +1.50 -0.25 x 042 20/40+2 Add: +4.25''',
         1.5, -1, 122, 0, 70, 0,
         1.5, -0.25, 42, 4.25, 40, 2),
        ('''REFRACTION : Manifest OD: +0.75-2.50x105 20/25-2 OS: +1.00-2.50x075 20/30-2 Add:+2.50''',
         0.75, -2.5, 105, 0, 25, -2,
         1, -2.5, 75, 2.5, 30, -2),
        ('''REFRACTION : Manifest:  OD: -1.75-1.25x068  Reading: OD:+0.75-1.25x068 OS: -1.50-1.00x080   
          OS:+1.00-1.00x080 ADD: SV ''',
         -1.75, -1.25, 68, 0, 0, 0,
         -1.5, -1, 80, 0, 0, 0),
        (''' REFRACTION
             Manifest Refraction:
             OD +3.50-1.00x097 add: +2.50 BVA 20/20-2
             OS +2.75-0.75x092 add: +2.50 BVA 20/25-3
          ''',
         3.5, -1, 97, 2.5, 20, -2,
         2.75, -0.75, 92, 2.5, 25, -3),
        (''' Manifest Refraction today: RE: +200 -550 x 089 LE: +200 -650 x 083 add power: + 275 ''',  # FIX
         3.5, -1, 97, 2.5, 20, -2,
         2.75, -0.75, 92, 2.5, 25, -3),
    ])
def test_get_manifest_rx(
        text, sphere_re, cylinder_re, axis_re, add_re, denom_re, correct_re,
        sphere_le, cylinder_le, axis_le, add_le, denom_le, correct_le):
    res = get_manifest_rx(text)
    if not res:
        raise ValueError('Pattern not found.')
    assert res['manifestrx_sphere_re'] == sphere_re
    assert res['manifestrx_cylinder_re'] == cylinder_re
    assert res['manifestrx_axis_re'] == axis_re
    assert res['manifestrx_add_re'] == add_re
    assert res['manifestrx_denom_re'] == denom_re
    assert res['manifestrx_ncorr_re'] == correct_re
    assert res['manifestrx_sphere_le'] == sphere_le
    assert res['manifestrx_cylinder_le'] == cylinder_le
    assert res['manifestrx_axis_le'] == axis_le
    assert res['manifestrx_add_le'] == add_le
    assert res['manifestrx_denom_le'] == denom_le
    assert res['manifestrx_ncorr_le'] == correct_le


def test_bcv_pat():
    text = 'Best Correct Vision: OD: 20/25-2 OS: 20/40'
    m = BCV_PAT.search(text)
    assert m is not None
    assert m.group('od_denominator') == '25'
    assert m.group('od_correct') == '-2'
    assert m.group('os_denominator') == '40'
    assert m.group('os_correct') is None


def test_va_ni():
    text = r'VISUAL ACUITY:    Snellen CC:   OD: 20/40   PH: OD: 20/NI   OS: 20/20   PH: OS: 20/'
    result = list(extract_va(text))
    assert len(result) == 4
    post_json = json.loads(json.dumps(result))
    assert len(post_json) == 4
    va_dict = get_va(post_json)
    assert 40 == va_dict.get('vacc_denominator_re', None) == va_dict.get('vaph_denominator_re', None)
    assert 0 == va_dict.get('vacc_numbercorrect_re', None) == va_dict.get('vaph_numbercorrect_re', None)
