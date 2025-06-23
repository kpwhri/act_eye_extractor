import enum
import re

from eye_extractor.common.shared_patterns import retinal
from eye_extractor.nlp.negate.negation import is_negated, has_before, NEGWORD_UNKNOWN_PHRASES
from eye_extractor.common.severity import extract_severity, Severity
from eye_extractor.laterality import build_laterality_table, create_new_variable
from eye_extractor.sections.document import Document


class HemorrhageType(enum.IntEnum):
    UNKNOWN = -1
    NONE = 0
    YES_NOS = 1
    INTRARETINAL = 2
    DOT_BLOT = 3
    PRERETINAL = 4
    VITREOUS = 5
    SUBRETINAL = 6


heme = r'hem(?:orr?hage|e)?s?'
vitreous = r'vit(reous)?'

INTRARETINAL_PAT = re.compile(
    r'\b('
    rf'intra{retinal}\s*{heme}'
    rf'|{heme}\s*intra{retinal}'
    rf'|irh'
    r')\b',
    re.IGNORECASE
)
DOT_BLOT_PAT = re.compile(
    rf'\b('
    rf'd(ot)?(\W+|\s+and\s+)b(lot)?\s*{heme}'
    rf'|dot\s*{heme}'
    rf'|blot\s*{heme}'
    rf'|dbh'
    rf')\b',
    re.IGNORECASE
)
PRERETINAL_PAT = re.compile(
    rf'\b('
    rf'pre{retinal}\s*{heme}'
    rf'|{heme}\s*pre{retinal}'
    rf'|prh'
    rf')\b',
    re.IGNORECASE
)
VITREOUS_PAT = re.compile(
    rf'\b('
    rf'{vitreous}\s*{heme}'
    rf'|{heme}\s*{vitreous}'
    rf'|vh'
    rf')\b',
    re.IGNORECASE
)
SUBRETINAL_PAT = re.compile(
    rf'\b('
    rf'sub{retinal}\s*{heme}'
    rf'|{heme}\s*sub{retinal}'
    rf'|srh'
    rf')\b',
    re.IGNORECASE
)
HEME_NOS_PAT = re.compile(
    r'\b('
    rf'{heme}'
    r')\b',
    re.I
)


def get_hemorrhage_type(doc: Document) -> list:
    data = []
    for new_var in _get_hemorrhage_type(doc.get_text(), doc.get_lateralities(), 'ALL'):
        data.append(new_var)

    return data


def _get_hemorrhage_type(text: str, lateralities, source: str) -> dict:
    for pat, hem_type, hem_label, sev_var in [
        (INTRARETINAL_PAT, HemorrhageType.INTRARETINAL, 'intraretinal', 'intraretinal_hem'),
        (DOT_BLOT_PAT, HemorrhageType.DOT_BLOT, 'dot blot', 'dotblot_hem'),
        (PRERETINAL_PAT, HemorrhageType.PRERETINAL, 'preretinal', 'preretinal_hem'),
        (VITREOUS_PAT, HemorrhageType.VITREOUS, 'vitreous', 'vitreous_hem'),
        (SUBRETINAL_PAT, HemorrhageType.SUBRETINAL, 'subretinal', 'subretinal_hem_dr'),
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
                continue
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
