import re

sphere = r'([+-]\d+\.\d+|pla?n?o?)'
cylinder = r'[+-]\d+\.\d+'
axis = r'\d+'
denom = r'\d+'
ncorr = r'[+-]\d+(?:\.\d+)?'
add = r'\d+(?:\.\d+)?'
right_eye = r'(?:O\.?D\.?|R\.E?\.?):?'
left_eye = r'(?:O\.?S\.?|L\.E?\.?):?'

bva = r'(BVA|best correct vision)'


def vision_20(denominator_label, ncorrect_label):
    return rf'(?:20/\s*(?P<{denominator_label}>{denom})\s*(?P<{ncorrect_label}>{ncorr})?\s*)'


def prescript(sphere_label, cylinder_label, axis_label):
    return rf'(?P<{sphere_label}>{sphere})\W*(?P<{cylinder_label}>{cylinder})\W*x\W*(?P<{axis_label}>{axis})'


def add_power(add_label):
    return rf'(?:add(?:\W*power)?\W*(?P<{add_label}>{add})\W*)?'


MANIFEST_PAT = re.compile(
    rf'(?:(MANIFEST\W*)?REFRACTION)\W*(manifest\W*)?'
    rf'{right_eye}\W*{prescript("od_sphere", "od_cylinder", "od_axis")}\W*'
    rf'(?:(reading|nv)\W*{right_eye}\W*{prescript("od_sphere_nv", "od_cylinder_nv", "od_axis_nv")}\W*)?'
    rf'{vision_20("od_denominator", "od_correct")}?'
    rf'{add_power("od_add")}'
    rf'(?:{bva}\W*{vision_20("od_denominator_2", "od_correct_2")})?'
    rf'{left_eye}\W*{prescript("os_sphere", "os_cylinder", "os_axis")}\W*'
    rf'(?:(reading|nv)\W*{left_eye}\W*{prescript("os_sphere_nv", "os_cylinder_nv", "os_axis_nv")}\W*)?'
    rf'{vision_20("os_denominator", "os_correct")}?'
    rf'{add_power("os_add")}'
    rf'(?:{bva}\W*{vision_20("os_denominator_2", "os_correct_2")}?)?',
    re.I
)

RX_PAT = re.compile(
    r'(?:above refaction)\W*(?P<numerator>20|3E|E)/\s*(?P<score>\d+)\s*(?P<sign>[+|-])*\s*(?P<diopter>\d)*'
)

BCV_PAT = re.compile(
    r'(?:best correct vision)\W*'
    r'(?:O\.?D\.?|R\.?E?\.?):?\W*'
    r'(?:20/\s*(?P<od_denominator>\d+)\s*(?P<od_correct>[+-]\d+(?:\.\d+)?)?\W*)'
    r'(?:O\.?S\.?|L\.?E?\.?):?\W*'
    r'(?:20/\s*(?P<os_denominator>\d+)\s*(?P<os_correct>[+-]\d+(?:\.\d+)?)?\W*)',
    re.I
)


def get_manifest_rx(text):
    data = {}
    for m in MANIFEST_PAT.finditer(text):
        d = m.groupdict()
        data['manifestrx_sphere_re'] = 0.0 if d['od_sphere'].startswith('pl') else float(d['od_sphere'])
        data['manifestrx_cylinder_re'] = float(d['od_cylinder'])
        data['manifestrx_axis_re'] = float(d['od_axis'])
        data['manifestrx_add_re'] = float(d.get('od_add', 0.0) or 0.0)
        data['manifestrx_denom_re'] = float(
            d.get('od_denominator', 0.0)
            or d.get('od_denominator_2', 0.0)
            or 0.0
        )
        data['manifestrx_ncorr_re'] = float(
            d.get('od_correct', 0.0)
            or d.get('od_correct_2', 0.0)
            or 0.0
        )
        data['manifestrx_sphere_le'] = 0.0 if d['os_sphere'].startswith('pl') else float(d['os_sphere'])
        data['manifestrx_cylinder_le'] = float(d['os_cylinder'])
        data['manifestrx_axis_le'] = float(d['os_axis'])
        data['manifestrx_add_le'] = float(d.get('os_add', 0.0) or 0.0)
        data['manifestrx_denom_le'] = float(
            d.get('os_denominator', 0.0)
            or d.get('os_denominator_2', 0.0)
            or 0.0
        )
        data['manifestrx_ncorr_le'] = float(
            d.get('os_correct', 0.0)
            or d.get('os_correct_2', 0.0)
            or 0.0
        )
    return data
