import re

from eye_extractor.common.negation import is_negated, is_post_negated
from eye_extractor.laterality import build_laterality_table, create_new_variable


DIABETIC_RETINOPATHY_PATS = [
    ('diab_retinop_yesno', re.compile(
        r'\b('
        r'diabetic retinopathy|dr|npdr'
        r')\b',
        re.I
    )),
    ('ret_microaneurysm', re.compile(
        r'\b('
        r'mas?|retinal mas?|retinal micro\W?aneurisms?'
        r')\b',
        re.I
    )),
    ('cottonwspot', re.compile(
        r'\b('
        r'cotton\W?wool\W?spots?|cwss?|cws?'
        r')\b',
        re.I
    )),
    ('hardexudates', re.compile(
        r'\b('
        r'hard exudates?|he|lipid'
        r')\b',
        re.I
    )),
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
    ('neovasc_yesno', re.compile(
        r'\b('
        r'NV|Neovascularization|neovascularization of( the)? angle|neovascularization'
        r'|neovascularization of (the )?disc|neovascularization of the optic disc'
        r'|NVA|NVI|NVD|NVE'
        r')\b',
        re.I
    )),
    ('nva_yesno', re.compile(
        r'\b('
        r'neovascularization of( the)? angle|nva|angular neovascularization'
        r')\b',
        re.I
    )),
    ('nvi_yesno', re.compile(
        r'\b('
        r'nvi|neovascularization of( the)? iris|rubeosis|rubeosis iridis'
        r')\b',
        re.I
    )),
    ('nvd_yesno', re.compile(
        r'\b('
        r'nvd|neovascularization of (the )?disc|neovascularization of (the )?optic(al)? disc'
        r')\b',
        re.I
    )),
    ('nve_yesno', re.compile(
        r'\b('
        r'nve|neovascularization elsewhere'
        r')\b',
        re.I
    )),
    ('drtreatment', re.compile(
        r'\b('
        r'PRP|pan retinal photocoagulation|Pars plana vitrectomy'
        r')\b',
        re.I
    )),
    ('dmacedema_yesno', re.compile(
        r'\b('
        r'DME|diabetic macular edema'
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
