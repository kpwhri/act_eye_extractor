import datetime

import pytest

from eye_extractor.amd.dry import DRY_PAT, DRY_AMD_PAT, extract_dryamd_severity
from eye_extractor.amd.ga import GeoAtrophy
from eye_extractor.common.json import dumps_and_loads_json
from eye_extractor.headers import Headers
from eye_extractor.output.amd import build_dryamd_severity, augment_dryamd_severity


@pytest.mark.parametrize('pat, text, exp', [
    (DRY_PAT, 'dry', True),
    (DRY_AMD_PAT, 'dry amd', True),
    (DRY_AMD_PAT, 'atrophic armd', True),
])
def test_dry_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) is exp


@pytest.mark.parametrize(
    'text, headers, exp_dryamd_severity_re, exp_dryamd_severity_le, exp_dryamd_severity_unk, note_date', [
        ('', {'MACULA': 'dry'}, 'UNKNOWN', 'UNKNOWN', 'YES', None),
        ('', {'MACULA': 'not dry'}, 'UNKNOWN', 'UNKNOWN', 'NO', None),
        # test historical
        ('', {'MACULA': '12/5/2010 not dry'}, 'UNKNOWN', 'UNKNOWN', 'UNKNOWN', datetime.date(2022, 10, 5)),
        ('', {'MACULA': '12/5/2010 not dry 10/4/2022 dry'}, 'UNKNOWN', 'UNKNOWN', 'YES', datetime.date(2022, 10, 5)),
        ('', {'ASSESSMENT': 'atrophy od'}, 'YES', 'UNKNOWN', 'UNKNOWN', None),
        ('atrophic armd', None, 'UNKNOWN', 'UNKNOWN', 'YES', None),
        ('OD: non-exudative senile AMD', None, 'YES', 'UNKNOWN', 'UNKNOWN', None),
    ])
def test_dry_extract_build(text, headers, exp_dryamd_severity_re, exp_dryamd_severity_le,
                           exp_dryamd_severity_unk, note_date):
    pre_json = extract_dryamd_severity(text, headers=Headers(headers))
    post_json = dumps_and_loads_json(pre_json)
    result = build_dryamd_severity(post_json, note_date=note_date)
    assert result['dryamd_severity_re'] == exp_dryamd_severity_re
    assert result['dryamd_severity_le'] == exp_dryamd_severity_le
    assert result['dryamd_severity_unk'] == exp_dryamd_severity_unk


def test_dry_augment():
    ga_result = {'geoatrophy_re': GeoAtrophy.YES}
    dry_result = {'dryamd_severity_re': 'UNKNOWN'}
    res = augment_dryamd_severity(dry_result, ga_result=ga_result)
    assert res['dryamd_severity_re'] == 'YES'
