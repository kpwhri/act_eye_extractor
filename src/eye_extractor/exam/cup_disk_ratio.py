"""
Cup Disk Ratio

Cup/Disc Ratio	BE	cupdisc_checkbox		categories	No Mention/ WNL / Result
"""
import re

from eye_extractor.laterality import od_pattern, os_pattern

CUP_DISK_PAT = re.compile(
    r'\b(?:'
    rf'c(?:up)?\W*d(?:is[kc])?\W*?'
    rf'(?:\(.*?\))[:-]'
    rf'\s*(?:{od_pattern})?\s*(?P<od>\d\.\d+)\s*'
    rf'\s*(?:{os_pattern})?\s*(?P<os>\d\.\d+)\b'
    r')\b',
    re.I
)


def extract_cup_disk_ratio(text, *, headers=None, lateralities=None):
    data = []
    for m in CUP_DISK_PAT.finditer(text):
        data.append(
            {
                'context': m.group(),
                'cupdiscratio_rev': m.group('od'),
                'cupdiscratio_lev': m.group('os'),
                'regex': 'CUP_DISK_PAT', 'source': 'ALL',
            }
        )
    if headers:
        pass
    return data
