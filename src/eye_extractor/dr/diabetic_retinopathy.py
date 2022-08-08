import enum
import re

from eye_extractor.common.negation import is_negated, is_post_negated
from eye_extractor.laterality import build_laterality_table, create_new_variable


class HemorrhageType(enum.IntEnum):
    UNKNOWN = 0
    NONE = 1
    INTRARETINAL = 2
    DOT_BLOT = 3
    PRERETINAL = 4
    VITREOUS = 5
    SUBRETINAL = 6


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
    ('venbeading', re.compile(
            r'\b('
            r'venous beadings?|vbs?'
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
    ('irma', re.compile(
        r'\b('
        r'irma|intraretinal microvascular abnormality'
        r')\b',
        re.I
    )),
    ('fluid_dr', re.compile(
        r'\b('
        r'dr|irf|srf|fluid'
        r')\b',
        re.I
    )),
    ('dr_laser_scars', re.compile(
        r'\b('
        r'laser scars?'
        r')\b',
        re.I
    )),
    ('dr_laser_scar_type', re.compile(
        r'\b('
        r'(pan\W?retinal|focal|grid|macula)(\W*\w+){0,3}\W*(laser\W*)?scars'
        r'|(laser\W*)?scars(\W*\w+){0,3}\W*(pan\W?retinal|focal|grid|macula)'
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
    ('diabretinop_type', re.compile(
        r'\b('
        r'npdr|nonproliferative diabetic retinopathy|PDR|proliferative diabetic retinopathy'
        r')\b',
        re.I
    )),
    ('nonprolifdr', re.compile(
        r'\b('
        r'(No|mild|moderate|severe|very severe)\W*'
        r'(NPDR|background diabetic retinopathy|BDR|non\W?proliferative DR)'
        r')\b',
        re.I
    )),
    ('prolifdr', re.compile(
        r'\b('
        r'(No|mild|moderate|severe|very severe)\W*'
        r'(PDR|proliferative diabetic retinopathy|proliferative DR)'
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
    ('dmacedema_tx', re.compile(
        r'\b('
        r'focal laser|grid laser|laser focal|laser grid|intravitreal Injections?|anti-VEGF|PDT|photodynamic therapy'
        r')\b',
        re.I
    )),
    ('dmacedema_antivegf', re.compile(
        r'\b('
        r'anti-VEGF|intravitreal anti-VEG|bevacizumab|ranibizumab|aflibercept|triamcinolone'
        r')\b',
        re.I
    )),
]

INTRARETINAL_PAT = re.compile(
        r'\b('
        r'intraretinal\s*hemorrhage'
        r'|hemorrhage\s*intraretinal'
        r')\b'
    )
DOT_BLOT_PAT = re.compile(
        r'\b('
        r'dot blot\s*hemorrhage'
        r'|hemorrhage\s*dot blot'
        r')\b'
    )
PRERETINAL_PAT = re.compile(
        r'\b('
        r'preretinal\s*hemorrhage'
        r'|hemorrhage\s*preretinal'
        r')\b'
    )
VITREOUS_PAT = re.compile(
        r'\b('
        r'vitreous\s*hemorrhage'
        r'|hemorrhage\s*vitreous'
        r')\b'
    )
SUBRETINAL_PAT = re.compile(
        r'\b('
        r'subretinal\s*hemorrhage'
        r'|hemorrhage\s*subretinal'
        r')\b'
    )


# TODO: Perform conditional variable creation for non-binary values
def get_dr_binary(text, *, headers=None, lateralities=None):
    if not lateralities:
        lateralities = build_laterality_table(text)
    data = []
    for variable, PAT in DIABETIC_RETINOPATHY_PATS:
        for m in PAT.finditer(text):
            negword = is_negated(m, text, {'no', 'or', 'neg', 'without'}, word_window=4)
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


def get_hemorrhage_type(text, *, headers=None, lateralities=None):
    if not lateralities:
        lateralities = build_laterality_table(text)
    data = []
    for pat, hemtype, hemlabel in [
        (INTRARETINAL_PAT, HemorrhageType.INTRARETINAL, 'intraretinal'),
        (DOT_BLOT_PAT, HemorrhageType.DOT_BLOT, 'dot blot'),
        (PRERETINAL_PAT, HemorrhageType.PRERETINAL, 'preretinal'),
        (VITREOUS_PAT, HemorrhageType.VITREOUS, 'vitreous'),
        (SUBRETINAL_PAT, HemorrhageType.SUBRETINAL, 'subretinal'),
    ]:
        for m in pat.finditer(text):
            negword = is_negated(m, text, {'no', 'or', 'neg', 'without'}, word_window=3)
            data.append(
                create_new_variable(text, m, lateralities, 'hemorrhage_typ_dr', {
                    'value': HemorrhageType.NONE if negword else hemtype,
                    'term': m.group(),
                    'label': f'No {hemlabel} hemorrhage' if negword else f'{hemlabel} hemorrhage',
                    'negated': negword,
                    'regex': f'{hemlabel}_PAT',
                    'source': 'ALL',
                })
            )
    if headers:
        pass
    return data


def extract_dr_variables(text: str, *, headers=None, lateralities=None) -> dict:
    return {
        'dr': get_dr_binary(text, headers=headers, lateralities=lateralities),
        'hemorrhage_type': get_hemorrhage_type(text, headers=headers, lateralities=lateralities)
    }
