import re

from eye_extractor.nlp.negate.negation import is_negated
from eye_extractor.laterality import create_new_variable
from eye_extractor.sections.document import Document

DH_PAT = re.compile(
    fr'\b(?:'
    fr'dh|dis[ck]\W*hem\w*'
    fr')\b',
    re.I
)


def extract_disc_hem(doc: Document):
    """
    Extract disc hemorrhage into binary variable: 1=yes, 0=no, -1=unknown (default in builder)
    :param doc:
    :return:
    """
    data = []

    for m in DH_PAT.finditer(doc.get_text()):
        negword = is_negated(m, doc.get_text())
        data.append(
            create_new_variable(doc.get_text(), m, doc.get_lateralities(), 'disc_hem', {
                'value': 0 if negword else 1,
                'term': m.group(),
                'label': 'no' if negword else 'yes',
                'negated': negword,
                'regex': 'DH_PAT',
                'source': 'ALL',
            })
        )
    return data
