"""
Central corneal thickness (CCT)    
    RE    centralcornealthickness_re    Integer    550, 553, 560, etc. Range ~500-700    Glaucoma/ only check once
    LE    centralcornealthickness_le    Integer    550, 553, 560, etc. Range ~500-700    Glaucoma/ only check once
"""
import re

from eye_extractor.laterality import od_pattern, os_pattern, ou_pattern
from eye_extractor.sections.document import Document
from eye_extractor.sections.patterns import SectionName

cct = r'\d{3}'
microns = r'(?:microns?)?'
sep = r'(?:and)?'
microns_sep = fr'{microns}\W*{sep}'

CCT_OD_OS_PAT = re.compile(
    rf'\b(?:'
    # OD 500; 500 os
    rf'(?:{od_pattern})\W*(?P<od1>{cct})\W*{microns_sep}\W+(?P<os1>{cct})\W*{microns}\W*(?:{os_pattern})'
    # OD 500; OS 500
    rf'|(?:{od_pattern})\W*(?P<od2>{cct})\W*{microns_sep}\W*(?:{os_pattern})\W*(?P<os2>{cct})'
    # 500 od; os 500
    rf'|(?P<od3>{cct})\W*{microns}\W*(?:{od_pattern})\W*{sep}\W*(?:{os_pattern})\W*(?P<os3>{cct})'
    # 500 od; 500 os
    rf'|(?P<od4>{cct})\W*{microns}\W*(?:{od_pattern})\W*{sep}\W*(?P<os4>{cct})\W*{microns}\W*(?:{os_pattern})'
    rf')\b',
    re.I
)
CCT_OS_OD_PAT = re.compile(
    rf'\b(?:'
    # OS 500; 500 od
    rf'(?:{os_pattern})\W*(?P<os1>{cct})\W*{microns_sep}\W+(?P<od1>{cct})\W*{microns}\W*(?:{od_pattern})'
    # OS 500; OD 500
    rf'|(?:{os_pattern})\W*(?P<os2>{cct})\W*{microns_sep}\W*(?:{od_pattern})\W*(?P<od2>{cct})'
    # 500 os; od 500
    rf'|(?P<os3>{cct})\W*{microns}\W*(?:{os_pattern})\W*{sep}\W*(?:{od_pattern})\W*(?P<od3>{cct})'
    # 500 os; 500 od
    rf'|(?P<os4>{cct})\W*{microns}\W*(?:{os_pattern})\W+{sep}\W*(?P<od4>{cct})\W*{microns}\W*(?:{od_pattern})'
    rf')\b',
    re.I
)

CCT_OD_OS_GEN_PAT = re.compile(
    rf'\b(?:'
    rf'(?:{od_pattern})?\W*(?P<od>{cct})\W*{microns}\W*(?:{od_pattern})?\W+{sep}\W*'
    rf'(?:{os_pattern})?\W*(?P<os>{cct})\W*{microns}\W*(?:{os_pattern})?'
    rf')\b',
    re.I
)

CCT_OD_PAT = re.compile(
    rf'\b(?:'
    rf'(?:{od_pattern})\W*(?P<od1>{cct})'
    rf'|'
    rf'(?P<od2>{cct})\W*{microns}\W*(?:{od_pattern})'
    rf')\b',
    re.I
)

CCT_OS_PAT = re.compile(
    rf'\b(?:'
    rf'(?:{os_pattern})\W*(?P<os1>{cct})'
    rf'|'
    rf'(?P<os2>{cct})\W*{microns}\W*(?:{os_pattern})'
    rf')\b',
    re.I
)

CCT_OU_PAT = re.compile(
    rf'\b(?:'
    rf'(?:{ou_pattern})\W*(?P<ou1>{cct})'
    rf'|'
    rf'(?P<ou2>{cct})\W*{microns}\W*(?:{ou_pattern})'
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
    rf'\b(?:pachymetry|cct)\b',
    re.I
)


def search_cct(text, sect_name):
    def get_od_os(match, pat):
        return {
            'centralcornealthickness_re': {
                'value': int(
                    match.group('od1') or match.group('od2') or match.group('od3') or match.group('od4')
                ),
                'term': match.group(),
                'regex': pat,
                'source': sect_name,
            }, 'centralcornealthickness_le': {
                'value': int(
                    match.group('os1') or match.group('os2') or match.group('os3') or match.group('os4')
                ),
                'term': match.group(),
                'regex': pat,
                'source': sect_name,
            }}

    if m := CCT_OD_OS_PAT.search(text):
        return get_od_os(m, 'CCT_OD_OS_PAT')
    elif m := CCT_OS_OD_PAT.search(text):
        return get_od_os(m, 'CCT_OS_OD_PAT')
    elif m := CCT_OD_OS_GEN_PAT.search(text):
        return {
            'centralcornealthickness_re': {
                'value': int(m.group('od')),
                'term': m.group(),
                'regex': 'CCT_OD_OS_GEN_PAT',
                'source': sect_name,
            }, 'centralcornealthickness_le': {
                'value': int(m.group('os')),
                'term': m.group(),
                'regex': 'CCT_OD_OS_GEN_PAT',
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


def extract_cct(doc: Document):
    """
    Extract open/closed result of gonioscopy
    :param doc:
    :return:
    """
    data = []

    for section in doc.iter_sections(SectionName.PACHYMETRY, SectionName.CCT):
        if res := search_cct(section.text, section.name):
            data.append(res)
    for m in CCT_SECTION_PAT.finditer(doc.get_text()):
        if res := search_cct(doc.get_text()[m.end(): m.end() + 20], 'ALL'):
            data.append(res)
    return data
