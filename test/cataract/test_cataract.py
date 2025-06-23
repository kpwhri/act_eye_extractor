import pytest

from eye_extractor.common.json import dumps_and_loads_json
from eye_extractor.output.cataract import build_cataract
from eye_extractor.cataract.cataract import CATARACT_PAT, extract_cataract
from eye_extractor.sections.document import create_doc_and_sections


@pytest.mark.parametrize('text', [
    'significant cataract',
])
def test_cataract_pattern(text):
    assert CATARACT_PAT.match(text)


@pytest.mark.parametrize('text, exp_value, exp_negword', [
    ('visually significant cataract', 1, None),
])
def test_cataract_value(text, exp_value, exp_negword):
    doc = create_doc_and_sections(text)
    data = extract_cataract(doc)
    assert len(data) > 0
    first_variable = list(data[0].values())[0]
    assert first_variable['value'] == exp_value
    assert first_variable['negated'] == exp_negword


@pytest.mark.parametrize('data, cataract_yesno_re, cataract_yesno_le', [
    ([], -1, -1),
    ([{'cataractiol_yesno_le': {'value': 1},
       'cataractiol_yesno_re': {'value': 1}}],
     1, 1)
])
def test_cataract_to_column(data, cataract_yesno_re, cataract_yesno_le):
    result = build_cataract(data)
    assert result['cataractiol_yesno_le'] == cataract_yesno_le
    assert result['cataractiol_yesno_re'] == cataract_yesno_re


@pytest.mark.parametrize('text, yesno_re, yesno_le, yesno_unk', [
    ('visually significant cataract', -1, -1, 1),
    ('no visually significant cataract', -1, -1, 0),
])
def test_extract_and_build_cataract(text, yesno_re, yesno_le, yesno_unk):
    doc = create_doc_and_sections(text)
    pre_json = extract_cataract(doc)
    post_json = dumps_and_loads_json(pre_json)
    result = build_cataract(post_json)
    assert result['cataractiol_yesno_re'] == yesno_re
    assert result['cataractiol_yesno_le'] == yesno_le
    assert result['cataractiol_yesno_unk'] == yesno_unk
