import datetime

import pytest

from eye_extractor.amd.drusen import find_drusen, DrusenSize, DrusenType, SMALL_DRUSEN_PAT
from eye_extractor.common.json import dumps_and_loads_json
from eye_extractor.output.amd import get_drusen_size, get_drusen_type
from eye_extractor.sections.document import create_doc_and_sections


@pytest.mark.parametrize('text, exp_size_re, exp_size_le, exp_type_re, exp_type_le, note_date', [
    ('WNL OU',
     DrusenSize.UNKNOWN, DrusenSize.UNKNOWN, DrusenType.UNKNOWN, DrusenType.UNKNOWN, None),
    ('w/o drusen ou',
     DrusenSize.NO, DrusenSize.NO, DrusenType.NO, DrusenType.NO, None),
    ('drusen and RPE drop out OU',
     DrusenSize.YES, DrusenSize.YES, DrusenType.YES, DrusenType.YES, None),
    ('OD: large drusen',
     DrusenSize.LARGE, DrusenSize.UNKNOWN, DrusenType.YES, DrusenType.UNKNOWN, None),
    ('OD: 10/2/2011 large drusen',
     DrusenSize.UNKNOWN, DrusenSize.UNKNOWN, DrusenType.UNKNOWN, DrusenType.UNKNOWN,
     datetime.date(2011, 10, 9)),
    ('OD: 10/2/2011 no drusen 10/9/2011 confluent drusen',
     DrusenSize.LARGE, DrusenSize.UNKNOWN, DrusenType.SOFT, DrusenType.UNKNOWN,
     datetime.date(2011, 10, 9)),
    ('OD: 10/9/2011 no drusen 10/2/2011 confluent drusen',
     DrusenSize.NO, DrusenSize.UNKNOWN, DrusenType.NO, DrusenType.UNKNOWN,
     datetime.date(2011, 10, 9)),
    ('OD: no drusen OS: confluent drusen',
     DrusenSize.NO, DrusenSize.LARGE, DrusenType.NO, DrusenType.SOFT, None),
    ('intermediate drusen od, large drusen os',
     DrusenSize.INTERMEDIATE, DrusenSize.LARGE, DrusenType.YES, DrusenType.YES, None),
    ('pin-point drusen od, no drusen os',
     DrusenSize.SMALL, DrusenSize.NO, DrusenType.YES, DrusenType.NO, None),
])
def test_drusen(text, exp_size_re, exp_size_le, exp_type_re, exp_type_le, note_date):
    doc = create_doc_and_sections(text)
    pre_json = find_drusen(doc.text, doc.lateralities)
    post_json = dumps_and_loads_json(pre_json)
    size_result = get_drusen_size(post_json, note_date=note_date)
    type_result = get_drusen_type(post_json, note_date=note_date)
    # size
    assert size_result['drusen_size_le'] == exp_size_le
    assert size_result['drusen_size_re'] == exp_size_re
    # type
    assert type_result['drusen_type_le'] == exp_type_le
    assert type_result['drusen_type_re'] == exp_type_re


@pytest.mark.parametrize(('pattern', 'text', 'match'), [
    (SMALL_DRUSEN_PAT, 'pin-point drusen', False),
])
def test_drusen_size_patterns(pattern, text, match):
    m = pattern.match(text)
    if m is None and match is not None:
        raise ValueError(f'Pattern {pattern} failed to match text {text}: resulted in {m}.')
    if match:
        assert m.group() == match
