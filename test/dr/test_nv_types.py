import json

import pytest

from eye_extractor.dr.nv_types import get_nv_types, NVA_PAT, NVI_HEADER_PAT
from eye_extractor.output.dr import build_neovasc, build_nva, build_nvd, build_nve, build_nvi


# Test pattern.
_pattern_cases = [
    (NVA_PAT, 'NVA: 0.30/0.43 M', False),
    (NVI_HEADER_PAT, 'IRIS RUBEOSIS:', True),
    (NVI_HEADER_PAT, 'iris rubeosis', False),
    (NVI_HEADER_PAT, 'IRIS RUBEOSIS', False),
    (NVI_HEADER_PAT, 'IRIS:', False),
    (NVI_HEADER_PAT, 'NVI with SLE: n', True),
    (NVI_HEADER_PAT, 'NVI with SLE:', True),
    (NVI_HEADER_PAT, 'NVI with SLE', False),

]


def _get_pattern_cases():
    return [(x[0], x[1], x[2]) for x in _pattern_cases]


@pytest.mark.parametrize('pat, text, exp', _get_pattern_cases())
def test_neovasc_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) == exp


_neovasc_extract_and_build_cases = [
    ('Corneal neovascularization, unspecified.', {}, -1, -1, 1),
    ('no NVD OD', {}, 0, -1, -1),
    ('Normal blood cells without NVD', {}, -1, -1, 0),
    ('without NVD, NVE', {}, -1, -1, 0),
    ('no NVE Disc 0.35', {}, -1, -1, 0),
    ('Best corrected acuities with above refraction:\nRE: 20/30 NVA: 0.24-M\nLE: 20/20- NVA: 0.40 M', {}, -1, -1, -1),
    ('Best corrected acuities with above refraction:\nRE: 20/30- NVA: 0.24 M\nLE: 20/20+ NVA: 0.40 M', {}, -1, -1, -1),
    ('Best corrected acuities with above refraction:\nRE: 20/30- NVA: RS21\nLE: 20/20 NVA: RS21', {}, -1, -1, -1),
    ('Best corrected acuities with above refraction:\nRE: 20/30- NVA: 0.30/0.43 M\nLE: 20/20- NVA: 0.30/0.43 M',
     {}, -1, -1, -1),
    ('Best corrected acuities with above refraction:\nRE: 20/30-1 NVA: 20/20-\nLE: 20/20-2', {}, -1, -1, -1),
    ('Best corrected acuities with above refraction:\nRE: 20/30+3 NVA: 20/20- OU\nLE: 20/20-', {}, -1, -1, -1),
    ('Her NVA has decreased since last exam.', {}, -1, -1, -1),
    ('last Rx does not work well intermediate and NV.', {}, -1, -1, -1),
    ('Eye Examination - wearing 2yr Pals DV driving fine, NV sxs', {}, -1, -1, -1),
    ('Pt reports NVA is decreased CC', {}, -1, -1, -1),
    ('PAST VISIONS:\n… 07/04/1492( NV):200 , 40 *', {}, -1, -1, -1),
    ('Visual acuity: Snellen\nCC: OD: 20/200 NV\nOS: 20/30 NV', {}, -1, -1, -1),
    ('ADD: +2.75 »»»NVA 20/45 OU', {}, -1, -1, -1),
    # TODO: Fix `LATERALITY_PATTERN` bug to pass below case.
    # ('Iris: flat and unremarkable, O.U. (-)TI defects, (-)NVI', {}, 0, 0, -1),  # 'O.U.' not captured
    ('CC/Reason for Visit: eye health check, change in nva', {}, -1, -1, -1),
    ('Patient presents with: is experiencing DV and NV decrease.', {}, -1, -1, -1),
    ('362.16W Choroidal neovascularization of left eye', {}, -1, 1, -1),
    ('Patient presents with: new rx dva decrease, nva good.', {}, -1, -1, -1),
    ('Best corrected acuities with above refraction:\nRE: 20/30- NVA: 0.24 M\nLE: 20/20 NVA: 0.40 M', {}, -1, -1, -1),
    ('Best corrected acuities with above refraction:\nRE: 20/30- NI PH NVA: 0.50 M\nLE: 20/20- NVA: 0.40 M',
     {}, -1, -1, -1),
    ('NVI: none', {}, -1, -1, 0),
    ('IRIS: Normal Appearance, neg Rubeosis, OD.', {}, 0, -1, -1),
    ('Best corrected acuities with above refraction:\nRE: 20/30 NVA: 0.24 M\nLE: 20/200 NVA: <1.75 M', {}, -1, -1, -1),
    ('Best corrected acuities with above refraction:\nRE: 20/30 NVA: 0.24 M\nLE: 20/20 NVA: 0.40 M', {}, -1, -1, -1),
    ('Best corrected acuities with above refraction:\nRE: 20/*** NVA: *** M\nLE: 20/*** NVA: *** M', {}, -1, -1, -1),
    ('PROBLEM "TRACKING" LINE TO LINE ON NVA.', {}, -1, -1, -1),
    ('Patient presents with:\nPt reports difficulty with NVA.', {}, -1, -1, -1),
    ('SNELLEN VISUAL ACUITY\nCC specs OD: 20/30-1 OS: 20/50-3\nSC OD: 20/ OS: 20/\nNVA', {}, -1, -1, -1),
    ('SNELLEN VISUAL ACUITY\nCC specs OD: 20/30-1 OS: 20/50-3\nSC OD: 20/ OS: 20/\n\nNVA', {}, -1, -1, -1),
    ('IRIS: Normal Appearance, neg Rubeosis, OU', {}, 0, 0, -1),
    ('Iris: flat, even (-)NVI/TIDs', {}, -1, -1, 0),
    ('Optic Nerve: Distinct margins, (-)NVD/edema/pallor', {}, -1, -1, 0),
    ('»(-)heme, MA, HE, CWS, VB, IRMA, NVE OU', {}, 0, 0, -1),
    ('CC/Reason for Visit: iop check, decrease in nva, smaller print pt uses a mgnifting glass', {}, -1, -1, -1),
    ('SNELLEN VISUAL ACUITY\nCC specs OD: 20/40-2 OS: 20/30-2\nph OD: 20/45-3 OS: 20/50-1\nNVA', {}, -1, -1, -1),
    ('Pt states that vision has decreased OU, notes things seem dimmer NVA and DVA.', {}, -1, -1, -1),
    ('Pt. states she has been having trouble with her NVA', {}, -1, -1, -1),
    ('Visual acuity: Snellen\nCC: OD: 20/30-1 PH: OD: 20/NI\nOS: 20/40 PH: OS: 20/NA\nNVA:\nOD: 20/50\nOS: 20/30',
     {}, -1, -1, -1),
    ('Pt c/o tearing OS>OD. Pt c/o decreased NVA OU', {}, -1, -1, -1),
    ('Patient presents with: OU blurry DVA and NVA,', {}, -1, -1, -1),
    ('NVA OU: 20/20', {}, -1, -1, -1),
    ('Probs with both dva and nva.', {}, -1, -1, -1),
    ('Best corrected acuities with above refraction:\nRE: 20/30-3+2 NVA: 0.40-M\nLE: 20/30-2 NVA: 0.40-',
     {}, -1, -1, -1),
    ('Pt states having trouble watching television, NVA seems to be fine and she is unsure if her DVA has decreased',
     {}, -1, -1, -1),
    ('Patient presents with: OS NVA DECREASE NOTICED RECENTLY AS SHE HAS BEEN READING MORE', {}, -1, -1, -1),
    ("Best corrected acuities with above refraction:\nRE: CF 2' NVA: < 3 M\nLE: CF 2' NVA: < 3 M", {}, -1, -1, -1),
    ('VAs with above correction\nOD: 20/30-\nOS: 20/30\nNVA: RS 21', {}, -1, -1, -1),
    ('Pt states he is not seeing as well with NVA.', {}, -1, -1, -1),
    ("SNELLEN VISUAL ACUITY\nCC OD: 20/ OS: 20/\nSC OD: 20/5' edges of hand OS: 20/150\n\nNVA", {}, -1, -1, -1),
    ('Patient presents with: Nva decrease/sm.print assoc.w/ occais.triangular h/a ongoing 6+mo.s.', {}, -1, -1, -1),
    ('CC: DecrNear VA\nNVA cc: 20/3 4+', {}, -1, -1, -1),
    ('Chief complaint:\nPt states that her NVA is getting worse.', {}, -1, -1, -1),
]


