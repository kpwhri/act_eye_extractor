import re

from eye_extractor.nlp.negate.negation import is_negated
from eye_extractor.laterality import create_new_variable
from eye_extractor.sections.oct_macula import find_oct_macula_sections

MACULAR_CYST = re.compile(
    rf'\b(?:'
    rf'cysts?'
    rf')\b'
)


def _extract_macular_cyst(text, lateralities, source, *, known_laterality=None, known_date=None, priority=0):
    data = []
    for m in MACULAR_CYST.finditer(text):
        negword = is_negated(m, text)
        data.append(
            create_new_variable(text, m, lateralities, 'macular_cyst', {
                'value': 0 if negword else 1,
                'label': 'no' if negword else 'yes',
                'term': m.group(),
                'negated': negword,
                'regex': 'MACULAR_CYST',
                'source': source,
                'date': known_date,
                'priority': priority,
            }, known_laterality=known_laterality)
        )
    return data


def extract_macular_cyst(text, *, headers=None, lateralities=None):
    data = []
    for section_dict in find_oct_macula_sections(text):
        for lat, values in section_dict.items():
            data += _extract_macular_cyst(values['text'], None, 'OCT MACULA',
                                          known_laterality=lat, known_date=values['date'], priority=2)
    for section_name, section_text in headers.iterate('MACULA', 'MAC'):
        data += _extract_macular_cyst(section_text, None, section_name, priority=1)
    return data
