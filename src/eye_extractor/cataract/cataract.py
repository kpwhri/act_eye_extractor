import re

from eye_extractor.nlp.negate.negation import is_negated
from eye_extractor.laterality import build_laterality_table, create_new_variable
from eye_extractor.sections.document import Document

CATARACT_PAT = re.compile(
    r'(?:'
    r'(need|require)s?\W*cataract\W*surgery'
    r'|(significant|cortical|nuclear|mild)\W*cataract'
    r')',
    re.I
)


def extract_cataract(doc: Document):
    # TODO: what sections?
    data = []
    for m in CATARACT_PAT.finditer(doc.get_text()):
        negword = is_negated(m, doc.get_text())
        data.append(
            create_new_variable(doc.get_text(), m, doc.get_lateralities(), 'cataractiol_yesno', {
                'value': 0 if negword else 1,
                'term': m.group(),
                'label': 'no' if negword else 'yes',
                'negated': negword,
                'regex': 'CATARACT_PAT', 'source': 'ALL',
            })
        )
    return data
