import re

from eye_extractor.common.negation import is_negated
from eye_extractor.laterality import build_laterality_table, create_new_variable

DIABETIC_RETINOPATHY_PATS = [
    ('diabetic_retinopathy', re.compile(
        r'\b('
        r'diabetic retinopathy|dr|npdr'
        r')\b',
        re.I
    )),
    ('retinal_microaneurism', re.compile(
        r'\b('
        r'mas?|retinal mas?|retinal micro\W?aneurisms?'
        r')\b',
        re.I
    )),
    ('cotton_wool_spot', re.compile(
        r'\b('
        r'cotton\W?wool\W?spots?|cwss?'
        r')\b',
        re.I
    )),
    ('hard_exudates', re.compile(
        r'\b('
        r'hard exudates?|he|lipid'
        r')\b',
        re.I
    )),
    ('venous_beading', re.compile(
        r'\b('
        r'venous beadings?|vbs?'
        r')\b',
        re.I
    )),
    ('disc_edema', re.compile(
        r'\b('
        r'disc edema'
        r')\b',
        re.I
    )),
    ('hemorrhage', re.compile(
        r'\b('
        r'hemorrhage'
        r')\b',
        re.I
    )),
    ('hemorrhage_type', re.compile(
        r'\b('
        r'(intraretinal|dot blot|preretinal|vitreous|subretinal) hemorrhage'
        r'|hemorrhage (intraretinal|dot blot|preretinal|vitreous|subretinal)'
        r')\b',
        re.I
    )),
    ('hemorrhage_type', re.compile(
        r'\b('
        r'(intraretinal|dot blot|preretinal|vitreous|subretinal) hemorrhage'
        r'|hemorrhage (intraretinal|dot blot|preretinal|vitreous|subretinal)'
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
    ('laser_scars', re.compile(
        r'\b('
        r'laser scars?'
        r')\b',
        re.I
    )),
    ('laser_scars_type', re.compile(
        r'\b('
        r'(pan\W?retinal|focal|grid|macula)(\W*\w+){0,3}\W*(laser\W*)?scars'
        r'|(laser\W*)?scars(\W*\w+){0,3}\W*(pan\W?retinal|focal|grid|macula)'
        r')\b',
        re.I
    )),
    ('laser_panretinal_scars', re.compile(
        r'\b('
        r'prp|laser panretinal photo\W?coagulation|scatter photo\W?coagulation'
        r')\b',
        re.I
    )),
    ('neovascularization', re.compile(
        r'\b('
        r'NV|Neovascularization|neovascularization of( the)? angle|neovascularization'
        r'|neovascularization of (the )?disc|neovascularization of the optic disc'
        r'|NVA|NVI|NVD|NVE'
        r')\b',
        re.I
    )),
    ('neovascularization', re.compile(
        r'\b('
        r'NV|Neovascularization|neovascularization of( the)? angle|neovascularization'
        r'|neovascularization of (the )?disc|neovascularization of the optic disc'
        r'|NVA|NVI|NVD|NVE'
        r')\b',
        re.I
    )),
    ('nva', re.compile(
        r'\b('
        r'neovascularization of( the)? angle|nva|angular neovascularization'
        r')\b',
        re.I
    )),
    ('nvi', re.compile(
        r'\b('
        r'nvi|neovascularization of( the)? iris|rubeosis|rubeosis iridis'
        r')\b',
        re.I
    )),
    ('nvd', re.compile(
        r'\b('
        r'nvd|neovascularization of (the )?disc|neovascularization of (the )?optic(al)? disc'
        r')\b',
        re.I
    )),
    ('nve', re.compile(
        r'\b('
        r'nve|neovascularization elsewhere'
        r')\b',
        re.I
    )),
    ('dr_type', re.compile(
        r'\b('
        r'npdr|nonproliferative diabetic retinopathy|PDR|proliferative diabetic retinopathy'
        r')\b',
        re.I
    )),
    ('npdr_severity', re.compile(
        r'\b('
        r'(No|mild|moderate|severe|very severe)\W*'
        r'(NPDR|background diabetic retinopathy|BDR|non\W?proliferative DR)'
        r')\b',
        re.I
    )),
    ('pdr_severity', re.compile(
        r'\b('
        r'(No|mild|moderate|severe|very severe)\W*'
        r'(PDR|proliferative diabetic retinopathy|proliferative DR)'
        r')\b',
        re.I
    )),
    ('dr_treatment', re.compile(
        r'\b('
        r'PRP|pan retinal photocoagulation|Pars plana vitrectomy'
        r')\b',
        re.I
    )),
    ('dr_edema', re.compile(
        r'\b('
        r'DME|diabetic macular edema'
        r')\b',
        re.I
    )),
    ('dr_edema_significant', re.compile(
        r'\b('
        r'CSME|clinically significant (diabetic )?macular edema'
        r')\b',
        re.I
    )),
    ('oct_cmt', re.compile(
        r'\b('
        r'CMT|central macular thickness|macular thickness|thickness of macula'
        r')\b',
        re.I
    )),
    ('edema_tx', re.compile(
        r'\b('
        r'focal laser|grid laser|laser focal|laser grid|intravitreal Injections?|anti-VEGF|PDT|photodynamic therapy'
        r')\b',
        re.I
    )),
    ('antivegf', re.compile(
        r'\b('
        r'anti-VEGF|intravitreal anti-VEG|bevacizumab|ranibizumab|aflibercept|triamcinolone'
        r')\b',
        re.I
    )),
]


def get_dr(text, *, headers=None, lateralities=None):
    if not lateralities:
        lateralities = build_laterality_table(text)
    data = []
    for variable, PAT in DIABETIC_RETINOPATHY_PATS:
        for m in PAT.finditer(text):
            negword = is_negated(m, text, {'no', 'or'})
            data.append(
                create_new_variable(text, m, lateralities, variable, {
                    'value': 0 if negword else 1,
                    'term': m.group(),
                    'label': 'no' if negword else 'yes',
                    'negated': negword,
                    'regex': f'{variable}_PAT',
                    'source': 'ALL',
                })
            )
    if headers:
        pass
    return data


def extract_dr_variables(text: str, *, headers=None, lateralities=None) -> dict:
    return {
        'dr': get_dr(text, headers=headers, lateralities=lateralities)
    }


# import pathlib
#
# path = pathlib.Path(r'G:\CTRHS\ACT_Eye\PROGRAMMING\NLP\corpus\corpus_20210326_train')
#
# num_files = 0
# for i, file in enumerate(path.iterdir()):
#     name, extension = file.name.split(".")
#     if extension == "txt":
#         num_files += 1
#
# print(num_files)