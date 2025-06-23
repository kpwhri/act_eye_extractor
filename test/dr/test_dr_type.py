import json
import pytest

from eye_extractor.dr.dr_type import (
    DrType,
    get_dr_type,
    get_pdr,
    NPDR_PAT,
    PDR_PAT,
)
from eye_extractor.output.dr import build_dr_type, build_npdr_severity, build_pdr_severity
from eye_extractor.sections.document import create_doc_and_sections

# Test pattern.
_dr_type_pattern_cases = [
    (NPDR_PAT, 'NPDR', True),
    (NPDR_PAT, 'non-proliferative diabetic retinopathy', True),
    (NPDR_PAT, 'Nonproliferative diabetic retinopathy', True),
    (NPDR_PAT, 'Non proliferative diabetic retinopathy', True),
    (NPDR_PAT, 'NONPROLIFERATIVE DIABETIC RETINOPATHY', True),
    (NPDR_PAT, 'BDR', True),
    (NPDR_PAT, 'bgdr', True),
    (NPDR_PAT, 'non-proliferative DR)', True),
    (PDR_PAT, 'PDR', True),
    (PDR_PAT, 'Proliferative Diabetic Retinopathy', True),
    (PDR_PAT, 'proliferative diabetic retinopathy', True),
    (PDR_PAT, 'PROLIFERATIVE DIABETIC RETINOPATHY', True),
]


def _get_pattern_cases(cases):
    return [(x[0], x[1], x[2]) for x in cases]


@pytest.mark.parametrize('pat, text, exp', _get_pattern_cases(_dr_type_pattern_cases))
def test_dr_type_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) == exp


# Test extract and build.
_dr_type_extract_and_build_cases = [
    ('Type II DM with mild - moderate NPDR ou', {}, DrType.NPDR, DrType.NPDR, DrType.UNKNOWN),
    ('DM w/out NPDR OU', {}, DrType.NONE, DrType.NONE, DrType.UNKNOWN),
    ('no NPDR', {}, DrType.UNKNOWN, DrType.UNKNOWN, DrType.NONE),
    ('MODERATE NONPROLIFERATIVE DIABETIC RETINOPATHY OD', {}, DrType.NPDR, DrType.UNKNOWN, DrType.UNKNOWN),
    ('proliferative Diabetic Retinopathy: YES, MILD OU', {}, DrType.PDR, DrType.PDR, DrType.UNKNOWN),
    ('Proliferative diabetic retinopathy OS', {}, DrType.UNKNOWN, DrType.PDR, DrType.UNKNOWN),
    ('Hx of pdr od', {}, DrType.NONE, DrType.UNKNOWN, DrType.UNKNOWN),  # historical
    ('Uncontrolled Proliferative Diabetic Retinopathy', {}, DrType.UNKNOWN, DrType.UNKNOWN, DrType.PDR),
    ('no BDR at that time. Review shows no apparent BDR OD and inconclusive OS', {},
     DrType.NONE, DrType.UNKNOWN, DrType.UNKNOWN),
    ('confirm no BDR', {}, DrType.UNKNOWN, DrType.UNKNOWN, DrType.NONE),
    ('no bgdr ou', {}, DrType.NONE, DrType.NONE, DrType.UNKNOWN),
    ('no bdr ou', {}, DrType.NONE, DrType.NONE, DrType.UNKNOWN),
    ('¶(1) No diabetic retinopathy.', {},
     DrType.UNKNOWN, DrType.UNKNOWN, DrType.NONE),
    ('NPDR : no ', {}, DrType.UNKNOWN, DrType.UNKNOWN, DrType.NONE),
    ('very severe NPDR ou', {}, DrType.NPDR, DrType.NPDR, DrType.UNKNOWN),
    ('DR os', {}, DrType.UNKNOWN, DrType.YES_NOS, DrType.UNKNOWN),  # synthetic
    ('diabetic retinopathy OU', {}, DrType.YES_NOS, DrType.YES_NOS, DrType.UNKNOWN),  # synthetic
    ("See DR. Bowers' April 19, 2023 exam", {}, DrType.UNKNOWN, DrType.UNKNOWN, DrType.UNKNOWN),
    ('recommended by Dr. Bowers', {}, DrType.UNKNOWN, DrType.UNKNOWN, DrType.UNKNOWN),
    ('w/Dr Bowers', {}, DrType.UNKNOWN, DrType.UNKNOWN, DrType.UNKNOWN),
    ('ASPIRIN TABLET DR 100MG PO', {}, DrType.UNKNOWN, DrType.UNKNOWN, DrType.UNKNOWN),
    # TODO: Resolve laterality issues to pass below tests.
    # ('nonproliferative diabetic retinopathy ¶ iols ou', {}, DrType.UNKNOWN, DrType.UNKNOWN, DrType.NPDR),
    # ('¶(1) No diabetic retinopathy. ¶(2) Increasing cataract, RE,', {}, DrType.UNKNOWN, DrType.UNKNOWN, DrType.NONE),
    # ('Background diabetic retinopathy ¶ ¶ ¶Plan.) start alphagan ou', {}, DrType.UNKNOWN, DrType.UNKNOWN, DrType.NPDR),
]


