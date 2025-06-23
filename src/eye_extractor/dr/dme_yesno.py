import re

from eye_extractor.common.get_variable import get_variable
from eye_extractor.nlp.negate.negation import has_before, is_negated, NEGWORD_UNKNOWN_PHRASES
from eye_extractor.laterality import create_new_variable
from eye_extractor.sections.document import Document
from eye_extractor.sections.patterns import SectionName

macular_edema = fr'(?:macula\w*\s+edema)'

DME_YESNO_PAT = re.compile(
    r'\b('
    r'(cs|d)me'
    rf'|diabetic\s+{macular_edema}'
    rf'|diabetic\s+retinopathy\s+(?:\w*\s+)+{macular_edema}'
    rf'|clinical\w*\s+signific\w*\s{macular_edema}'
    r')\b',
    re.I
)


def get_dme_yesno(doc: Document) -> list:
    return get_variable(doc, _get_dme_yesno,
                        target_headers=[
                            SectionName.ASSESSMENT,
                            SectionName.MACULA,
                            SectionName.PLAN,
                            SectionName.SUBJECTIVE
                        ],
                        split_char='.')


def _get_dme_yesno(text: str, lateralities, source: str) -> dict:
    for m in DME_YESNO_PAT.finditer(text):
        if has_before(m if isinstance(m, int) else m.start(),
                      text,
                      terms={'r/o', 'indication', 'possible'},
                      word_window=2,
                      boundary_chars='¶'):
            continue
        negated = is_negated(m, text, word_window=4, return_unknown=True)
        if negated in NEGWORD_UNKNOWN_PHRASES:
            continue
        yield create_new_variable(text, m, lateralities, 'dmacedema_yesno', {
            'value': 0 if negated else 1,
            'term': m.group(),
            'label': 'No' if negated else 'Yes',
            'negated': negated,
            'regex': 'DME_YESNO_PAT',
            'source': source,
        })
