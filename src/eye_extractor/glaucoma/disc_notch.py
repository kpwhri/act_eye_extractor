import re

from eye_extractor.nlp.negate.negation import is_negated
from eye_extractor.laterality import create_new_variable
from eye_extractor.sections.document import Document

NOTCH_PAT = re.compile(
    fr'\b(?:notch\w*)\b',
    re.I
)


def extract_disc_notch(doc: Document):
    """

    :param doc:
    :return:
    """
    data = []

    for m in NOTCH_PAT.finditer(doc.get_text()):
        negword = is_negated(m, doc.get_text())
        data.append(
            create_new_variable(doc.get_text(), m, doc.get_lateralities(), 'disc_notch', {
                'value': 0 if negword else 1,
                'term': m.group(),
                'label': 'no' if negword else 'yes',
                'negated': negword,
                'regex': 'NOTCH_PAT',
                'source': 'ALL',
            })
        )
    return data
