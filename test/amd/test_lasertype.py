import json

import pytest

from eye_extractor.amd.lasertype import LASER_PAT, PHOTODYNAMIC_PAT, THERMAL_PAT, extract_lasertype
from eye_extractor.headers import Headers
from eye_extractor.output.amd import build_lasertype


@pytest.mark.parametrize('pat, text, exp', [
    (LASER_PAT, 'laser', True),
    (PHOTODYNAMIC_PAT, 'photodynamic therapy', True),
    (PHOTODYNAMIC_PAT, 'pdt', True),
    (THERMAL_PAT, 'thermal laser', True),
])
def test_lasertype_pattern(pat, text, exp):
    m = pat.search(text)
    assert bool(m) == exp


@pytest.mark.parametrize('text, headers, exp_amd_lasertype_re, exp_amd_lasertype_le, exp_amd_lasertype_unk', [
    ('', {'ASSESSMENT': 'laser therapy od'}, 1, -1, -1),
    ('', {'ASSESSMENT': 'OS: Photodynamic therapy'}, -1, 2, -1),
    ('', {'ASSESSMENT': 'thermal laser'}, -1, -1, 3),
])
def test_lasertype_extract_and_build(text, headers, exp_amd_lasertype_re, exp_amd_lasertype_le, exp_amd_lasertype_unk):
    pre_json = extract_lasertype(text, headers=Headers(headers), lateralities=None)
    post_json = json.loads(json.dumps(pre_json))
    result = build_lasertype(post_json)
    assert result['amd_lasertype_re'] == exp_amd_lasertype_re
    assert result['amd_lasertype_le'] == exp_amd_lasertype_le
    assert result['amd_lasertype_unk'] == exp_amd_lasertype_unk
