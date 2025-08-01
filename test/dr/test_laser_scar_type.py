import json
import pytest

from eye_extractor.dr import laser_scar_type as lst
from eye_extractor.output.dr import (
    build_focal_laser_scar_type,
    build_grid_laser_scar_type,
    build_macular_laser_scar_type
)
from eye_extractor.sections.document import create_doc_and_sections

# Test pattern.
_pattern_cases = [
    (lst.FOCAL_PAT, 'focal laser scars', True),
    (lst.FOCAL_PAT, 'focal tx scars', True),
    (lst.FOCAL_PAT, 'Focal scars', True),
    (lst.FOCAL_PAT, 'focal OU', False),
    (lst.MAC_FOCAL_PAT, 'focal OU', True),
    (lst.GRID_PAT, 'focal (grid) scars', True),
    (lst.GRID_PAT, 'grid laser scars', True),
    (lst.MAC_GRID_PAT, 'grid OU', True),
    (lst.MACULAR_PAT, 'macular scars', True),
    (lst.MACULAR_PAT, 'macula flat, peripheral laser scars', True),
    (lst.MAC_PANRETINAL_PAT, 'previous prp', True),
    (lst.PANRETINAL_PAT, 'prp scarring', True),
]


def _get_pattern_cases():
    return [(x[0], x[1], x[2]) for x in _pattern_cases]


@pytest.mark.parametrize('pat, text, exp', _get_pattern_cases())
def test_laser_scar_type_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) == exp


# Test extract and build.
_focal_extract_and_build_cases = [
    ('focal laser scars OU', {}, 1, 1, -1),
    ('focal tx scars OS', {}, -1, 1, -1),
    ('', {'MACULA': 'Focal scars ou.'}, 1, 1, -1),
    ('focal scars no new nvd', {}, -1, -1, 1),
    ('old focal tx scars OD', {}, 1, -1, -1),
    ('¶Macula: choroidal scar OD with focal laser scars', {}, 1, -1, -1),
    ('', {'MACULA': 'focal OU; no CS ME; ERM OS'}, 1, 1, -1),
    ('Central macular thickness: 123 um, No SRF, few focal scars', {}, -1, -1, 1),
    ('L: classification: macula thin, but normal contour Central macular thickness: 123 um, No SRF, few focal scars',
     {}, -1, 1, -1),
]

_grid_extract_and_build_cases = [
    ('focal (grid) scars OU', {}, 1, 1, -1),
    ('full grid laser scars', {}, -1, -1, 1),
    ('scars (grid) OD', {}, 1, -1, -1),
]

_macular_extract_and_build_cases = [
    ('', {'MACULA': 'Large disciform scars OU'}, 1, 1, -1),
    ('', {'MACULA': 'laser scars OD'}, 1, -1, -1),
    ('macular scars OS.', {}, -1, 1, -1),
    ('macula flat, peripheral laser  OS', {}, -1, 1, -1)
]


@pytest.mark.parametrize('text, sections, exp_focal_dr_laser_scar_type_re, exp_focal_dr_laser_scar_type_le, '
                         'exp_focal_dr_laser_scar_type_unk',
                         _focal_extract_and_build_cases)
def test_focal_laser_scar_type_extract_and_build(text,
                                                 sections,
                                                 exp_focal_dr_laser_scar_type_re,
                                                 exp_focal_dr_laser_scar_type_le,
                                                 exp_focal_dr_laser_scar_type_unk):
    doc = create_doc_and_sections(text, sections)
    pre_json = lst.get_laser_scar_type(doc)
    post_json = json.loads(json.dumps(pre_json))
    result = build_focal_laser_scar_type(post_json)
    assert result['focal_dr_laser_scar_type_re'] == exp_focal_dr_laser_scar_type_re
    assert result['focal_dr_laser_scar_type_le'] == exp_focal_dr_laser_scar_type_le
    assert result['focal_dr_laser_scar_type_unk'] == exp_focal_dr_laser_scar_type_unk


@pytest.mark.parametrize('text, sections, exp_grid_dr_laser_scar_type_re, exp_grid_dr_laser_scar_type_le, '
                         'exp_grid_dr_laser_scar_type_unk',
                         _grid_extract_and_build_cases)
def test_grid_laser_scar_type_extract_and_build(text,
                                                sections,
                                                exp_grid_dr_laser_scar_type_re,
                                                exp_grid_dr_laser_scar_type_le,
                                                exp_grid_dr_laser_scar_type_unk):
    doc = create_doc_and_sections(text, sections)
    pre_json = lst.get_laser_scar_type(doc)
    post_json = json.loads(json.dumps(pre_json))
    result = build_grid_laser_scar_type(post_json)
    assert result['grid_dr_laser_scar_type_re'] == exp_grid_dr_laser_scar_type_re
    assert result['grid_dr_laser_scar_type_le'] == exp_grid_dr_laser_scar_type_le
    assert result['grid_dr_laser_scar_type_unk'] == exp_grid_dr_laser_scar_type_unk


@pytest.mark.parametrize('text, sections, exp_macular_dr_laser_scar_type_re, exp_macular_dr_laser_scar_type_le, '
                         'exp_macular_dr_laser_scar_type_unk',
                         _macular_extract_and_build_cases)
def test_macular_laser_scar_type_extract_and_build(text,
                                                   sections,
                                                   exp_macular_dr_laser_scar_type_re,
                                                   exp_macular_dr_laser_scar_type_le,
                                                   exp_macular_dr_laser_scar_type_unk):
    doc = create_doc_and_sections(text, sections)
    pre_json = lst.get_laser_scar_type(doc)
    post_json = json.loads(json.dumps(pre_json))
    result = build_macular_laser_scar_type(post_json)
    assert result['macular_dr_laser_scar_type_re'] == exp_macular_dr_laser_scar_type_re
    assert result['macular_dr_laser_scar_type_le'] == exp_macular_dr_laser_scar_type_le
    assert result['macular_dr_laser_scar_type_unk'] == exp_macular_dr_laser_scar_type_unk
