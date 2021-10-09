import re

MANIFEST_PAT = re.compile(
    r'(?:(MANIFEST\W*)?REFRACTION)\W*(manifest\W*)?'
    r'(?:O\.?D\.?|R\.E?\.?):?\W*(?P<od_sphere>[+-]\d+\.\d+|pl)\W*(?P<od_cylinder>[+-]\d+\.\d+)\W*x\W*(?P<od_axis>\d+)\W*'
    r'(?:(reading|nv)\W*(?:O\.?D\.?|R\.E?\.?):?\W*(?P<od_sphere_nv>[+-]\d+\.\d+|pl)\W*(?P<od_cylinder_nv>[+-]\d+\.\d+)\W*x\W*(?P<od_axis_nv>\d+)\W*)?'
    r'(?:20/\s*(?P<od_denominator>\d+)\s*(?P<od_correct>[+-]\d+(?:\.\d+)?)?\s*)?'
    r'(?:add(?:\W*power)?\W*(?P<od_add>\d+(?:\.\d+)?))?'
    r'(?:O\.?S\.?|L\.?E?\.?):?\W*(?P<os_sphere>[+-]\d+\.\d+|pl)\W*(?P<os_cylinder>[+-]\d+\.\d+)\W*x\W*(?P<os_axis>\d+)\W*'
    r'(?:(reading|nv)\W*(?:O\.?S\.?|L\.E?\.?):?\W*(?P<os_sphere_nv>[+-]\d+\.\d+|pl)\W*(?P<os_cylinder_nv>[+-]\d+\.\d+)\W*x\W*(?P<os_axis_nv>\d+)\W*)?'
    r'(?:20/\s*(?P<os_denominator>\d+)\s*(?P<os_correct>[+-]\d+(?:\.\d+)?)\W*)?'
    r'(?:add(?:\W*power)?\W*(?P<os_add>[+-]?\d+(?:\.\d+)?))?',
    re.I
)

RX_PAT = re.compile(
    r'(?:above refaction)\W*(?P<numerator>20|3E|E)/\s*(?P<score>\d+)\s*(?P<sign>[+|-])*\s*(?P<diopter>\d)*'
)


def get_manifest_rx(text):
    data = {}
    for m in MANIFEST_PAT.finditer(text):
        d = m.groupdict()
        data['manifestrx_sphere_re'] = 0.0 if d['od_sphere'] == 'pl' else float(d['od_sphere'])
        data['manifestrx_cylinder_re'] = float(d['od_cylinder'])
        data['manifestrx_axis_re'] = float(d['od_axis'])
        data['manifestrx_add_re'] = float(d.get('od_add', 0.0) or 0.0)
        data['manifestrx_denom_re'] = float(d.get('od_denominator', 0.0) or 0.0)
        data['manifestrx_ncorr_re'] = float(d.get('od_correct', 0.0) or 0.0)
        data['manifestrx_sphere_le'] = 0.0 if d['os_sphere'] == 'pl' else float(d['os_sphere'])
        data['manifestrx_cylinder_le'] = float(d['os_cylinder'])
        data['manifestrx_axis_le'] = float(d['os_axis'])
        data['manifestrx_add_le'] = float(d.get('os_add', 0.0) or 0.0)
        data['manifestrx_denom_le'] = float(d.get('os_denominator', 0.0) or 0.0)
        data['manifestrx_ncorr_le'] = float(d.get('os_correct', 0.0) or 0.0)
    return data
