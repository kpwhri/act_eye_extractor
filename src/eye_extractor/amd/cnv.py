import enum
import re

from eye_extractor.nlp.negate.negation import is_negated
from eye_extractor.laterality import build_laterality_table, create_new_variable


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


def extract_choroidalneovasc(text, *, headers=None, lateralities=None):
    lateralities = lateralities or build_laterality_table(text)
    data = []
    if headers:
        for sect_label, sect_text in headers.iterate('ASSESSMENT'):
            sect_lats = build_laterality_table(sect_text)
            _extract_cnv(sect_text, data, sect_lats, sect_label)
    _extract_cnv(text, data, lateralities, 'ALL')
    return data


def _extract_cnv(text, data, lateralities, sect_label):
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
