"""
Exfoliation, but not glaucoma.
"""
import enum
import re

from eye_extractor.nlp.negate.negation import has_before, has_after, is_negated
from eye_extractor.laterality import create_new_variable
from eye_extractor.sections.document import Document


class Exfoliation(enum.IntEnum):
    UNKNOWN = -1
    NO = 0
    YES = 1


EXFOLIATION_PAT = re.compile(
    rf'(?:'
    rf'\b(?:p[de]x|pxf|xfs)\b'
    rf'|'
    rf'capsulare'
    rf'|'
    rf'(?:pseudo\W*)?exfoll?iat\w*'
    rf')',
    re.I
)


def extract_exfoliation(doc: Document):
    data = []
    text = doc.get_text()
    for m in EXFOLIATION_PAT.finditer(text):
        matchedtext = m.group()
        # cannot include glaucoma
        if has_before(m.start(), text, {'glauc', 'gl', 'glaucoma'},
                      word_window=3, skip_n_boundary_chars=1):
            continue
        elif has_after(m.end(), text, {'glauc', 'gl', 'glaucoma'},
                       word_window=3):
            continue
        negword = is_negated(m, text)
        data.append(
            create_new_variable(text, m, doc.get_lateralities(), 'exfoliation', {
                'value': Exfoliation.NO if negword else Exfoliation.YES,
                'term': matchedtext,
                'label': 'no' if negword else 'yes',
                'negated': negword,
                'regex': 'EXFOLIATION_PAT',
                'source': 'ALL',
            })
        )
    return data
