import pytest

from eye_extractor.history.famhx import create_family_history
from eye_extractor.sections.document import create_doc_and_sections


@pytest.mark.parametrize('text, exp', [
    ('FAMILY HISTORY:    Diabetes no    Migraine yes    SOCIAL HISTORY:',
     {'diabetes': 0, 'migraine': 1}),
    ('FAMILY HISTORY:    \nDiabetes no    \nMigraine yes    \nSOCIAL HISTORY:',
     {'diabetes': 0, 'migraine': 1}),
    ('FAMILY HISTORY:    \nno-Diabetes    \nyes- Migraine    \nSOCIAL HISTORY:',
     {'diabetes': 0, 'migraine': 1}),
])
def test_family_history_section(text, exp):
    doc = create_doc_and_sections(text)
    res = create_family_history(doc)
    assert res == exp
