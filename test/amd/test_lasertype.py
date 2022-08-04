import json

import pytest

import eye_extractor.amd.lasertype as lt
import eye_extractor.common.algo.treatment as tx
from eye_extractor.headers import Headers
from eye_extractor.output.amd import build_lasertype

_pattern_cases = [
    (tx.LASER_PAT, lt.LASER_PAT, 'laser', True),
    (tx.PHOTODYNAMIC_PAT, lt.PHOTODYNAMIC_PAT, 'photodynamic therapy', True),
    (tx.PHOTODYNAMIC_PAT, lt.PHOTODYNAMIC_PAT, 'pdt', True),
    (tx.THERMAL_PAT, lt.THERMAL_PAT, 'thermal laser', True),
]


def _get_pattern_cases(old_version=False):
    return [(x[1] if old_version else x[0], x[2], x[3]) for x in _pattern_cases]


@pytest.mark.parametrize('pat, text, exp', _get_pattern_cases(old_version=True))
def test_lasertype_pattern(pat, text, exp):
    m = pat.search(text)
    assert bool(m) == exp


@pytest.mark.parametrize('text, headers, exp_amd_lasertype_re, exp_amd_lasertype_le, exp_amd_lasertype_unk', [
    ('', {'ASSESSMENT': 'laser therapy od'}, 1, -1, -1),
    ('', {'ASSESSMENT': 'OS: Photodynamic therapy'}, -1, 2, -1),
    ('', {'ASSESSMENT': 'thermal laser'}, -1, -1, 3),
])
def test_lasertype_extract_and_build(text, headers, exp_amd_lasertype_re, exp_amd_lasertype_le, exp_amd_lasertype_unk):
    pre_json = lt.extract_lasertype(text, headers=Headers(headers), lateralities=None)
    post_json = json.loads(json.dumps(pre_json))
    result = build_lasertype(post_json)
    assert result['amd_lasertype_re'] == exp_amd_lasertype_re
    assert result['amd_lasertype_le'] == exp_amd_lasertype_le
    assert result['amd_lasertype_unk'] == exp_amd_lasertype_unk
