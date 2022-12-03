import re

from eye_extractor.nlp.negate.negation import is_negated, is_post_negated
from eye_extractor.laterality import build_laterality_table, create_new_variable


NVA_PAT = re.compile(
        r'\b('
        r'(angular\s+)neovascularization\s+of(\s+the)?\s+angle'
        r'|nva(?!\W+\d.\d{2}\W*m)(?!\W+\d{2}/\d{2})'
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
            yield create_new_variable(text, m, lateralities, variable, {
                    'value': 0 if negated else 1,
                    'term': m.group(),
                    'label': 'no' if negated else 'yes',
                    'negated': negated,
                    'regex': f'{variable}_PAT',
                    'source': 'ALL'
            })