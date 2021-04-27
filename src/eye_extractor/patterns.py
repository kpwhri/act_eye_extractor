import re

CATARACT_PAT = re.compile(r'(cataracts?)', re.I)

AMD_PAT = re.compile(r'(macular degeneration|\bamd\b)', re.I)

DIABETES_PAT = re.compile(r'(diabetes)', re.I)

CANCER_PAT = re.compile(r'(cancer)', re.I)
HYPERTENSION_PAT = re.compile(r'(hypertension)', re.I)
RH_ARTHRITIS_PAT = re.compile(r'(rheumatoid arthritis)', re.I)
ARTHRITIS_PAT = re.compile(r'(?<!rheumatoid )(arthritis)', re.I)
RESPIRATORY_PAT = re.compile(r'(respiratory)', re.I)
MUSCLES_PAT = re.compile(r'(muscles,joints)', re.I)
SKIN_PAT = re.compile(r'(skin problems)', re.I)
KIDNEY_PAT = re.compile(r'(urinary,kidney)', re.I)
GLAUCOMA_PAT = re.compile(r'(glaucoma)', re.I)
THYROID_PAT = re.compile(r'(thyroid)', re.I)
CARDIO_PAT = re.compile(r'(cardio)', re.I)
RETINAL_DETACHMENT_PAT = re.compile(r'(retinal detachment)', re.I)
BLINDNESS_PAT = re.compile(r'(blindness)', re.I)
OTHER_PAT = re.compile(r'(other)', re.I)
PSEUDOPHAKIA_PAT = re.compile(r'(pseudophaki[ac])', re.I)
DIABETIC_RP_PAT = re.compile(r'diabetic\s*(retinopathy|r\Wt)', re.I)

YES_PAT = re.compile(r'\b(yes|y)\b', re.I)
NO_PAT = re.compile(r'\b(not?|n|none)\b', re.I)

PATTERN_BATTERY = [
    ('diabetes', DIABETES_PAT),
    ('cancer', CANCER_PAT),
    ('cataract', CATARACT_PAT),
    ('amd', AMD_PAT),
    ('hypertension', HYPERTENSION_PAT),
    ('rh_arthritis', RH_ARTHRITIS_PAT),
    ('arthritis', ARTHRITIS_PAT),
    ('respiratory', RESPIRATORY_PAT),
    ('muscles', MUSCLES_PAT),
    ('skin', SKIN_PAT),
    ('kidney', KIDNEY_PAT),
    ('glaucoma', GLAUCOMA_PAT),
    ('pseudophakia', PSEUDOPHAKIA_PAT),
    ('diabetic retinopathy', DIABETIC_RP_PAT),
    ('other', OTHER_PAT),
]

PATTERN_RESPONSE = [
    ('yes', YES_PAT),
    ('no', NO_PAT),
]
