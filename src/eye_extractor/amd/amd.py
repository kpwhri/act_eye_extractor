import enum
import re

from eye_extractor.common.negation import is_negated
from eye_extractor.laterality import create_new_variable

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
        negword = is_negated(m, section_text, word_window=3)
        data.append(
            create_new_variable(section_text, m, None, 'amd', {
                'label': 'no' if negword else 'amd',
                'value': 0 if negword else 1,
                'negated': negword,
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
