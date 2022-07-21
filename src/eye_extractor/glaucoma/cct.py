"""
Central corneal thickness (CCT)    
    RE    centralcornealthickness_re    Integer    550, 553, 560, etc. Range ~500-700    Glaucoma/ only check once
    LE    centralcornealthickness_le    Integer    550, 553, 560, etc. Range ~500-700    Glaucoma/ only check once
"""
import re

from eye_extractor.laterality import build_laterality_table, od_pattern, os_pattern, ou_pattern

cct = r'\d{3}'

CCT_OD_OS_PAT = re.compile(
    rf'\b(?:'
    rf'(?:{od_pattern})?\W*(?P<od>{cct})\W*(?:{od_pattern})?\W+'
    rf'(?:{os_pattern})?\W*(?P<os>{cct})\W*(?:{os_pattern})?'
    rf')\b',
    re.I
)

CCT_OD_PAT = re.compile(
    rf'\b(?:'
    rf'(?:{od_pattern})\W*(?P<od1>{cct})'
    rf'|'
    rf'(?P<od2>{cct})\W*(?:{od_pattern})'
    rf')\b',
    re.I
)

CCT_OS_PAT = re.compile(
    rf'\b(?:'
    rf'(?:{os_pattern})\W*(?P<os1>{cct})'
    rf'|'
    rf'(?P<os2>{cct})\W*(?:{os_pattern})'
    rf')\b',
    re.I
)

CCT_OU_PAT = re.compile(
    rf'\b(?:'
    rf'(?:{ou_pattern})\W*(?P<ou1>{cct})'
    rf'|'
    rf'(?P<ou2>{cct})\W*(?:{ou_pattern})'
    rf')\b',
    re.I
)

CCT_PAT = re.compile(
    rf'\b(?:'
    rf'{cct}'
    rf')\b',
    re.I
)

CCT_SECTION_PAT = re.compile(
    rf'\b(?:'
    rf'pachymetry|cct'
    rf')'
)


def search_cct(text, sect_name):
    if m := CCT_OD_OS_PAT.search(text):
        return {
            'centralcornealthickness_re': {
                'value': int(m.group('od')),
                'term': m.group(),
                'regex': 'CCT_OD_OS_PAT',
                'source': sect_name,
            }, 'centralcornealthickness_le': {
                'value': int(m.group('os')),
                'term': m.group(),
                'regex': 'CCT_OD_OS_PAT',
                'source': sect_name,
            }}
    elif m := CCT_OU_PAT.search(text):
        entry = {
            'value': int(m.group('ou1') or m.group('ou2')),
            'term': m.group(),
            'regex': 'CCT_OU_PAT',
            'source': sect_name,
        }
        return {'centralcornealthickness_re': entry, 'centralcornealthickness_le': entry}
    elif m := CCT_OD_PAT.search(text):
        entry = {
            'value': int(m.group('od1') or m.group('od2')),
            'term': m.group(),
            'regex': 'CCT_OD_PAT',
            'source': sect_name,
        }
        return {'centralcornealthickness_re': entry}
    elif m := CCT_OS_PAT.search(text):
        entry = {
            'value': int(m.group('os1') or m.group('os2')),
            'term': m.group(),
            'regex': 'CCT_OS_PAT',
            'source': sect_name,
        }
        return {'centralcornealthickness_le': entry}
    elif m := CCT_PAT.search(text):
        entry = {
            'value': int(m.group()),
            'term': m.group(),
            'regex': 'CCT_PAT',
            'source': sect_name,
        }
        return {'centralcornealthickness_re': entry, 'centralcornealthickness_le': entry}


def extract_cct(text, *, headers=None, lateralities=None):
    """
    Extract open/closed result of gonioscopy
    :param text:
    :param headers:
    :param lateralities:
    :return:
    """
    lateralities = lateralities or build_laterality_table(text)
    data = []

    if headers:
        for sect_name in ['PACHYMETRY', 'CCT']:
            if section_text := headers.get(sect_name, None):
                if res := search_cct(section_text, sect_name):
                    data.append(res)
    for m in CCT_SECTION_PAT.finditer(text):
        if res := search_cct(text[m.end(): m.end() + 20], 'ALL'):
            data.append(res)
    return data
