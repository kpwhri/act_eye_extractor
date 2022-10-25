import json

import pytest

from eye_extractor.cataract.posterior_cap_opacity import build_from_number_pco, extract_posterior_capsular_opacity
from eye_extractor.headers import Headers
from eye_extractor.output.cataract import build_posterior_cap_opacity


@pytest.mark.parametrize('pat, text, exp_match', [
    (build_from_number_pco(1), '1+ PCO', True),
    (build_from_number_pco(1), 'PCO 1+', True),
    (build_from_number_pco(1), '1+', False),
    (build_from_number_pco(1), 'gd 1 PCO', True),
    (build_from_number_pco(1), 'gd 1+ PCO', True),
])
def test_iol_patterns(pat, text, exp_match):
    assert bool(pat.search(text)) == exp_match


@pytest.mark.parametrize('lens_text, exp_posterior_cap_opacity_re, exp_posterior_cap_opacity_le', [
    ('IOL OD: 1+ PCO IOL OS: tr pco', '1+', 'tr'),
])
def test_extract_and_build_iol_lens(lens_text, exp_posterior_cap_opacity_re, exp_posterior_cap_opacity_le):
    res = extract_posterior_capsular_opacity(None, headers=Headers({'LENS': lens_text}))
    from_json = json.loads(json.dumps(res, default=str))
    variables = build_posterior_cap_opacity(from_json)
    assert variables['posterior_cap_opacity_re'] == exp_posterior_cap_opacity_re
    assert variables['posterior_cap_opacity_le'] == exp_posterior_cap_opacity_le
