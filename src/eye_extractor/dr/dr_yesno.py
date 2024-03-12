import re

from eye_extractor.nlp.negate.negation import has_after, has_before, is_negated, is_post_negated
from eye_extractor.laterality import build_laterality_table, create_new_variable

# Patterns.
DR_YESNO_PAT = re.compile(
    r'\b('
    r'diabetic\s+retinopathy'
    r'|macular\s+edema\s+due\s+to\s+secondary\s+diabetes'
    r')\b',
    re.I
)
# Separate pattern to capture case-sensitive abbreviations.
DR_YESNO_ABBR_PAT = re.compile(
    r'\b('
    r'DR(?!\.)'
    r'|(N?P|BG?)DR'
    r'|DMR'
    r'|dr(?!\'s|\.)'
    r'|(n?p|bg?)dr'
    r'|dmr'
    r')\b',
)
DR_YESNO_NEG_PAT = re.compile(
    r'\b('
    r'without\s+retinopathy'
    r')\b'
)

# Context FSAs.
DR_YESNO_PRE_IGNORE = {
    'confirm': True,
    'does': {
        'patient': {
            'have': True,
            None: False,
        },
        None: False,
    },
    'exam': True,
    'surgeon': True,
    'tablet': True,
    None: False
}
DR_YESNO_POST_IGNORE = {
    'exam': True,
    'requires': {
        'refresh': True,
        None: False,
    },
    None: False,
}
DR_YESNO_ABBR_PRE_IGNORE = {
    'ce': {
        'iol': True,
        None: False,
    },
    'ceiol/': True,
    'f/u': True,
    'last': {
        'exam': True,
        None: False,
    },
    'per': True,
    'recent': {
        'dfe': {
            'w/': True,
            None: False,
        },
        None: False
    },
    'refer': True,
    'referred': {
        'by': True,
        None: False,
    },
    'return': True,
    'sees': True,
    None: False,
}
DR_YESNO_ABBR_POST_IGNORE = {
    'redo': True,
    'to': {
        'review': True,
        None: False,
    },
    None: False,
}


def filter_dr_yesno_context(match: re.Match, text: str, pat_label: str = None):
    if has_before(match if isinstance(match, int) else match.start(),
                  text,
                  terms=DR_YESNO_PRE_IGNORE,
                  word_window=3,
                  boundary_chars='¶'):
        return True
    elif has_after(match if isinstance(match, int) else match.start(),
                   text,
                   terms=DR_YESNO_POST_IGNORE,
                   word_window=8):
        return True
    if pat_label is 'DR_YESNO_ABBR_PAT':
        if has_before(match if isinstance(match, int) else match.start(),
                      text,
                      terms=DR_YESNO_ABBR_PRE_IGNORE,
                      word_window=4,
                      boundary_chars='¶'):
            return True
        if has_after(match if isinstance(match, int) else match.start(),
                     text,
                     terms=DR_YESNO_ABBR_POST_IGNORE,
                     word_window=4,
                     boundary_chars='¶'):
            return True
    return False


def get_dr_yesno(text: str, *, headers=None, lateralities=None) -> list:
    data = []
    # Extract matches from sections / headers.
    if headers:
        pass
    # Extract matches from full text.
    if not lateralities:
        lateralities = build_laterality_table(text, search_negated_list=True)
    for new_var in _get_dr_yesno(text, lateralities, 'ALL'):
        data.append(new_var)
    return data


def _get_dr_yesno(text: str, lateralities, source: str) -> dict:
    for pat_label, pat, variable in [
        ('DR_YESNO_NEG_PAT', DR_YESNO_NEG_PAT, 'diab_retinop_yesno'),
        ('DR_YESNO_PAT', DR_YESNO_PAT, 'diab_retinop_yesno'),
        ('DR_YESNO_ABBR_PAT', DR_YESNO_ABBR_PAT, 'diab_retinop_yesno'),
    ]:
        for m in pat.finditer(text):
            if filter_dr_yesno_context(m, text, pat_label=pat_label):
                continue
            if pat_label is 'DR_YESNO_NEG_PAT':
                yield create_new_variable(text, m, lateralities, variable, {
                    'value': 0,
                    'term': m.group(),
                    'label': 'No',
                    'negated': None,
                    'regex': pat_label,
                    'source': source,
                })
            else:
                negated = (
                    is_negated(m, text, word_window=4, boundary_chars=':¶)')
                    or is_post_negated(m, text,
                                       terms={'no'},
                                       word_window=1,
                                       boundary_chars=';¶',
                                       skip_n_boundary_chars=0)
                )
                yield create_new_variable(text, m, lateralities, variable, {
                    'value': 0 if negated else 1,
                    'term': m.group(),
                    'label': 'No' if negated else 'Yes',
                    'negated': negated,
                    'regex': pat_label,
                    'source': source,
                })