@pytest.mark.parametrize('text, headers, exp_neovasc_yesno_re, exp_neovasc_yesno_le, exp_neovasc_yesno_unk',
                         _neovasc_extract_and_build_cases)
def test_neovasc_extract_and_build(text,
                                   headers,
                                   exp_neovasc_yesno_re,
                                   exp_neovasc_yesno_le,
                                   exp_neovasc_yesno_unk):
    pre_json = get_nv_types(text)
    post_json = json.loads(json.dumps(pre_json))
    result = build_neovasc(post_json)
    assert result['neovasc_yesno_re'] == exp_neovasc_yesno_re
    assert result['neovasc_yesno_le'] == exp_neovasc_yesno_le
    assert result['neovasc_yesno_unk'] == exp_neovasc_yesno_unk


_nva_extract_and_build_cases = [
    # ('Gonioscopy: right eye: no NVA', {}, 0, -1, -1),
    ('RE: 20/40+ NVA: 0.60 M ¶LE: 20/30- NVA: 0.47 M', {}, -1, -1, -1),
    ('RE: 20/30 NVA: 0.47-M ¶LE: 20/20- NVA: 0.40 M', {}, -1, -1, -1),
    ('NVA: <1.75M', {}, -1, -1, -1),
    ('NVA 20/25 OU', {}, -1, -1, -1),
    ('OD: 20/25 NVA: 0.34 M ¶OS: 20/35 NVA: 0.34 M', {}, -1, -1, -1),
    ('RE: 20/30- NVA: 0.37- M LE: 20/30- NVA: 0.37- M', {}, -1, -1, -1),
    ('Her NVA has decreased since last exam.', {}, -1, -1, -1),
    ('Best corrected acuities with above refraction:\nRE: 20/30 NVA: 0.24-M\nLE: 20/20- NVA: 0.40 M', {}, -1, -1, -1),
    ('Best corrected acuities with above refraction:\nRE: 20/30- NVA: 0.24 M\nLE: 20/20+ NVA: 0.40 M', {}, -1, -1, -1),
    ('Best corrected acuities with above refraction:\nRE: 20/30- NVA: RS21\nLE: 20/20 NVA: RS21', {}, -1, -1, -1),
    ('Best corrected acuities with above refraction:\nRE: 20/30- NVA: 0.30/0.43 M\nLE: 20/20- NVA: 0.30/0.43 M',
     {}, -1, -1, -1),
    ('Best corrected acuities with above refraction:\nRE: 20/30-1 NVA: 20/20-\nLE: 20/20-2', {}, -1, -1, -1),
    ('Best corrected acuities with above refraction:\nRE: 20/30+3 NVA: 20/20- OU\nLE: 20/20-', {}, -1, -1, -1),
    ('Her NVA has decreased since last exam.', {}, -1, -1, -1),
    ('Pt reports NVA is decreased CC', {}, -1, -1, -1),
    ('ADD: +2.75 »»»NVA 20/45 OU', {}, -1, -1, -1),
    ('CC/Reason for Visit: eye health check, change in nva', {}, -1, -1, -1),
    ('Patient presents with: new rx dva decrease, nva good.', {}, -1, -1, -1),
    ('Best corrected acuities with above refraction:\nRE: 20/30- NVA: 0.24 M\nLE: 20/20 NVA: 0.40 M', {}, -1, -1, -1),
    ('Best corrected acuities with above refraction:\nRE: 20/30- NI PH NVA: 0.50 M\nLE: 20/20- NVA: 0.40 M',
     {}, -1, -1, -1),
    ('Best corrected acuities with above refraction:\nRE: 20/30 NVA: 0.24 M\nLE: 20/200 NVA: <1.75 M', {}, -1, -1, -1),
    ('Best corrected acuities with above refraction:\nRE: 20/30 NVA: 0.24 M\nLE: 20/20 NVA: 0.40 M', {}, -1, -1, -1),
    ('Best corrected acuities with above refraction:\nRE: 20/*** NVA: *** M\nLE: 20/*** NVA: *** M', {}, -1, -1, -1),
    ('PROBLEM "TRACKING" LINE TO LINE ON NVA.', {}, -1, -1, -1),
    ('Patient presents with:\nPt reports difficulty with NVA.', {}, -1, -1, -1),
    ('SNELLEN VISUAL ACUITY\nCC specs OD: 20/30-1 OS: 20/50-3\nSC OD: 20/ OS: 20/\nNVA', {}, -1, -1, -1),
    ('SNELLEN VISUAL ACUITY\nCC specs OD: 20/30-1 OS: 20/50-3\nSC OD: 20/ OS: 20/\n\nNVA', {}, -1, -1, -1),
    ('CC/Reason for Visit: iop check, decrease in nva, smaller print pt uses a mgnifting glass', {}, -1, -1, -1),
    ('SNELLEN VISUAL ACUITY\nCC specs OD: 20/40-2 OS: 20/30-2\nph OD: 20/45-3 OS: 20/50-1\nNVA', {}, -1, -1, -1),
    ('Pt states that vision has decreased OU, notes things seem dimmer NVA and DVA.', {}, -1, -1, -1),
    ('Pt. states she has been having trouble with her NVA', {}, -1, -1, -1),
    ('Visual acuity: Snellen\nCC: OD: 20/30-1 PH: OD: 20/NI\nOS: 20/40 PH: OS: 20/NA\n\nNVA:\nOD: 20/50\nOS: 20/30',
     {}, -1, -1, -1),
    ('Pt c/o tearing OS>OD. Pt c/o decreased NVA OU', {}, -1, -1, -1),
    ('Patient presents with: OU blurry DVA and NVA,', {}, -1, -1, -1),
    ('NVA OU: 20/20', {}, -1, -1, -1),
    ('Probs with both dva and nva.', {}, -1, -1, -1),
    ('Best corrected acuities with above refraction:\nRE: 20/30-3+2 NVA: 0.40-M\nLE: 20/30-2 NVA: 0.40-',
     {}, -1, -1, -1),
    ('Pt states having trouble watching television, NVA seems to be fine and she is unsure if her DVA has decreased',
     {}, -1, -1, -1),
    ('Patient presents with: OS NVA DECREASE NOTICED RECENTLY AS SHE HAS BEEN READING MORE', {}, -1, -1, -1),
    ("Best corrected acuities with above refraction:\nRE: CF 2' NVA: < 3 M\nLE: CF 2' NVA: < 3 M", {}, -1, -1, -1),
    ('VAs with above correction\nOD: 20/30-\nOS: 20/30\nNVA: RS 21', {}, -1, -1, -1),
    ('Pt states he is not seeing as well with NVA.', {}, -1, -1, -1),
    ("SNELLEN VISUAL ACUITY\nCC OD: 20/ OS: 20/\nSC OD: 20/5' edges of hand OS: 20/150\n\nNVA", {}, -1, -1, -1),
    ('Patient presents with: Nva decrease/sm.print assoc.w/ occais.triangular h/a ongoing 6+mo.s.', {}, -1, -1, -1),
    ('CC: DecrNear VA\nNVA cc: 20/3 4+', {}, -1, -1, -1),
    ('Chief complaint:\nPt states that her NVA is getting worse.', {}, -1, -1, -1),
    # Sections: gonioscopy, history of present illness, angle
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
    # TODO: Fix `LATERALITY_PATTERN` bug to pass below case.
    pytest.param('Iris: flat and unremarkable, O.U. (-)TI defects, (-)NVI', {}, 0, 0, -1, marks=pytest.mark.skip()),
    ('NVI: none', {}, -1, -1, 0),
    ('IRIS: Normal Appearance, neg Rubeosis, OD.', {}, 0, -1, -1),
    ('Iris: flat, even (-)NVI/TIDs', {}, -1, -1, 0),
    # new
    ('Iris/rubeosis - Not performed', {}, -1, -1, -1),
    ('IRIS RUBEOSIS: n/a', {}, -1, -1, -1),
    ('IRIS RUBEOSIS: none seen', {}, -1, -1, 0),
    # TODO: Fix laterality capture, `_get_by_index_default` to pass below case.
    pytest.param('Rubeosis: R eye: No L eye: No', {}, 0, 0, -1, marks=pytest.mark.skip()),
    # TODO: Extract NVI headers and replace with whitespace to pass below 4 cases.
    pytest.param('IRIS RUBEOSIS: ', {}, -1, -1, -1, marks=pytest.mark.skip()),
    pytest.param('', {'IRIS RUBEOSIS': ''}, -1, -1, -1, marks=pytest.mark.skip()),
    pytest.param('IRIS RUBEOSIS:\nPUPILLARY DILATION: No', {}, -1, -1, -1, marks=pytest.mark.skip()),
    pytest.param('', {'IRIS RUBEOSIS': '', 'PUPILLARY DILATION': 'No'}, -1, -1, -1, marks=pytest.mark.skip()),
    ('Iris/rubeosis - nt', {}, -1, -1, -1),
    ('IRIS: Normal Appearance, neg Rubeosis, OD. Coloboma OS', {}, 0, -1, -1),
    ('Will follow for rubeosis', {}, -1, -1, -1),
    # TODO: Fix laterality capture, `_get_by_index_default` to pass below case.
    pytest.param('IRIS RUBEOSIS: OD No OS NO', {}, 0, 0, -1, marks=pytest.mark.skip()),
    ('RUBEOSIS: n', {}, -1, -1, 0),
    # TODO: Extract NVI headers and replace with whitespace to pass below 4 cases.
    pytest.param('IRIS RUBEOSIS: abnormal Hazy view OD;normal OS', {}, -1, 0, -1, marks=pytest.mark.skip()),
    pytest.param('', {'IRIS RUBEOSIS': 'abnormal Hazy view OD;normal OS'}, -1, 0, -1, marks=pytest.mark.skip()),
    pytest.param('IRIS RUBEOSIS: abnormal Hazy view OD;normal OS\nTONOMETRY:Defer to Dr.Bowers', {}, -1, 0, -1,
                 marks=pytest.mark.skip()),
    pytest.param('', {'IRIS RUBEOSIS': 'abnormal Hazy view OD;normal OS\n',
          'TONOMETRY': 'Defer to Dr.Bowers'}, -1, 0, -1, marks=pytest.mark.skip()),
    ('IRIS RUBEOSIS: Not seen OU', {}, 0, 0, -1),
    ('IRIS RUBEOSIS: none', {}, -1, -1, 0),
    ('NVI with SLE: n', {}, -1, -1, 0),
    ('RUBEOSIS: None Seen', {}, -1, -1, 0),
    ('RUBEOSIS: None', {}, -1, -1, 0),
    ('IRIS RUBEOSIS: NT', {}, -1, -1, -1),
    # TODO: Extract NVI headers and replace with whitespace to pass below 4 cases.
    pytest.param('NVI with SLE:', {}, -1, -1, -1, marks=pytest.mark.skip()),
    pytest.param('', {'NVI with SLE': ''}, -1, -1, -1, marks=pytest.mark.skip()),
    pytest.param('NVI with SLE:\nTa:', {}, -1, -1, -1, marks=pytest.mark.skip()),
    pytest.param('', {'NVI with SLE': '\n', 'Ta': ''}, -1, -1, -1, marks=pytest.mark.skip()),
    ('NVI with SLE: none seen', {}, -1, -1, 0),
    ('Iris/rubeosis - WNL', {}, -1, -1, 0),
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
    ('Optic Nerve: Distinct margins, (-)NVD/edema/pallor', {}, -1, -1, 0),
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
