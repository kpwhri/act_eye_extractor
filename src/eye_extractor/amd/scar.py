import enum
import re

from eye_extractor.common.get_variable import get_variable
from eye_extractor.nlp.inline_section import is_periphery
from eye_extractor.nlp.negate.negation import has_before, is_negated
from eye_extractor.laterality import create_new_variable
from eye_extractor.sections.document import Document
from eye_extractor.sections.patterns import SectionName


class Scar(enum.IntEnum):
    UNKNOWN = -1
    NO = 0
    YES = 1
    MACULAR = 2
    SUBRETINAL = 3
    DISCIFORM = 4


scar = r'(?:scar(?:ring|s)?|fibros[ie]s|fibrous)(?!-like)'
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
    rf'|glial\s*{scar}'
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

# Context FSAs.
ALL_PRE_IGNORE = {
    'hx': True,
    'possibly': True,
    None: False
}
SCAR_PRE_IGNORE = {
    'laser': True,
    'peripheral': True,
    None: False
}


def extract_subret_fibrous(doc: Document):
    return get_variable(doc, _extract_subret_fibrous, target_headers=[
        SectionName.OCT, SectionName.MACULA, SectionName.ASSESSMENT, SectionName.PLAN],
                        search_full_text=False)


def _extract_subret_fibrous(text: str, lateralities, source: str):
    for pat, pat_label, variable in [
        (DISCIFORM_SCAR_PAT, 'DISCIFORM_SCAR_PAT', Scar.DISCIFORM),
        (SUBRET_SCAR_PAT, 'SUBRET_SCAR_PAT', Scar.SUBRETINAL),
        (MACULAR_SCAR_PAT, 'MACULAR_SCAR_PAT', Scar.MACULAR),
        (SCAR_PAT, 'SCAR_PAT', Scar.YES),
    ]:
        for m in pat.finditer(text):
            if has_before(m if isinstance(m, int) else m.start(),
                          text,
                          terms=ALL_PRE_IGNORE,
                          word_window=6):
                continue
            if pat_label == 'SCAR_PAT':
                if has_before(m if isinstance(m, int) else m.start(),
                              text,
                              terms=SCAR_PRE_IGNORE,
                              word_window=3):
                    continue
            if is_periphery(m.start(), text):
                continue
            negated = is_negated(m, text, word_window=3)
            yield create_new_variable(text, m, lateralities, 'subret_fibrous', {
                'value': Scar.NO if negated else variable,
                'term': m.group(),
                'label': 'no' if negated else variable.name.lower(),
                'negated': negated,
                'regex': pat_label,
                'source': source,
            })
