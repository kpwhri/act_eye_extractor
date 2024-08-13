import enum
import re

from eye_extractor.nlp.negate.negation import is_negated
from eye_extractor.laterality import build_laterality_table, create_new_variable


class Scar(enum.IntEnum):
    UNKNOWN = -1
    NO = 0
    YES = 1
    MACULAR = 2
    SUBRETINAL = 3
    DISCIFORM = 4


scar = r'(?:scars?|fibros[ie]s|fibrous)'
subret = r'(?:sub\s*ret\w*)'

SCAR_PAT = re.compile(
    rf'\b(?:'
    rf'{scar}'
    rf')\b',
    re.I
)

MACULAR_SCAR_PAT = re.compile(
    rf'\b(?:'
    rf'macula\w*\s*{scar}'
    rf'|{scar}\s+(?:\w+\s*){{,2}}macula\w*'
    rf')\b',
    re.I
)

SUBRET_SCAR_PAT = re.compile(
    rf'\b(?:'
    rf'{subret}\s*{scar}'
    rf'|{scar}\s+(?:\w+\s*){{,2}}{subret}'
    rf')\b',
    re.I
)

DISCIFORM_SCAR_PAT = re.compile(
    rf'\b(?:'
    rf'disci\w*\s*{scar}'
    rf'|{scar}\s+(?:\w+\s*){{,2}}disci\w*'
    rf')\b',
    re.I
)


def extract_subret_fibrous(text, *, headers=None, lateralities=None):
    data = []
    if headers:
        for sect_label, sect_text in headers.iterate('MACULA'):
            _extract_subret_fibrous(sect_text, data, sect_label)
    if not data:
        _extract_subret_fibrous(text, data, 'ALL')
    return data


def _extract_subret_fibrous(text, data, sect_label):
    for pat, label, value in [
        (DISCIFORM_SCAR_PAT, 'DISCIFORM_SCAR_PAT', Scar.DISCIFORM),
        (SUBRET_SCAR_PAT, 'SUBRET_SCAR_PAT', Scar.SUBRETINAL),
        (MACULAR_SCAR_PAT, 'MACULAR_SCAR_PAT', Scar.MACULAR),
        (SCAR_PAT, 'SCAR_PAT', Scar.YES),
    ]:
        if sect_label == 'ALL' and value == Scar.YES:  # Why is this included??
            continue  # only from MACULA section
        curr_text = text
        for m in pat.finditer(curr_text):
            lateralities = build_laterality_table(curr_text)
            negword = is_negated(m, curr_text, word_window=3)
            data.append(
                create_new_variable(curr_text, m, lateralities, 'subret_fibrous', {
                    'value': Scar.NO if negword else value,
                    'term': m.group(),
                    'label': 'no' if negword else value.name.lower(),
                    'negated': negword,
                    'regex': label,
                    'source': sect_label,
                })
            )
            text = text[:m.start()] + text[m.end():]
