import enum
import re

from eye_extractor.nlp.negate.historical import is_historical
from eye_extractor.nlp.negate.negation import is_negated
from eye_extractor.laterality import create_new_variable
from eye_extractor.nlp.negate.other_subject import is_other_subject

AMD_RX = re.compile(
    r'\b(?:'
    r'ar?md'
    r'|(age\W*related\W*)?macular?\s*degener\w+'
    r'|macular?\s+degener\w+'
    r')\b',
    re.I
)


class AMD(enum.IntEnum):
    UNKNOWN = -1
    NO = 0
    YES = 1


def _extract_amd(section_name, section_text, priority=0):
    data = []
    for m in AMD_RX.finditer(section_text):
        if priority == 0 and ':' in section_text[m.end():m.end() + 2]:
            if 'y' not in section_text[m.end()+1:m.end() + 3]:
                continue
        negword = is_negated(m, section_text, word_window=3)
        histword = is_historical(m, section_text)
        osubjword = is_other_subject(m, section_text)
        data.append(
            create_new_variable(section_text, m, None, 'amd', {
                'label': 'no' if negword else 'amd',
                'value': 0 if negword else -1 if histword or osubjword else 1,
                'negated': negword,
                'othersubj': osubjword,
                'historical': histword,
                'term': m.group(),
                'priority': priority,
                'source': section_name,
            })
        )
    return data


def extract_amd(text, *, headers=None, lateralities=None):
    data = []
    for section_name, section_text in headers.iterate('ASSESSMENT', 'PLAN', 'COMMENTS', 'MACULA'):
        data += _extract_amd(section_name, section_text, priority=2)
    data += _extract_amd('ALL', text)
    return data
