import re

NPDR_PAT = re.compile(
    r'\b('
    r'npdr|non(-)?proliferative diabetic retinopathy'
    r')\b',
    re.I
)
PDR_PAT = re.compile(
    r'\b('
    r'pdr|proliferative diabetic retinopathy'
    r')\b',
    re.I
)
