import re

from eye_extractor.common.get_variable import get_variable
from eye_extractor.nlp.inline_section import is_periphery
from eye_extractor.nlp.negate.negation import is_negated, is_any_negated, has_before
from eye_extractor.laterality import create_new_variable
from eye_extractor.sections.document import Document

subretinal = r'(?:sub\W*ret(?:inal)?|sr)'
heme = r'(?:hem\w*|hg)'

SRH_PAT = re.compile(
    rf'\b(?:'
    rf'{subretinal}\W*{heme}'
    rf'|sr\s*hf?e?'
    rf'|sub\W*(?:and|&)\W*intra\W*ret\w*\s*{heme}'
    rf')\b',
    re.IGNORECASE
)

# Context FSAs.
ALL_PRE_IGNORE = {
    'follow': {
        'up': True,
        None: False
    },
    'no': {
        'new': True,
        None: False
    },
    None: False
}


def extract_subretinal_hemorrhage(doc: Document):
    data = []
    # prioritizing oct results
    for section_dict in doc.oct_macula_sections:
        for lat, values in section_dict.items():
            for m in SRH_PAT.finditer(values['text']):
                if has_before(m if isinstance(m, int) else m.start(),
                              values['text'],
                              terms=ALL_PRE_IGNORE,
                              word_window=3):
                    continue
                if is_negated(m, values['text'], {'intraretinal', 'retinal', 'subarachnoid', 'vitreous'},
                              word_window=1):
                    continue
                negword = is_any_negated(m, values['text'])
                data.append(
                    create_new_variable(values['text'], m, doc.lateralities, 'subretinal_hem', {
                        'value': 0 if negword else 1,
                        'term': m.group(),
                        'label': 'no' if negword else 'yes',
                        'negated': negword,
                        'regex': 'SRH_PAT',
                        'source': 'OCT MACULA',
                        'priority': 2,
                        'date': values['date']
                    }, known_laterality=lat)
                )

    data += get_variable(doc, _extract_subret_heme,
                         text=doc.text_no_oct_macula,
                         lateralities=doc.lateralities_no_oct_macula,
                         target_headers=['macula'])

    return data


def _extract_subret_heme(text: str, lateralities, source: str):
    for m in SRH_PAT.finditer(text):  # everywhere
        if is_periphery(m.start(), text):
            continue
        if has_before(m if isinstance(m, int) else m.start(),
                      text,
                      terms=ALL_PRE_IGNORE,
                      word_window=5):
            continue
        negated = is_negated(m, text, word_window=3)
        yield create_new_variable(text, m, lateralities, 'subretinal_hem', {
            'value': 0 if negated else 1,
            'term': m.group(),
            'label': 'no' if negated else 'yes',
            'negated': negated,
            'regex': 'SRH_PAT',
            'source': source,
        })

# def extract_subretinal_hemorrhage(text, *, headers=None, lateralities=None):
#     lateralities = lateralities or build_laterality_table(text)
#     data = []
#     # prioritizing oct results
#     for section_dict in find_oct_macula_sections(text):
#         for lat, values in section_dict.items():
#             for m in SRH_PAT.finditer(values['text']):
#                 if is_negated(m, values['text'], {'intraretinal', 'retinal', 'subarachnoid', 'vitreous'},
#                               word_window=1):
#                     continue
#                 negword = is_any_negated(m, values['text'])
#                 data.append(
#                     create_new_variable(values['text'], m, lateralities, 'subretinal_hem', {
#                         'value': 0 if negword else 1,
#                         'term': m.group(),
#                         'label': 'no' if negword else 'yes',
#                         'negated': negword,
#                         'regex': 'SRH_PAT',
#                         'source': 'OCT MACULA',
#                         'priority': 2,
#                         'date': values['date']
#                     }, known_laterality=lat)
#                 )
#     text = remove_macula_oct(text)
#
#     for m in SRH_PAT.finditer(text):  # everywhere
#         negword = is_any_negated(m, text)
#         data.append(
#             create_new_variable(text, m, lateralities, 'subretinal_hem', {
#                 'value': 0 if negword else 1,
#                 'term': m.group(),
#                 'label': 'no' if negword else 'yes',
#                 'negated': negword,
#                 'regex': 'SRH_PAT', 'source': 'ALL',
#             })
#         )
#     if headers:  # macula text only
#         for macula_header, macula_text in headers.iterate('MACULA'):
#             lateralities = build_laterality_table(macula_text)
#             for m in SRH_PAT.finditer(macula_text):
#                 # exclusion words (wrong heme)
#                 if is_negated(m, macula_text, {'intraretinal', 'retinal'}):
#                     continue
#                 negword = is_any_negated(m, macula_text)
#                 data.append(
#                     create_new_variable(macula_text, m, lateralities, 'subretinal_hem', {
#                         'value': 0 if negword else 1,
#                         'term': m.group(),
#                         'label': 'no' if negword else 'yes',
#                         'negated': negword,
#                         'regex': 'SRH_PAT',
#                         'source': macula_header,
#                     })
#                 )
#     return data
