import enum
import re

from eye_extractor.common.negation import is_negated
from eye_extractor.common.severity import extract_severity, Severity
from eye_extractor.laterality import build_laterality_table, create_new_variable


class HemorrhageType(enum.IntEnum):
    UNKNOWN = -1
    NONE = 0
    INTRARETINAL = 1
    DOT_BLOT = 2
    PRERETINAL = 3
    VITREOUS = 4
    SUBRETINAL = 5


INTRARETINAL_PAT = re.compile(
        r'\b('
        r'intraretinal\s*hem(orrhage|e)'
        r'|hem(orrhage|e)\s*intraretinal'
        r')\b'
)
DOT_BLOT_PAT = re.compile(
        r'\b('
        r'dot blot\s*hem(orrhage|e)'
        r'|hem(orrhage|e)\s*dot blot'
        r')\b'
)
PRERETINAL_PAT = re.compile(
        r'\b('
        r'preretinal\s*hem(orrhage|e)'
        r'|hem(orrhage|e)\s*preretinal'
        r')\b'
)
VITREOUS_PAT = re.compile(
        r'\b('
        r'vitreous\s*hem(orrhage|e)'
        r'|hem(orrhage|e)\s*vitreous'
        r')\b'
)
SUBRETINAL_PAT = re.compile(
        r'\b('
        r'subretinal\s*hem(orrhage|e)'
        r'|hem(orrhage|e)\s*subretinal'
        r')\b'
)


def get_hemorrhage_type(text: str, *, headers=None, lateralities=None) -> list:
    if not lateralities:
        lateralities = build_laterality_table(text)
    data = []
    for new_var in _get_hemorrhage_type(text, lateralities, 'ALL'):
        data.append(new_var)
    if headers:
        pass

    return data


def _get_hemorrhage_type(text: str, lateralities, source: str) -> dict:
    for pat, hem_type, hem_label, sev_var in [
        (INTRARETINAL_PAT, HemorrhageType.INTRARETINAL, 'intraretinal', 'intraretinal_hem'),
        (DOT_BLOT_PAT, HemorrhageType.DOT_BLOT, 'dot blot', 'dotblot_hem'),
        (PRERETINAL_PAT, HemorrhageType.PRERETINAL, 'preretinal', None),
        (VITREOUS_PAT, HemorrhageType.VITREOUS, 'vitreous', None),
        (SUBRETINAL_PAT, HemorrhageType.SUBRETINAL, 'subretinal', None),
    ]:
        for m in pat.finditer(text):
            negated = is_negated(m, text, word_window=3)
            context = f'{text[max(0, m.start() - 100): m.start()]} {text[m.end():min(len(text), m.end() + 100)]}'
            severities = extract_severity(context)
            if sev_var and severities:
                for sev in severities:
                    yield create_new_variable(text, m, lateralities, sev_var, {
                        'value': sev,
                        'term': m.group(),
                        'label': f'{hem_label} hemorrhage',
                        'negated': negated,
                        'regex': f'{hem_label.upper()}_PAT',
                        'source': source,
                    })
            elif negated:
                yield create_new_variable(text, m, lateralities, sev_var, {
                    'value': Severity.NONE,
                    'term': m.group(),
                    'label': f'No {hem_label} hemorrhage',
                    'negated': negated,
                    'regex': f'{hem_label.upper()}_PAT',
                    'source': source,
                })
            yield create_new_variable(text, m, lateralities, 'hemorrhage_typ_dr', {
                    'value': HemorrhageType.NONE if negated else hem_type,
                    'term': m.group(),
                    'label': f'No {hem_label} hemorrhage' if negated else f'{hem_label} hemorrhage',
                    'negated': negated,
                    'regex': f'{hem_label.upper()}_PAT',
                    'source': source,
                })
