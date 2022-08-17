import pytest

from eye_extractor.dr import laser_scar_type as lst
# from eye_extractor.headers import Headers
# from eye_extractor.output.dr import build_laser_scar_type


# Test pattern.
_pattern_cases = [
    (lst.PANRETINAL_PAT, 'PRP scars', True),
    (lst.PANRETINAL_PAT, 'PRP marks visible', True),
    (lst.FOCAL_PAT, 'focal laser scars', True),
    (lst.FOCAL_PAT, 'focal tx scars', True),
    (lst.GRID_PAT, 'focal (grid) scars', True),
    (lst.GRID_PAT, 'grid laser scars', True),
    (lst.MACULAR_PAT, 'macular scars', True),
    (lst.MACULAR_PAT, 'macula flat, peripheral laser scars', True),
]


def _get_pattern_cases():
    return [(x[0], x[1], x[2]) for x in _pattern_cases]


@pytest.mark.parametrize('pat, text, exp', _get_pattern_cases())
def test_laser_scar_type_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) == exp


# Test extract and build.
_panretinal_extract_and_build_cases = [
    ('PRP scars OS', {}, -1, 1, -1),
    ('PRP marks visible OD', {}, 1, -1, -1),
    ('PRP scarring', {}, -1, -1, 1)
]

_focal_extract_and_build_cases = [
    ('focal laser scars OU', {}, 1, 1, -1),
    ('focal tx scars OS', {}, -1, 1, -1),
    ('', {'MACULA': 'Focal scars ou.'}, 1, 1, -1),
    ('focal scars no new nvd', {}, -1, -1, 1),
    ('old focal tx scars OD', {}, 1, -1, -1),
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


# @pytest.mark.parametrize('text, headers, exp_dr_laser_scar_type_re, exp_dr_laser_scar_type_le, '
#                          'exp_dr_laser_scar_type_unk',
#                          _extract_and_build_cases)
# def test_laser_scar_type_extract_and_build(text,
#                                            headers,
#                                            exp_dr_laser_scar_type_re,
#                                            exp_dr_laser_scar_type_le,
#                                            exp_dr_laser_scar_type_unk):
#     pre_json = tx.extract_treatment(text, headers=Headers(headers), lateralities=None)
#     post_json = json.loads(json.dumps(pre_json))
#     result = build_lasertype_new(post_json)
#     assert result['dr_laser_scar_type_re'] == exp_dr_laser_scar_type_re
#     assert result['dr_laser_scar_type_le'] == exp_dr_laser_scar_type_le
#     assert result['dr_laser_scar_type_unk'] == exp_dr_laser_scar_type_unk
