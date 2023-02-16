import json
import pytest

from eye_extractor.dr.exudates import (
    EXUDATES_PAT,
    get_exudates,
    HARD_EXUDATES_ABBR_PAT,
    HARD_EXUDATES_PAT
)
from eye_extractor.headers import Headers
from eye_extractor.output.dr import build_exudates, build_hard_exudates

# Test pattern.
_pattern_cases = [
    (EXUDATES_PAT, 'exud', True),
    (EXUDATES_PAT, 'exuds', True),
    (EXUDATES_PAT, 'exudates', True),
    (EXUDATES_PAT, 'exudate', True),
    (EXUDATES_PAT, 'soft exudate', False),
    (EXUDATES_PAT, 'soft exudates', False),
    (EXUDATES_PAT, 'hard exudates', False),
    (EXUDATES_PAT, 'HE', False),
    (HARD_EXUDATES_PAT, 'Hard exud', True),
    (HARD_EXUDATES_PAT, 'Hard Exudate', True),
    (HARD_EXUDATES_PAT, 'hard exudates', True),
    (HARD_EXUDATES_ABBR_PAT, 'HE', True),
    (HARD_EXUDATES_ABBR_PAT, 'Angle Van Herick', False),
    (HARD_EXUDATES_ABBR_PAT, 'He ate a pickle', False),
]


def _get_pattern_cases():
    return [(x[0], x[1], x[2]) for x in _pattern_cases]


@pytest.mark.parametrize('pat, text, exp', _get_pattern_cases())
def test_exudates_patterns(pat, text, exp):
    m = pat.search(text)
    assert bool(m) == exp


# Test extract and build.
_exudates_extract_and_build_cases = [
    ('MACULA: clr OU\nno hem, no exud, no CWS OU', {}, 0, 0, -1),
    ('MACULA: clr OU\nno hem, no exud, no\nCWS OU', {}, 0, 0, -1),
    # Unless specified, all conditions in negated list are OU.
    # Idea: process laterality differently in (negated)? list format.
    # Since no laterality specified, laterality should be OU.
    pytest.param('No Microaneurysms/hemes, cotton-wool spots, exudates, IRMA, Venous beading, NVE',
                 {}, 0, 0, -1, marks=pytest.mark.skip()),
]

_hard_exudates_extract_and_build_cases = [
    ('OS:  Numerous hard exudates superior macula', {}, -1, 1, -1),
    # Unless specified, all conditions in negated list are OU.
    # Idea: process laterality differently in (negated)? list format.
    # Since no laterality specified, laterality should be OU.
    pytest.param('Periphery: RE trace BDR; LE with extensive PRP, but no NVZE/hg/CWS/HE noted today\n',
                 {}, 0, 0, -1, marks=pytest.mark.skip()),
    # Since no laterality specified, laterality should be OU.
    # TODO: Ask Chantelle if 'no CWS OR HE;' counts as negated list.
    pytest.param('Vessels: scattered MA/dot hgs, but no CWS or HE;', {}, 0, 0, -1, marks=pytest.mark.skip()),
]


@pytest.mark.parametrize('text, headers, exp_exudates_re, exp_exudates_le, exp_exudates_unk',
                         _exudates_extract_and_build_cases)
def test_exudates_extract_and_build(text,
                                    headers,
                                    exp_exudates_re,
                                    exp_exudates_le,
                                    exp_exudates_unk):
    pre_json = get_exudates(text, headers=Headers(headers))
    post_json = json.loads(json.dumps(pre_json))
    result = build_exudates(post_json)
    assert result['exudates_re'] == exp_exudates_re
    assert result['exudates_le'] == exp_exudates_le
    assert result['exudates_unk'] == exp_exudates_unk


@pytest.mark.parametrize('text, headers, exp_hard_exudates_re, exp_hard_exudates_le, exp_hard_exudates_unk',
                         _hard_exudates_extract_and_build_cases)
def test_hard_exudates_extract_and_build(text,
                                         headers,
                                         exp_hard_exudates_re,
                                         exp_hard_exudates_le,
                                         exp_hard_exudates_unk):
    pre_json = get_exudates(text, headers=Headers(headers))
    post_json = json.loads(json.dumps(pre_json))
    result = build_hard_exudates(post_json)
    assert result['hard_exudates_re'] == exp_hard_exudates_re
    assert result['hard_exudates_le'] == exp_hard_exudates_le
    assert result['hard_exudates_unk'] == exp_hard_exudates_unk
