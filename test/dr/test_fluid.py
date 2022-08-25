import json
import pytest

from eye_extractor.common.algo.fluid import extract_fluid, Fluid
from eye_extractor.headers import Headers
from eye_extractor.output.dr import build_fluid


# Patterns tested in 'amd/test_fluid.py'


@pytest.mark.parametrize('text, headers, exp_fluid_re, exp_fluid_le, exp_fluid_unk', [
    ('', {'MACULA': 'subretinal fluid od'}, 'SUBRETINAL FLUID', 'UNKNOWN', 'UNKNOWN'),
    ('', {'MACULA': 'with fluid and exudates'}, 'UNKNOWN', 'UNKNOWN', 'FLUID'),
    ('no SRF/IRF OS', {}, 'UNKNOWN', 'NO SUB AND INTRARETINAL FLUID', 'UNKNOWN'),
    ('No heme or fluid od', {}, 'NO', 'UNKNOWN', 'UNKNOWN'),
    ('no IRF OU', {}, 'NO INTRARETINAL FLUID', 'NO INTRARETINAL FLUID', 'UNKNOWN')
])
def test_fluid_extract_and_build(text, headers, exp_fluid_re, exp_fluid_le, exp_fluid_unk, ):
    pre_json = extract_fluid(text, headers=Headers(headers))
    post_json = json.loads(json.dumps(pre_json))
    result = build_fluid(post_json, skip_rename_variable=True)
    assert result['fluid_dr_re'] == exp_fluid_re
    assert result['fluid_dr_le'] == exp_fluid_le
    assert result['fluid_dr_unk'] == exp_fluid_unk
