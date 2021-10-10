sphere = r'([+-]\d+\.\d+|pla?n?o?)'
cylinder = r'[+-]\d+\.\d+'
axis = r'\d+'
denom = r'\d+'
ncorr = r'[+-]\d+(?:\.\d+)?'
add = r'\d+(?:\.\d+)?'
right_eye = r'(?:O\.?D\.?|R\.?E?\.?):?'
left_eye = r'(?:O\.?S\.?|L\.?E?\.?):?'
bva = r'(BVA|best correct vision)'


def vision_20(denominator_label, ncorrect_label):
    return rf'(?:20/\s*(?P<{denominator_label}>{denom})\s*(?P<{ncorrect_label}>{ncorr})?\s*)'


def prescript(sphere_label, cylinder_label, axis_label):
    return rf'(?P<{sphere_label}>{sphere})\W*(?P<{cylinder_label}>{cylinder})\W*x\W*(?P<{axis_label}>{axis})'


def add_power(add_label):
    return rf'(?:add(?:\W*power)?\W*(?P<{add_label}>{add})\W*)?'