import re

from eye_extractor.common.get_variable import get_variable
from eye_extractor.nlp.negate.negation import is_negated, is_post_negated, has_after
from eye_extractor.laterality import build_laterality_table, create_new_variable

NV_PAT = re.compile(
    r'\b('
    r'neovascularization'
    r'\b)',
    re.I
)
NVA_PAT = re.compile(
    r'\b('
    r'(angular\s+)neovascularization\s+of(\s+the)?\s+angle'
    r'|nva'
    r'(?!\W+\d.\d{2}\W*m)'
    r'(?!\W+\d.\d{2}/\d.\d{2})'  # near visual acuity - ex: 'NVA 0.30/0.43 M'
    r'(?!\W+\d{2}/\d{2})'  # near visual acuity - ex: 20/20
    r'(?!\W+rs\d{2})'  # near visual acuity - RS
    r')\b',
    re.I
)
NVI_PAT = re.compile(
    r'\b('
    r'nvi|neovascularization of( the)? iris|rubeosis|rubeosis iridis'
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


# TODO: Merge `get_neovasc` and `get_nv_types` into one function.
def get_neovasc(text: str, *, headers=None, lateralities=None) -> list:
    return get_variable(text, _get_neovasc, headers=headers, lateralities=lateralities)


def _get_neovasc(text: str, lateralities, source: str) -> dict:
    for pat_label, pat in [
        ('NV_PAT', NV_PAT),
        ('NVA_PAT', NVA_PAT),
        ('NVI_PAT', NVI_PAT),
        ('NVD_PAT', NVD_PAT),
        ('NVE_PAT', NVE_PAT),
    ]:
        for m in pat.finditer(text):
            negated = (
                is_negated(m, text, word_window=4)
                or is_negated(m, text, terms={'no'}, word_window=8)
                or is_post_negated(m, text, terms={'normal', 'neg', 'deferred', 'no', 'nc'}, word_window=2)
            )
            if has_after(m if isinstance(m, int) else m.start(),
                         text,
                         terms={'decreased'},
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


def get_nv_types(text: str, *, headers=None, lateralities=None) -> list:
    if not lateralities:
        lateralities = build_laterality_table(text)
    data = []
    for new_var in _get_nv_types(text, lateralities):
        data.append(new_var)
    if headers:
        pass

    return data


def _get_nv_types(text: str, lateralities):
    for pat_label, pat, variable in [
        ('NVA_PAT', NVA_PAT, 'nva_yesno'),
        ('NVI_PAT', NVI_PAT, 'nvi_yesno'),
        ('NVD_PAT', NVD_PAT, 'nvd_yesno'),
        ('NVE_PAT', NVE_PAT, 'nve_yesno'),
    ]:
        for m in pat.finditer(text):
            negated = (
                is_negated(m, text, word_window=4)
                or is_negated(m, text, terms={'no'}, word_window=8)
                or is_post_negated(m, text, terms={'normal', 'neg', 'deferred', 'no', 'nc'}, word_window=2)
            )
            if has_after(m if isinstance(m, int) else m.start(),
                         text,
                         terms={'decreased'},
                         word_window=3):
                break
            yield create_new_variable(text, m, lateralities, variable, {
                'value': 0 if negated else 1,
                'term': m.group(),
                'label': 'no' if negated else 'yes',
                'negated': negated,
                'regex': pat_label,
                'source': 'ALL'
            })
