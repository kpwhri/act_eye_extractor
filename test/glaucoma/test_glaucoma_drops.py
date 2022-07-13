import pytest

from eye_extractor.glaucoma.drops import DROPS_RX, get_standardized_name, DRUG_TO_ENUM, NO_OPT_MED_RX


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
            assert standardized_term in DRUG_TO_ENUM
