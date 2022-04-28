import re

# RAO, retinal artery occlusion, RvasO (retinal vascular occlusion - can be vein or artery),
# BRAO, Branch retinal artery occlusion, CRAO, Central retinal artery occlusion

RAO_PAT = re.compile(
    r'(?:'
    r'\b[cb]?rao\b'
    r'|\brvas[o0]\b'
    r'|(?:(?:branch|central)\W*)?retinal\W*(arter(y|ial)|vein(al)?)?\W*occlu\w+'
    r''
    r')',
    re.I
)
