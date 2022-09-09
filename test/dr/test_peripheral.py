import json
import pytest

from eye_extractor.dr.peripheral import (
    get_peripheral,
    PERI_HEME_PAT,
    PERI_HEADER_HEME_PAT,
    PERI_HEADER_LASER_SCARS_PAT,
    PRP_SCARS_PAT
)
from eye_extractor.headers import Headers
from eye_extractor.output.dr import build_peripheral_heme, build_prp_laser_scar

# Test pattern.
_pattern_cases = [
    (PERI_HEME_PAT, 'peripheral hemorrhage', True),
    (PERI_HEME_PAT, 'peripheral heme', True),
    (PRP_SCARS_PAT, 'prp laser scars', True),
    (PRP_SCARS_PAT, 'PRP laser scar OU', True),
    (PRP_SCARS_PAT, 'laser panretinal photo-coagulation scars', True),
    (PERI_HEADER_HEME_PAT, 'hemorrhage', True),
    (PERI_HEADER_HEME_PAT, 'heme', True),
    (PERI_HEADER_LASER_SCARS_PAT, 'laser scars', True),
]


def _get_pattern_cases():
    return [(x[0], x[1], x[2]) for x in _pattern_cases]


@pytest.mark.parametrize('pat, text, exp', _get_pattern_cases())
def test_laser_scar_type_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) == exp


# Test extract and build.
_peri_heme_extract_and_build_cases = [
    ('peripheral heme OD', {}, 1, -1, -1),
    ('peripheral hemorrhage OS', {}, -1, 1, -1),
    ('', {'PERIPHERAL': 'heme ou.'}, 1, 1, -1),
]

_prp_laser_scars_extract_and_build_cases = [
    ('PRP laser scars OD', {}, 1, -1, -1),
    ('prp tx scars OS', {}, -1, 1, -1),
    ('', {'PERIPHERAL': 'laser scars ou.'}, 1, 1, -1),
    ('panretinal photo-coagulation scars', {}, -1, -1, 1),
]


@pytest.mark.parametrize('text, headers, exp_peripheral_heme_re, exp_peripheral_heme_le, '
                         'exp_peripheral_heme_unk',
                         _peri_heme_extract_and_build_cases)
def test_peripheral_heme_extract_and_build(text,
                                           headers,
                                           exp_peripheral_heme_re,
                                           exp_peripheral_heme_le,
                                           exp_peripheral_heme_unk):
    pre_json = get_peripheral(text, headers=Headers(headers))
    post_json = json.loads(json.dumps(pre_json))
    result = build_peripheral_heme(post_json)
    assert result['peripheral_heme_re'] == exp_peripheral_heme_re
    assert result['peripheral_heme_le'] == exp_peripheral_heme_le
    assert result['peripheral_heme_unk'] == exp_peripheral_heme_unk


@pytest.mark.parametrize('text, headers, exp_prp_laser_scar_re, exp_prp_laser_scar_le, '
                         'exp_prp_laser_scar_unk',
                         _prp_laser_scars_extract_and_build_cases)
def test_prp_laser_scars_extract_and_build(text,
                                           headers,
                                           exp_prp_laser_scar_re,
                                           exp_prp_laser_scar_le,
                                           exp_prp_laser_scar_unk):
    pre_json = get_peripheral(text, headers=Headers(headers))
    post_json = json.loads(json.dumps(pre_json))
    result = build_prp_laser_scar(post_json)
    assert result['prp_laser_scar_re'] == exp_prp_laser_scar_re
    assert result['prp_laser_scar_le'] == exp_prp_laser_scar_le
    assert result['prp_laser_scar_unk'] == exp_prp_laser_scar_unk
