import pytest

from eye_extractor.va.extractor2 import vacc_numbercorrect_le
from eye_extractor.va.rx import get_manifest_rx


@pytest.mark.parametrize('text, exp', [
    ('SNELLEN VISUAL ACUITY    CC   OD: 20/   OS: 20/  SC   OD: 20/40 OS:20/30+1  PH   OD: 20/40 OS:20/', -1),
])
def test_vacc_le(text, exp):
    assert vacc_numbercorrect_le(text) == exp


@pytest.mark.parametrize(
    'text, sphere_re, cylinder_re, axis_re, add_re, sphere_le, cylinder_le, axis_le, add_le',
    [
        ('''Manifest Refraction: OD: +1.50 -1.00 x 122 20/70 OS: +1.50 -0.25 x 042 20/40+2 Add: +4.25''',
         1.5, -1, 122, 0,
         1.5, -0.25, 42, 4.25),
    ])
def test_get_manifest_rx(text, sphere_re, cylinder_re, axis_re, add_re, sphere_le, cylinder_le, axis_le, add_le):
    res = get_manifest_rx(text)
    assert res['manifestrx_sphere_re'] == sphere_re
    assert res['manifestrx_cylinder_re'] == cylinder_re
    assert res['manifestrx_axis_re'] == axis_re
    assert res['manifestrx_add_re'] == add_re
    assert res['manifestrx_sphere_le'] == sphere_le
    assert res['manifestrx_cylinder_le'] == cylinder_le
    assert res['manifestrx_axis_le'] == axis_le
    assert res['manifestrx_add_le'] == add_le
