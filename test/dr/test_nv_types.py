import json

import pytest

from eye_extractor.dr.nv_types import get_nv_types
from eye_extractor.output.dr import build_nva, build_nvd, build_nve, build_nvi

_nva_extract_and_build_cases = [
    ('Gonioscopy: right eye: no NVA', {}, 0, -1, -1),
    ('RE: 20/40+ NVA: 0.60 M ¶LE: 20/30- NVA: 0.47 M', {}, -1, -1, -1),
    ('RE: 20/30 NVA: 0.47-M ¶LE: 20/20- NVA: 0.40 M', {}, -1, -1, -1),
    ('NVA: <1.75M', {}, -1, -1, -1),
    ('NVA 20/25 OU', {}, -1, -1, -1),
    ('OD: 20/25 NVA: 0.34 M ¶OS: 20/35 NVA: 0.34 M', {}, -1, -1, -1),
    ('RE: 20/30- NVA: 0.37- M LE: 20/30- NVA: 0.37- M', {}, -1, -1, -1),
]


@pytest.mark.parametrize('text, headers, exp_nva_yesno_re, exp_nva_yesno_le, exp_nva_yesno_unk',
                         _nva_extract_and_build_cases)
def test_nva_extract_and_build(text,
                               headers,
                               exp_nva_yesno_re,
                               exp_nva_yesno_le,
                               exp_nva_yesno_unk):
    pre_json = get_nv_types(text)
    post_json = json.loads(json.dumps(pre_json))
    result = build_nva(post_json)
    assert result['nva_yesno_re'] == exp_nva_yesno_re
    assert result['nva_yesno_le'] == exp_nva_yesno_le
    assert result['nva_yesno_unk'] == exp_nva_yesno_unk


_nvi_extract_and_build_cases = [
    ('IRIS - normal without rubeosis', {}, -1, -1, 0),
    ('IRIS RUBEOSIS: normal', {}, -1, -1, 0),
    ('IRIS: Normal Appearance, neg Rubeosis, OU', {}, 0, 0, -1),
    ('IRIS RUBEOSIS: neg', {}, -1, -1, 0),
    ('Iris Rubeosis - normal', {}, -1, -1, 0),
    ('IRIS RUBEOSIS: deferred', {}, -1, -1, 0),
    ('IRIS RUBEOSIS: no', {}, -1, -1, 0),
    # ('Iris: flat and unremarkable, O.U. (-)TI defects, (-)NVI', {}, 0, 0, -1),
]


@pytest.mark.parametrize('text, headers, exp_nvi_yesno_re, exp_nvi_yesno_le, exp_nvi_yesno_unk',
                         _nvi_extract_and_build_cases)
def test_nvi_extract_and_build(text,
                               headers,
                               exp_nvi_yesno_re,
                               exp_nvi_yesno_le,
                               exp_nvi_yesno_unk):
    pre_json = get_nv_types(text)
    post_json = json.loads(json.dumps(pre_json))
    result = build_nvi(post_json)
    assert result['nvi_yesno_re'] == exp_nvi_yesno_re
    assert result['nvi_yesno_le'] == exp_nvi_yesno_le
    assert result['nvi_yesno_unk'] == exp_nvi_yesno_unk


_nvd_extract_and_build_cases = [
    ('(-)NVD OU', {}, 0, 0, -1),
    ('no NVZD', {}, -1, -1, 0),
]


@pytest.mark.parametrize('text, headers, exp_nvd_yesno_re, exp_nvd_yesno_le, exp_nvd_yesno_unk',
                         _nvd_extract_and_build_cases)
def test_nvd_extract_and_build(text,
                               headers,
                               exp_nvd_yesno_re,
                               exp_nvd_yesno_le,
                               exp_nvd_yesno_unk):
    pre_json = get_nv_types(text)
    post_json = json.loads(json.dumps(pre_json))
    result = build_nvd(post_json)
    assert result['nvd_yesno_re'] == exp_nvd_yesno_re
    assert result['nvd_yesno_le'] == exp_nvd_yesno_le
    assert result['nvd_yesno_unk'] == exp_nvd_yesno_unk


_nve_extract_and_build_cases = [
    ('(-)heme, MA, HE, CWS, VB, IRMA, NVE OU', {}, 0, 0, -1),
    ('no NVZE', {}, -1, -1, 0),
]


@pytest.mark.parametrize('text, headers, exp_nve_yesno_re, exp_nve_yesno_le, exp_nve_yesno_unk',
                         _nve_extract_and_build_cases)
def test_nve_extract_and_build(text,
                               headers,
                               exp_nve_yesno_re,
                               exp_nve_yesno_le,
                               exp_nve_yesno_unk):
    pre_json = get_nv_types(text)
    post_json = json.loads(json.dumps(pre_json))
    result = build_nve(post_json)
    assert result['nve_yesno_re'] == exp_nve_yesno_re
    assert result['nve_yesno_le'] == exp_nve_yesno_le
    assert result['nve_yesno_unk'] == exp_nve_yesno_unk
