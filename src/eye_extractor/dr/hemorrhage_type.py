import enum
import re

from eye_extractor.nlp.negate.negation import is_negated, has_before, NEGWORD_UNKNOWN_PHRASES
from eye_extractor.common.severity import extract_severity, Severity
from eye_extractor.laterality import build_laterality_table, create_new_variable


class HemorrhageType(enum.IntEnum):
    UNKNOWN = -1
    NONE = 0
    YES_NOS = 1
    INTRARETINAL = 2
    DOT_BLOT = 3
    PRERETINAL = 4
    VITREOUS = 5
    SUBRETINAL = 6


INTRARETINAL_PAT = re.compile(
    r'\b('
    r'intraretinal\s*hem(orrhage|e)s?'
    r'|hem(orrhage|e)\s*intraretinal'
    r')\b',
    re.IGNORECASE
)
DOT_BLOT_PAT = re.compile(
    r'\b('
    r'd(ot)?(\W+|\s+and\s+)b(lot)?\s*hem(orrhage|e)s?'
    r'|dot\s*hem(orrhage|e)?s?'
    r'|blot\s*hem(orrhage|e)?'
    r')\b',
    re.IGNORECASE
)
PRERETINAL_PAT = re.compile(
    r'\b('
    r'preretinal\s*hem(orrhage|e)s?'
    r'|hem(orrhage|e)\s*preretinal'
    r')\b',
    re.IGNORECASE
)
VITREOUS_PAT = re.compile(
    r'\b('
    r'vitreous\s*hem(orrhage|e)s?'
    r'|hem(orrhage|e)\s*vitreous'
    r')\b',
    re.IGNORECASE
)
SUBRETINAL_PAT = re.compile(
    r'\b('
    r'subretinal\s*hem(orrhage|e)s?'
    r'|hem(orrhage|e)\s*subretinal'
    r')\b',
    re.IGNORECASE
)
HEME_NOS_PAT = re.compile(
    r'\b('
    r'hem(orrhage|e)'
    r')\b',
    re.I
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
        (PRERETINAL_PAT, HemorrhageType.PRERETINAL, 'preretinal', 'preretinal_hem'),
        (VITREOUS_PAT, HemorrhageType.VITREOUS, 'vitreous', None),
        (SUBRETINAL_PAT, HemorrhageType.SUBRETINAL, 'subretinal', None),
        (HEME_NOS_PAT, HemorrhageType.YES_NOS, 'NOS', None),
    ]:
        for m in pat.finditer(text):
            negated = is_negated(m, text, word_window=3, return_unknown=True)
            if negated in NEGWORD_UNKNOWN_PHRASES:  # e.g., 'no new' -> UNKNOWN
                continue
            context = f'{text[max(0, m.start() - 100): m.start()]} {text[m.end():min(len(text), m.end() + 100)]}'
            severities = extract_severity(context)
            if has_before(m if isinstance(m, int) else m.start(),
                          text,
                          terms={'hx', 'h/o', 'resolved'},
                          boundary_chars='',
                          word_window=6):
                break
            if sev_var:
                # Severity found & positive instance.
                if severities:
                    for sev in severities:
                        yield create_new_variable(text, m, lateralities, sev_var, {
                            'value': sev,
                            'term': m.group(),
                            'label': f'{hem_label} hemorrhage',
                            'negated': negated,
                            'regex': f'{hem_label.upper()}_PAT',
                            'source': source,
                        })
                # Severity found & negative instance.
                elif negated:
                    yield create_new_variable(text, m, lateralities, sev_var, {
                        'value': Severity.NONE,
                        'term': m.group(),
                        'label': f'No {hem_label} hemorrhage',
                        'negated': negated,
                        'regex': f'{hem_label.upper()}_PAT',
                        'source': source,
                    })
                # Affirmative without severity quantifier.
                else:
                    yield create_new_variable(text, m, lateralities, sev_var, {
                        'value': Severity.YES_NOS,
                        'term': m.group(),
                        'label': f'{hem_label} hemorrhage',
                        'negated': negated,
                        'regex': f'{hem_label.upper()}_PAT',
                        'source': source,
                    })
            # Severity not found, both positive and negative instance.
            yield create_new_variable(text, m, lateralities, 'hemorrhage_typ_dr', {
                'value': HemorrhageType.NONE if negated else hem_type,
                'term': m.group(),
                'label': f'No {hem_label} hemorrhage' if negated else f'{hem_label} hemorrhage',
                'negated': negated,
                'regex': f'{hem_label.upper()}_PAT',
                'source': source,
            })
