import re

from eye_extractor.nlp.negate.negation import is_negated, is_post_negated
from eye_extractor.laterality import build_laterality_table, create_new_variable

DIABETIC_RETINOPATHY_PATS = [
    ('disc_edema_DR', re.compile(
        r'\b('
        r'disc edema'
        r')\b',
        re.I
    )),
    ('hemorrhage_dr', re.compile(
        r'\b('
        r'hemorrhage'
        r')\b',
        re.I
    )),
    ('dr_laser_scars', re.compile(
        r'\b('
        r'laser scars?'
        r')\b',
        re.I
    )),
    ('laserpanret_photocoag', re.compile(
        r'\b('
        r'prp|laser panretinal photo\W?coagulation|scatter photo\W?coagulation'
        r')\b',
        re.I
    )),
    ('drtreatment', re.compile(
        r'\b('
        r'PRP|pan retinal photocoagulation|Pars plana vitrectomy'
        r')\b',
        re.I
    )),
    ('dmacedema_clinsignif', re.compile(
        r'\b('
        r'CSME|clinically significant (diabetic )?macular edema'
        r')\b',
        re.I
    )),
    ('oct_centralmac', re.compile(
        r'\b('
        r'CMT|central macular thickness|macular thickness|thickness of macula'
        r')\b',
        re.I
    )),
]


def get_dr_binary(text, *, headers=None, lateralities=None):
    if not lateralities:
        lateralities = build_laterality_table(text)
    data = []
    for variable, PAT in DIABETIC_RETINOPATHY_PATS:
        for m in PAT.finditer(text):
            negword = is_negated(m, text, word_window=4)
            if not negword:
                negword = is_post_negated(m, text, {'or'}, word_window=2)
            data.append(
                create_new_variable(text, m, lateralities, variable, {
                    'value': 0 if negword else 1,
                    'term': m.group(),
                    'label': 'no' if negword else 'yes',
                    'negated': negword,
                    'regex': f'{variable}_PAT',
                    'source': 'ALL'
                })
            )
    if headers:
        pass
    return data
