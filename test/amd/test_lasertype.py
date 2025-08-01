import json

import pytest

import eye_extractor.amd.lasertype as lt
import eye_extractor.common.algo.treatment as tx
from eye_extractor.sections.document import create_doc_and_sections
from eye_extractor.output.amd import build_lasertype, build_lasertype_new

_pattern_cases = [
    (tx.LASER_PAT, lt.LASER_PAT, 'laser', True),
    (tx.PHOTODYNAMIC_PAT, lt.PHOTODYNAMIC_PAT, 'photodynamic therapy', True),
    (tx.PHOTODYNAMIC_PAT, lt.PHOTODYNAMIC_PAT, 'pdt', True),
    (tx.THERMAL_PAT, lt.THERMAL_PAT, 'thermal laser', True),
]

_extract_and_build_cases = [
    ('', {'ASSESSMENT': 'laser therapy od'}, 1, -1, -1),
    ('', {'ASSESSMENT': 'OS: Photodynamic therapy'}, -1, 2, -1),
    ('', {'ASSESSMENT': 'thermal laser'}, -1, -1, 3),
]


def _get_pattern_cases(old_version=False):
    return [(x[1] if old_version else x[0], x[2], x[3]) for x in _pattern_cases]


# NEW VERSIONS
@pytest.mark.parametrize('pat, text, exp', _get_pattern_cases(old_version=False))
def test_treatment_patterns_for_lasertype(pat, text, exp):
    m = pat.search(text)
    assert bool(m) == exp


@pytest.mark.parametrize('text, sections, exp_amd_lasertype_re, exp_amd_lasertype_le, exp_amd_lasertype_unk',
                         _extract_and_build_cases)
def test_tx_extract_and_build_for_lasertype(text, sections, exp_amd_lasertype_re, exp_amd_lasertype_le, exp_amd_lasertype_unk):
    doc = create_doc_and_sections(text, sections)
    pre_json = tx.extract_treatment(doc)
    post_json = json.loads(json.dumps(pre_json))
    result = build_lasertype_new(post_json)
    assert result['amd_lasertype_re'] == exp_amd_lasertype_re
    assert result['amd_lasertype_le'] == exp_amd_lasertype_le
    assert result['amd_lasertype_unk'] == exp_amd_lasertype_unk


# OLD VERSIONS
@pytest.mark.parametrize('pat, text, exp', _get_pattern_cases(old_version=True))
def test_lasertype_pattern(pat, text, exp):
    m = pat.search(text)
    assert bool(m) == exp


@pytest.mark.parametrize('text, sections, exp_amd_lasertype_re, exp_amd_lasertype_le, exp_amd_lasertype_unk',
                         _extract_and_build_cases)
def test_lasertype_extract_and_build(text, sections, exp_amd_lasertype_re, exp_amd_lasertype_le, exp_amd_lasertype_unk):
    doc = create_doc_and_sections(text, sections)
    pre_json = lt.extract_lasertype(doc)
    post_json = json.loads(json.dumps(pre_json))
    result = build_lasertype(post_json)
    assert result['amd_lasertype_re'] == exp_amd_lasertype_re
    assert result['amd_lasertype_le'] == exp_amd_lasertype_le
    assert result['amd_lasertype_unk'] == exp_amd_lasertype_unk
