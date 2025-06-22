import enum
import re

from eye_extractor.nlp.negate.negation import is_negated
from eye_extractor.laterality import create_new_variable
from eye_extractor.sections.document import Document


class ChoroidalNeoVasc(enum.IntEnum):
    UNKNOWN = -1
    NO = 0
    YES = 1


CNV_PAT = re.compile(
    rf'\b(?:'
    rf'cnvm?s?'
    rf'|chor\w*\W*neovas\w*'
    rf')\b',
    re.I
)


def extract_choroidalneovasc(doc: Document):
    data = []
    if doc.sections:
        for section in doc.iter_sections('assessment'):
            data += _extract_cnv(section.text, section.lateralities, section.name)
    data += _extract_cnv(doc.text_no_hx, doc.lateralities, 'ALL')
    return data


def _extract_cnv(text, lateralities, sect_label):
    data = []
    for m in CNV_PAT.finditer(text):
        negword = is_negated(m, text, word_window=3)
        data.append(
            create_new_variable(text, m, lateralities, 'choroidalneovasc', {
                'value': ChoroidalNeoVasc.NO if negword else ChoroidalNeoVasc.YES,
                'term': m.group(),
                'label': 'no' if negword else 'yes',
                'negated': negword,
                'regex': 'CNV_PAT',
                'source': sect_label,
            })
        )
    return data
