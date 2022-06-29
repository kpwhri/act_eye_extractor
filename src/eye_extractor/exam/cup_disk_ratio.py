"""
Cup Disk Ratio

Cup/Disc Ratio	BE	cupdisc_checkbox		categories	No Mention/ WNL / Result
"""
import re

from eye_extractor.laterality import od_pattern, os_pattern, ou_pattern

cd_ratio = (rf'c(?:up)?\W*d(?:is[kc])?\W*?'
            rf'(?:ratios?\s*)?'
            rf'(?:\(.*?\))?[:-]?')
ratio = r'\d\.\d+'

CUP_DISK_PAT = re.compile(
    rf'\b(?:{cd_ratio}'
    rf'(?:'
    rf'\s*(?:{od_pattern})\s*(?P<od>{ratio})\W*'
    rf'\s*(?:{os_pattern})\s*(?P<os>{ratio})\b'
    rf'|'
    rf'\s*(?:{ou_pattern})\s*(?P<ou>{ratio})\b'
    rf'|'
    rf'\s*(?P<ou2>{ratio})\s*(?:{ou_pattern})'
    rf')'
    rf')\b',
    re.I
)

CUP_DISC_NO_LAT_LABEL_PAT = re.compile(
    rf'\b(?:{cd_ratio}\W*(?P<od>{ratio})\s*(?:[,/]\s*)?(?P<os>{ratio}))\b',
    re.I
)


def extract_cup_disk_ratio(text, *, headers=None, lateralities=None):
    data = []
    for m in CUP_DISK_PAT.finditer(text):
        data.append(
            {
                'context': m.group(),
                'cupdiscratio_rev': m.group('od') or m.group('ou') or m.group('ou2'),
                'cupdiscratio_reh': m.group('od') or m.group('ou') or m.group('ou2'),
                'cupdiscratio_lev': m.group('os') or m.group('ou') or m.group('ou2'),
                'cupdiscratio_leh': m.group('os') or m.group('ou') or m.group('ou2'),
                'regex': 'CUP_DISK_PAT', 'source': 'ALL',
            }
        )
    if headers:
        pass
    return data
