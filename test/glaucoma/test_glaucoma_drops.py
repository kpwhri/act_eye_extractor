import json

import pytest

from eye_extractor.glaucoma.drops import NO_OPT_MED_RX, extract_glaucoma_drops
from eye_extractor.common.drug.drops import DROP_TO_ENUM, DROPS_RX
from eye_extractor.common.drug.shared import get_standardized_name
from eye_extractor.output.glaucoma import build_glaucoma_drops


@pytest.mark.parametrize('pat, text, exp_count, exp_neg', [
    (DROPS_RX, 'Eye medications (and last dose):    Active Ophthalmic Medications as of 01/01/2030: '
               ' LATANOPROST 0.005 % OPHTHALMIC DROPS', 1, None),
    (NO_OPT_MED_RX, 'No Active Ophthalmic Medications', 1, 'No'),
    (NO_OPT_MED_RX, 'Eye medications:none', 1, 'none'),
])
def test_patterns(pat, text, exp_count, exp_neg):
    matches = pat.findall(text)
    assert len(matches) == exp_count
    for match in matches:
        if exp_neg:
            assert exp_neg in match  # this is a tuple
        else:
            standardized_term = get_standardized_name(match)
            assert standardized_term in DROP_TO_ENUM


@pytest.mark.parametrize('text, exp_dict', [
    ('No Active Ophthalmic Medications', {'glaucoma_rx_none': 1}),
])
def test_drops_extract_and_build(text, exp_dict):
    pre_json = extract_glaucoma_drops(text)
    post_json = json.loads(json.dumps(pre_json))
    result = build_glaucoma_drops(post_json)
    for key, val in result.items():
        assert val == exp_dict.get(key, -1)
