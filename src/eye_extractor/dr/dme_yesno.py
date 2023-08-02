import re

from eye_extractor.common.get_variable import get_variable
from eye_extractor.nlp.negate.negation import is_negated, is_post_negated
from eye_extractor.laterality import build_laterality_table, create_new_variable

DME_YESNO_PAT = re.compile(
    r'\b('
    r'(cs|d)me'
    r'|diabetic\s+macular\s+edema'
    r'|diabetic\s+retinopathy\s+(?:\w*\s+)+macular\s+edema'
    r')\b',
    re.I
)


def get_dme_yesno(text: str, *, headers=None, lateralities=None) -> list:
    return get_variable(text, _get_dme_yesno, headers=headers,
                        target_headers=['ASSESSMENT', 'MACULA', 'PLAN'], lateralities=lateralities)


def _get_dme_yesno(text: str, lateralities, source: str) -> dict:
    for m in DME_YESNO_PAT.finditer(text):
        negated = is_negated(m, text, word_window=4)
        yield create_new_variable(text, m, lateralities, 'dmacedema_yesno', {
            'value': 0 if negated else 1,
            'term': m.group(),
            'label': 'No' if negated else 'Yes',
            'negated': negated,
            'regex': 'DME_YESNO_PAT',
            'source': source,
        })
