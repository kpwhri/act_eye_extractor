import enum
import re

from eye_extractor.nlp.negate.negation import NEGWORD_SET, is_negated
from eye_extractor.laterality import create_new_variable
from eye_extractor.sections.document import Document
from eye_extractor.sections.patterns import PatternGroup


class Drusen(enum.IntEnum):
    UNKNOWN = -1
    NO = 0
    YES = 4

class DrusenSize(enum.IntEnum):
    UNKNOWN = Drusen.UNKNOWN
    NO = Drusen.NO
    YES = Drusen.YES
    SMALL = 1
    INTERMEDIATE = 2
    LARGE = 3

class DrusenType(enum.IntEnum):
    UNKNOWN = Drusen.UNKNOWN
    NO = Drusen.NO
    YES = Drusen.YES
    HARD = 1
    SOFT = 2
    BOTH = 3


small = r'(?:fine|very\W?fine|pin\W?point|tiny|small)'
intermediate = r'(?:intermediate|moderate)'
large = r'(?:large|heavy|big|confluent)'
words_lt3 = r'(\s+\w+){,3}'
drusen = 'drusen?'
soft = r'(?:soft|confluent)'

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
SOFT_DRUSEN_PAT = re.compile(rf'({soft} drusen)', re.I)
BOTH_DRUSEN_PAT = re.compile(rf'({soft}(\s*(and|,|/)\s*hard)?|hard(\s*(and|,|/)\s*{soft})?) drusen', re.I)
NO_DRUSEN_PAT = re.compile(rf'(?:(?:{"|".join(NEGWORD_SET)}) drusen)', re.I)


def extract_drusen(doc: Document):
    data = []
    if doc.sections:
        for section in doc.iter_sections(*PatternGroup.MACULA_ASSESSMENT_PLAN):
            data += find_drusen(section.text, section.lateralities)
    else:
        data += find_drusen(doc.text_no_hx, doc.lateralities_no_hx)
    return data


def find_drusen(text, lateralities):
    """
    Designed so that subsequent variables can overwrite earlier ones.
    In the build step, only the final element will be retained, so starting with the most general.
    :param text:
    :param lateralities:
    :return:
    """
    data = []
    for pattern, label, value, priority, targets in [
        (DRUSEN_PAT, 'yes', Drusen.YES, 0, ('drusen_size', 'drusen_type')),
        (NO_DRUSEN_PAT, 'no', Drusen.NO, 1, ('drusen_size', 'drusen_type')),
        (BOTH_DRUSEN_PAT, 'both', DrusenType.BOTH, 2, ('drusen_type',)),
        (HARD_DRUSEN_PAT, 'hard', DrusenType.HARD, 3, ('drusen_type',)),
        (SOFT_DRUSEN_PAT, 'soft', DrusenType.SOFT, 4, ('drusen_type',)),
        (SMALL_DRUSEN_PAT, 'small', DrusenSize.SMALL, 2, ('drusen_size',)),
        (INTERMEDIATE_DRUSEN_PAT, 'intermediate', DrusenSize.INTERMEDIATE, 3, ('drusen_size',)),
        (LARGE_DRUSEN_PAT, 'large', DrusenSize.LARGE, 2, ('drusen_size',)),
    ]:
        for m in pattern.finditer(text):
            negword = is_negated(m, text, word_window=1)
            for target in targets:
                data.append(
                    create_new_variable(text, m, lateralities, target, {
                        'value': Drusen.NO if negword else value,
                        'term': m.group(),
                        'label': f'negated {label}' if negword else label,
                        'negated': negword,
                        'source': 'MACULA',
                        'priority': priority,
                    })
                )
    return data
