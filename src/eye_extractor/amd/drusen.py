import re

from eye_extractor.laterality import build_laterality_table, create_variable

SMALL_DRUSEN_PAT = re.compile(
    r'('
    r'(very\W*)?fine'
    r'|scattered'
    r'|occasional'
    r'|rare'
    r'|few'
    r'|mild'
    r'|small(er)?'
    r'|trace'
    r'|light'
    r')(\s*\w+){3} drusen\b',
    re.I
)
INTERMEDIATE_DRUSEN_PAT = re.compile(
    r'('
    r'intermediate'
    r'|moderate'
    r')(\s*\w+){3} drusen\b',
    re.I
)
LARGE_DRUSEN_PAT = re.compile(
    r'('
    r'dense'
    r'|large'
    r'|heavy'
    r'|big'
    r')(\s*\w+){3} drusen\b',
    re.I
)

DRUSEN_PAT = re.compile(r'drusen', re.I)
HARD_DRUSEN_PAT = re.compile(r'(hard drusen)', re.I)
SOFT_DRUSEN_PAT = re.compile(r'(soft drusen)', re.I)
BOTH_DRUSEN_PAT = re.compile(r'(soft(\s*(and|,|/)\s*hard)?|hard(\s*(and|,|/)\s*soft)?) drusen', re.I)
NO_DRUSEN_PAT = re.compile(r'((no|or) drusen)', re.I)


def get_drusen(text, *, headers=None, lateralities=None):
    data = {}
    if headers:
        if macula_text := headers.get('MACULA', None):
            lateralities = build_laterality_table(macula_text)
            data |= find_drusen(macula_text, lateralities)
    else:
        if not lateralities:
            lateralities = build_laterality_table(text)
        data |= find_drusen(text, lateralities)
    return data


def find_drusen(text, lateralities):
    """
    Designed so that subsequent variables can overwrite earlier ones
    :param text:
    :param lateralities:
    :return:
    """
    data = {}
    for m in DRUSEN_PAT.finditer(text):
        create_variable(data, text, m, lateralities, 'drusen_size', {
            'value': 4, 'term': m.group(), 'label': 'unknown', 'source': 'MACULA',
        })
        create_variable(data, text, m, lateralities, 'drusen_type', {
            'value': 4, 'term': m.group(), 'label': 'unknown', 'source': 'MACULA',
        })
    for m in NO_DRUSEN_PAT.finditer(text):
        create_variable(data, text, m, lateralities, 'drusen_size', {
            'value': 0, 'term': m.group(), 'label': 'no', 'source': 'MACULA',
        })
        create_variable(data, text, m, lateralities, 'drusen_type', {
            'value': 0, 'term': m.group(), 'label': 'no', 'source': 'MACULA',
        })

    for m in BOTH_DRUSEN_PAT.finditer(text):
        create_variable(data, text, m, lateralities, 'drusen_size', {
            'value': 3, 'term': m.group(), 'label': 'both', 'source': 'MACULA',
        })

    for m in HARD_DRUSEN_PAT.finditer(text):
        create_variable(data, text, m, lateralities, 'drusen_size', {
            'value': 1, 'term': m.group(), 'label': 'hard', 'source': 'MACULA',
        })

    for m in SOFT_DRUSEN_PAT.finditer(text):
        create_variable(data, text, m, lateralities, 'drusen_size', {
            'value': 2, 'term': m.group(), 'label': 'soft', 'source': 'MACULA',
        })

    for m in SMALL_DRUSEN_PAT.finditer(text):
        create_variable(data, text, m, lateralities, 'drusen_type', {
            'value': 1, 'term': m.group(), 'label': 'small', 'source': 'MACULA',
        })
    for m in INTERMEDIATE_DRUSEN_PAT.finditer(text):
        create_variable(data, text, m, lateralities, 'drusen_type', {
            'value': 2, 'term': m.group(), 'label': 'intermediate', 'source': 'MACULA',
        })
    for m in LARGE_DRUSEN_PAT.finditer(text):
        create_variable(data, text, m, lateralities, 'drusen_type', {
            'value': 3, 'term': m.group(), 'label': 'large', 'source': 'MACULA',
        })
    return data