@pytest.mark.parametrize('text, sections, exp_diabretinop_type_re, exp_diabretinop_type_le, '
                         'exp_diabretinop_type_unk',
                         _dr_type_extract_and_build_cases)
def test_dr_type_extract_and_build(text,
                                   sections,
                                   exp_diabretinop_type_re,
                                   exp_diabretinop_type_le,
                                   exp_diabretinop_type_unk):
    doc = create_doc_and_sections(text, sections)
    pre_json = get_dr_type(doc)
    post_json = json.loads(json.dumps(pre_json))
    result = build_dr_type(post_json)
    assert result['diabretinop_type_re'] == exp_diabretinop_type_re
    assert result['diabretinop_type_le'] == exp_diabretinop_type_le
    assert result['diabretinop_type_unk'] == exp_diabretinop_type_unk


_npdr_severity_extract_and_build_cases = [
    ('mild BDR OU', {}, 'MILD', 'MILD', 'UNKNOWN'),
    ('Mild - moderate non-proliferative DR OD', {}, 'MODERATE', 'UNKNOWN', 'UNKNOWN'),
    ('no NPDR ou', {}, 'NONE', 'NONE', 'UNKNOWN'),
    ('moderate background diabetic retinopathy OS', {}, 'UNKNOWN', 'MODERATE', 'UNKNOWN'),
    ('severe NPDR', {}, 'UNKNOWN', 'UNKNOWN', 'SEVERE'),
    ('very severe NPDR ou', {}, 'VERY SEVERE', 'VERY SEVERE', 'UNKNOWN'),
    ('NPDR OS', {}, 'UNKNOWN', 'YES NOS', 'UNKNOWN'),
    ('PDR OU', {}, 'UNKNOWN', 'UNKNOWN', 'UNKNOWN'),
]


@pytest.mark.parametrize('text, sections, exp_nonprolifdr_re, exp_nonprolifdr_le, '
                         'exp_nonprolifdr_unk',
                         _npdr_severity_extract_and_build_cases)
def test_npdr_severity_extract_and_build(text,
                                         sections,
                                         exp_nonprolifdr_re,
                                         exp_nonprolifdr_le,
                                         exp_nonprolifdr_unk):
    doc = create_doc_and_sections(text, sections)
    pre_json = get_dr_type(doc)
    post_json = json.loads(json.dumps(pre_json))
    result = build_npdr_severity(post_json)
    assert result['nonprolifdr_re'] == exp_nonprolifdr_re
    assert result['nonprolifdr_le'] == exp_nonprolifdr_le
    assert result['nonprolifdr_unk'] == exp_nonprolifdr_unk


_pdr_severity_extract_and_build_cases = [
    ('PDR OU', {}, 'YES NOS', 'YES NOS', 'UNKNOWN'),
    ('Mild - moderate proliferative DR OD', {}, 'YES NOS', 'UNKNOWN', 'UNKNOWN'),
    ('no PDR ou', {}, 'NONE', 'NONE', 'UNKNOWN'),
    ('moderate proliferative diabetic retinopathy OS', {}, 'UNKNOWN', 'YES NOS', 'UNKNOWN'),
    ('proliferative DR', {}, 'UNKNOWN', 'UNKNOWN', 'YES NOS'),
    ('PRP OU for PDR', {}, 'YES NOS', 'YES NOS', 'UNKNOWN'),
    ('New PDR os', {}, 'UNKNOWN', 'YES NOS', 'UNKNOWN'),
    ('Stable proliferative diabetic retinopathy of both eyes', {}, 'YES NOS', 'YES NOS', 'UNKNOWN'),
    ('Proliferative diabetic retinopathy of right eye', {}, 'YES NOS', 'UNKNOWN', 'UNKNOWN'),
    ('Low risk proliferative diabetic retinopathy OU', {}, 'LOW RISK', 'LOW RISK', 'UNKNOWN'),  # Synthetic.
    ('High risk PDR OS', {}, 'UNKNOWN', 'HIGH RISK', 'UNKNOWN'),  # Synthetic.
]


@pytest.mark.parametrize('text, sections, exp_prolifdr_re, exp_prolifdr_le, '
                         'exp_prolifdr_unk',
                         _pdr_severity_extract_and_build_cases)
def test_pdr_severity_extract_and_build(text,
                                        sections,
                                        exp_prolifdr_re,
                                        exp_prolifdr_le,
                                        exp_prolifdr_unk):
    doc = create_doc_and_sections(text, sections)
    pre_json = get_pdr(doc)
    post_json = json.loads(json.dumps(pre_json))
    result = build_pdr_severity(post_json)
    assert result['prolifdr_re'] == exp_prolifdr_re
    assert result['prolifdr_le'] == exp_prolifdr_le
    assert result['prolifdr_unk'] == exp_prolifdr_unk
