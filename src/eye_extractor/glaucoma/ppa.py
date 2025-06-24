"""
Peripapillary atropy

Peripapillary atrophy (PPA)
    RE    ppa_re    PPA    Binary    Y/N    Glaucoma
    LE    ppa_le    PPA    Binary    Y/N    Glaucoma
"""
import re

from eye_extractor.nlp.negate.negation import is_negated
from eye_extractor.laterality import create_new_variable
from eye_extractor.sections.document import Document

PPA_PAT = re.compile(
    rf'\b(?:'
    rf'peri\W*papillary\W*atrophy'
    rf'|ppa'
    rf')\b'
)


def extract_ppa(doc: Document):
    """
    Extract disc hemorrhage into binary variable: 1=yes, 0=no, -1=unknown (default in builder)
    :param text:
    :param headers:
    :param lateralities:
    :return:
    """
    text = doc.get_text()
    lateralities = doc.get_lateralities()
    data = []

    for m in PPA_PAT.finditer(text):
        negword = is_negated(m, text, boundary_chars=';:')
        data.append(
            create_new_variable(text, m, lateralities, 'ppa', {
                'value': 0 if negword else 1,
                'term': m.group(),
                'label': 'no' if negword else 'yes',
                'negated': negword,
                'regex': 'PPA_PAT',
                'source': 'ALL',
            })
        )
    return data
