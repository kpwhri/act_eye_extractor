import re

from eye_extractor.common.negation import is_negated
from eye_extractor.laterality import build_laterality_table, create_new_variable
from eye_extractor.sections.oct_macula import find_oct_macula_sections, remove_macula_oct

SRH_PAT = re.compile(
    r'('
    r'subretinal\W*(hem\w+|\bhg\b)'
    r'|\bsrh'
    r')',
    re.IGNORECASE
)

SRH_IN_MACULA_PAT = re.compile(
    r'('
    r'\bheme?s?\b'
    r'|hemorrhage'
    r'|\bsrh'
    r')',
    re.IGNORECASE
)


def extract_subretinal_hemorrhage(text, *, headers=None, lateralities=None):
    lateralities = lateralities or build_laterality_table(text)
    data = []
    # prioritizing oct results
    for section_dict in find_oct_macula_sections(text):
        for lat, values in section_dict.items():
            for m in SRH_IN_MACULA_PAT.finditer(values['text']):
                if is_negated(m, values['text'], {'intraretinal', 'retinal'}):
                    continue
                negword = is_negated(m, values['text'])
                data.append(
                    create_new_variable(values['text'], m, lateralities, 'subretinal_hem', {
                        'value': 0 if negword else 1,
                        'term': m.group(),
                        'label': 'no' if negword else 'yes',
                        'negated': negword,
                        'regex': 'SRH_IN_MACULA_PAT',
                        'source': 'OCT MACULA',
                        'priority': 2,
                        'date': values['date']
                    }, known_laterality=lat)
                )
    text = remove_macula_oct(text)

    for m in SRH_PAT.finditer(text):  # everywhere
        negword = is_negated(m, text)
        data.append(
            create_new_variable(text, m, lateralities, 'subretinal_hem', {
                'value': 0 if negword else 1,
                'term': m.group(),
                'label': 'no' if negword else 'yes',
                'negated': negword,
                'regex': 'SRH_PAT', 'source': 'ALL',
            })
        )
    if headers:  # macula text only
        for macula_header, macula_text in headers.iterate('MACULA'):
            lateralities = build_laterality_table(macula_text)
            for m in SRH_IN_MACULA_PAT.finditer(macula_text):
                # exclusion words (wrong heme)
                if is_negated(m, macula_text, {'intraretinal', 'retinal'}):
                    continue
                negword = is_negated(m, macula_text)
                data.append(
                    create_new_variable(macula_text, m, lateralities, 'subretinal_hem', {
                        'value': 0 if negword else 1,
                        'term': m.group(),
                        'label': 'no' if negword else 'yes',
                        'negated': negword,
                        'regex': 'SRH_IN_MACULA_PAT',
                        'source': 'MACULA',
                    })
                )
    return data
