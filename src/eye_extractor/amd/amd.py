import enum
import re

from eye_extractor.nlp.negate.historical import is_historical
from eye_extractor.nlp.negate.negation import is_negated
from eye_extractor.laterality import create_new_variable
from eye_extractor.nlp.negate.other_subject import is_other_subject
from eye_extractor.sections.document import Document
from eye_extractor.sections.patterns import PatternGroup

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


def _extract_amd(section_name, section_text, section_lateralities, priority=0):
    data = []
    for m in AMD_RX.finditer(section_text):
        if priority == 0 and ':' in section_text[m.end():m.end() + 2]:
            if 'y' not in section_text[m.end()+1:m.end() + 3]:
                continue
        negword = is_negated(m, section_text, word_window=3)
        histword = is_historical(m, section_text)
        osubjword = is_other_subject(m, section_text)
        data.append(
            create_new_variable(section_text, m, section_lateralities, 'amd', {
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


def extract_amd(doc: Document):
    data = []
    for section in doc.iter_sections(*PatternGroup.MACULA_ASSESSMENT_PLAN):
        data += _extract_amd(section.name, section.text, section.lateralities, priority=2)
    data += _extract_amd('ALL', doc.text_no_hx, doc.lateralities_no_hx)
    return data
