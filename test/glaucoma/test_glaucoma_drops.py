import pytest

from eye_extractor.glaucoma.drops import DROPS_RX, get_standardized_name, DRUG_TO_ENUM


@pytest.mark.parametrize('pat, text, exp_count', [
    (DROPS_RX, 'Eye medications (and last dose):    Active Ophthalmic Medications as of 01/01/2030:  '
               'LATANOPROST 0.005 % OPHTHALMIC DROPS', 1)
])
def test_patterns(pat, text, exp_count):
    matches = pat.findall(text)
    assert len(matches) == exp_count
    for match in matches:
        standardized_term = get_standardized_name(match)
        assert standardized_term in DRUG_TO_ENUM
