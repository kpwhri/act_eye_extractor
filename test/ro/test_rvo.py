import json

import pytest

from eye_extractor.common.algo.treatment import STEROID_PAT, TRIAMCINOLONE_PAT, DEXAMETHASONE_PAT
from eye_extractor.headers import Headers
from eye_extractor.output.ro import build_rvo, build_rvo_type
from eye_extractor.ro.rvo import RVO_PAT, extract_rvo, RvoType, get_rvo_kind


@pytest.mark.parametrize('text', [
    'retinal vein occlusion',
    'rvaso',
    'BRVO',
    'CRVO',
    'central retinal vein occlusion',
])
def test_rvo_pattern(text):
    assert RVO_PAT.match(text)


@pytest.mark.parametrize('text, exp_value, exp_negword, exp_kind', [
    ('Branch retinal vein occlusion', 1, None, RvoType.BRVO),
    ('ASSESSMENT: central retinal vein occlusion', 1, None, RvoType.CRVO),
    ('no brvo', 0, 'no', RvoType.BRVO),
    ('has crvo', 1, None, RvoType.CRVO),
    ('rvo', 1, None, RvoType.RVO),
])
def test_rvo_value(text, exp_value, exp_negword, exp_kind):
    data = extract_rvo(text)
    assert len(data) > 0
    first_variable = list(data[0].values())[0]
    assert first_variable['value'] == exp_value
    assert first_variable['negated'] == exp_negword
    assert first_variable['kind'] == exp_kind


@pytest.mark.parametrize('data, exp_rvo_re, exp_rvo_le', [
    ([], -1, -1),
    ([{'rvo_yesno_le': {'value': 1, 'term': 'Branch retinal vein occlusion', 'label': 'yes', 'negated': None,
                        'regex': 'RVO_PAT', 'source': 'ALL'},
       'rvo_yesno_re': {'value': 1, 'term': 'Branch retinal vein occlusion', 'label': 'yes', 'negated': None,
                        'regex': 'RVO_PAT', 'source': 'ALL'}}],
     1, 1)
])
def test_rao_to_column(data, exp_rvo_re, exp_rvo_le):
    result = build_rvo(data)
    assert result['rvo_yesno_re'] == exp_rvo_re
    assert result['rvo_yesno_le'] == exp_rvo_le


@pytest.mark.parametrize('text, exp', [
    ('retinal vein occlusion', RvoType.RVO),
    ('rvaso', RvoType.RVO),
    ('BRVO', RvoType.BRVO),
    ('CRVO', RvoType.CRVO),
    ('central retinal vein occlusion', RvoType.CRVO),
])
def test_rvo_type(text, exp):
    m = RVO_PAT.search(text)
    kind = get_rvo_kind(m)
    assert kind == exp


@pytest.mark.parametrize('text, headers, exp_rvo_type_re, exp_rvo_type_le, exp_rvo_type_unk', [
    ('Branch retinal vein occlusion RE', {}, RvoType.BRVO, RvoType.UNKNOWN, RvoType.UNKNOWN),
    ('ASSESSMENT: central retinal vein occlusion', {}, RvoType.UNKNOWN, RvoType.UNKNOWN, RvoType.CRVO),
    ('no brvo', {}, RvoType.UNKNOWN, RvoType.UNKNOWN, RvoType.BRVO),
    (' rvo', {}, RvoType.UNKNOWN, RvoType.UNKNOWN, RvoType.RVO),
    ('has crvo', {}, RvoType.UNKNOWN, RvoType.UNKNOWN, RvoType.CRVO),
])
def test_rvo_type_extract_and_build(text, headers, exp_rvo_type_re, exp_rvo_type_le, exp_rvo_type_unk):
    pre_json = extract_rvo(text, headers=Headers(headers), lateralities=None)
    post_json = json.loads(json.dumps(pre_json))
    result = build_rvo_type(post_json, skip_output_mappings=True)  # skip mappings to redcap output
    assert result['rvo_type_re'] == exp_rvo_type_re
    assert result['rvo_type_le'] == exp_rvo_type_le
    assert result['rvo_type_unk'] == exp_rvo_type_unk


@pytest.mark.parametrize('pattern, text, exp', [
    (STEROID_PAT, 'steroids', True),
    (TRIAMCINOLONE_PAT, 'triamcinolone acetonide', True),
    (DEXAMETHASONE_PAT, 'dexamethasone implant', True),
])
def test_rvo_treatment_patterns(pattern, text, exp):
    assert bool(pattern.search(text)) == exp
