import re

from eye_extractor.common.get_variable import get_variable
from eye_extractor.nlp.negate.negation import has_after, has_before, is_negated, is_post_negated
from eye_extractor.laterality import build_laterality_table, create_new_variable

# Patterns.
NV_PAT = re.compile(
    r'\b('
    r'neovascularization'
    r')\b',
    re.I
)
NVA_PAT = re.compile(
    r'\b('
    r'(?<!20/\*{3}\W)'  # near visual acuity - ex: 'RE: 20/*** NVA'
    r'(?<!20/\W)'  # near visual acuity - ex: 'OS: 20/\nNVA'
    r'(?<!20/\W{2})'  # near visual acuity - ex: 'OS: 20/\n\nNVA'
    r'(?<!20/\d{3}\W{2})'  # near visual acuity - ex: 'OS: 20/150\n\nNVA'
    r'(?<!\d{2}/\d{2}-\d\W)'  # near visual acuity - ex: '20/50-1\nNVA'
    r'(neovascularization\s+of(\s+the)?\s+angle'
    r'|nva)'
    r'(?!\W+\d.\d{2}\W*m)'
    r'(?!\W+\d.\d{2}/\d.\d{2})'  # near visual acuity - ex: 'NVA 0.30/0.43 M'
    r'(?!\W+\d{2}/\d{2})'  # near visual acuity - ex: 20/20
    r'(?!\W+rs\s?\d{2})'  # near visual acuity - RS
    r'(?!\W+o[dsu]\W+20/\d{2})'  # near visual acuity - ex: 'NVA OU: 20/20'
    r'(?!\W+\d\W+m)'  # near visual acuity - ex: 'NVA: < 3 M'
    r'(?!\W+cc\W+20/)'  # near visual acuity - ex: 'NVA cc: 20/3'
    r')\b',
    re.I
)
NVI_HEADER_PAT = re.compile(
    r'\b('
    r'iris\s+rubeosis:'
    r'|nvi\s+with\s+sle:'
    r')(\s|$)',
    re.I
)
NVI_PAT = re.compile(
    r'\b('
    r'nvi'
    r'|neovascularization of( the)? iris'
    r'|rubeosis'
    r'|rubeosis iridis'
    r')\b',
    re.I
)
NVD_PAT = re.compile(
    r'\b('
    r'nvz?d|neovascularization of (the )?disc|neovascularization of (the )?optic(al)? disc'
    r')\b',
    re.I
)
NVE_PAT = re.compile(
    r'\b('
    r'nvz?e|neovascularization elsewhere'
    r')\b',
    re.I
)

# Context FSAs.
NVA_PRE_IGNORE = {
    'change': {
        'in': True,
        None: False
    },
    'problem': {
        'tracking': True,
        None: False
    },
    'difficulty': {
        'with': True,
        None: False
    },
    'decrease': {
        'in': True,
        None: False
    },
    'trouble': {
        'with': True,
        'watching': {
            'television': True,
            None: False,
        },
        None: False,
    },
    'decreased': True,
    'dva': True,
    'not': {
        'seeing': {
            'as': {
                'well': {
                    'with': True,
                    None: False,
                },
                None: False,
            },
            None: False,
        },
        None: False
    },
    None: False,
}
NVA_POST_IGNORE = {
    'good': True,
    'dva': True,
    'decrease': True,
    'decrease/sm': True,
    'getting': {
        'worse': True,
        None: False,
    },
    None: False
}
NVI_PRE_IGNORE = {
    'will': {
        'follow': {
            'for': True,
            None: False,
        },
        None: False,
    },
    None: False,
}
NVI_POST_IGNORE = {
    'not': {
        'performed': True,
        None: False,
    },
    'nt': True,
    'n/a': True,
    None: False,
}


def get_nv_types(text: str, *, headers=None, lateralities=None) -> list:
    return get_variable(text, _get_nv_types, headers=headers, lateralities=lateralities)


def _get_nv_types(text: str, lateralities, source: str):
    for pat_label, pat, variable in [
        ('NV_PAT', NV_PAT, None),
        ('NVA_PAT', NVA_PAT, 'nva_yesno'),
        ('NVI_PAT', NVI_PAT, 'nvi_yesno'),
        ('NVD_PAT', NVD_PAT, 'nvd_yesno'),
        ('NVE_PAT', NVE_PAT, 'nve_yesno'),
    ]:
        for m in pat.finditer(text):
            negated = (
                is_negated(m, text, word_window=4)
                or is_negated(m, text, terms={'no'}, word_window=8)
                or is_post_negated(m, text,
                                   terms={'normal': True,
                                          'neg': True,
                                          'deferred': True,
                                          'no': True,
                                          'nc': True,
                                          'none': True,
                                          'n': True,
                                          'not': {
                                              'seen': True,
                                              None: False
                                          },
                                          'wnl': True,
                                          None: False},
                                   word_window=3)
            )
            if has_after(m if isinstance(m, int) else m.start(),
                         text,
                         terms={'decreased'},
                         word_window=3):
                break
            if pat_label is 'NVA_PAT':
                if has_before(m if isinstance(m, int) else m.start(),
                              text,
                              terms=NVA_PRE_IGNORE,
                              word_window=6):
                    continue
                elif has_after(m if isinstance(m, int) else m.start(),
                               text,
                               terms=NVA_POST_IGNORE,
                               word_window=4):  # `has_after` word_window includes current match
                    continue
            if pat_label is 'NVI_PAT':
                if has_before(m if isinstance(m, int) else m.start(),
                              text,
                              terms=NVI_PRE_IGNORE,
                              word_window=3):
                    continue
                if has_after(m if isinstance(m, int) else m.start(),
                             text,
                             terms=NVI_POST_IGNORE,
                             word_window=3):
                    continue
            yield create_new_variable(text, m, lateralities, 'neovasc_yesno', {
                'value': 0 if negated else 1,
                'term': m.group(),
                'label': 'no' if negated else 'yes',
                'negated': negated,
                'regex': pat_label,
                'source': source
            })
            if variable:
                yield create_new_variable(text, m, lateralities, variable, {
                    'value': 0 if negated else 1,
                    'term': m.group(),
                    'label': 'no' if negated else 'yes',
                    'negated': negated,
                    'regex': pat_label,
                    'source': source
                })
