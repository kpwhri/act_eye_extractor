import re

from eye_extractor.common.negation import NEGWORD_SET
from eye_extractor.laterality import build_laterality_table, create_new_variable

small = r'(?:(very\W*)?fine|scattered|occasional|rare|few|mild|small(er)?|trace|light)'
intermediate = r'(?:intermediate|moderate)'
large = r'(?:dense|extensive|large|heavy|big|many|lots)'
words_lt3 = r'(\s+\w+){,3}'
drusen = 'drusen?'

SMALL_DRUSEN_PAT = re.compile(
    rf'(?:'
    rf'{small}{words_lt3}\s*{drusen}\b'
    rf'|\b{drusen}{words_lt3}\s*{small}'
    rf')',
    re.I
)
INTERMEDIATE_DRUSEN_PAT = re.compile(
    r'(?:'
    rf'{intermediate}{words_lt3}\s*{drusen}\b'
    rf'|\b{drusen}{words_lt3}\s*{intermediate}'
    rf')',
    re.I
)
LARGE_DRUSEN_PAT = re.compile(
    r'(?:'
    rf'{large}{words_lt3}\s*{drusen}\b'
    rf'|\b{drusen}{words_lt3}\s*{large}'
    rf')',
    re.I
)

DRUSEN_PAT = re.compile(r'drusen', re.I)
HARD_DRUSEN_PAT = re.compile(r'(hard drusen)', re.I)
SOFT_DRUSEN_PAT = re.compile(r'(soft drusen)', re.I)
BOTH_DRUSEN_PAT = re.compile(r'(soft(\s*(and|,|/)\s*hard)?|hard(\s*(and|,|/)\s*soft)?) drusen', re.I)
NO_DRUSEN_PAT = re.compile(rf'(?:(?:{"|".join(NEGWORD_SET)}) drusen)', re.I)


def extract_drusen(text, *, headers=None, lateralities=None):
    data = []
    if headers:
        for macula_header, macula_text in headers.iterate('MACULA', 'COMMENTS', 'ASSESSMENT_COMMENTS'):
            lateralities = build_laterality_table(macula_text)
            data += find_drusen(macula_text, lateralities)
    else:
        if not lateralities:
            lateralities = build_laterality_table(text)
        data += find_drusen(text, lateralities)
    return data


def find_drusen(text, lateralities=None):
    """
    Designed so that subsequent variables can overwrite earlier ones.
    In the build step, only the final element will be retained, so starting with the most general.
    :param text:
    :param lateralities:
    :return:
    """
    lateralities = lateralities or build_laterality_table(text)
    data = []
    for pattern, label, value, priority, targets in [
        (DRUSEN_PAT, 'yes', 4, 0, ('drusen_size', 'drusen_type')),
        (NO_DRUSEN_PAT, 'no', 0, 1, ('drusen_size', 'drusen_type')),
        (BOTH_DRUSEN_PAT, 'both', 3, 2, ('drusen_type',)),
        (HARD_DRUSEN_PAT, 'hard', 1, 3, ('drusen_type',)),
        (SOFT_DRUSEN_PAT, 'soft', 2, 4, ('drusen_type',)),
        (SMALL_DRUSEN_PAT, 'small', 1, 2, ('drusen_size',)),
        (INTERMEDIATE_DRUSEN_PAT, 'intermediate', 2, 3, ('drusen_size',)),
        (LARGE_DRUSEN_PAT, 'large', 3, 2, ('drusen_size',)),
    ]:
        for m in pattern.finditer(text):
            for target in targets:
                data.append(
                    create_new_variable(text, m, lateralities, target, {
                        'value': value,
                        'term': m.group(),
                        'label': label,
                        'source': 'MACULA',
                        'priority': priority,
                    })
                )
    return data
