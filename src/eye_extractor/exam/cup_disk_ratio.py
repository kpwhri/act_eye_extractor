"""
Cup Disk Ratio

Cup/Disc Ratio	BE	cupdisc_checkbox		categories	No Mention/ WNL / Result

TODO:
* handle v/h when presented separately
    - c/d od 0.6v0.65h os 0.5v/0.55h
    - c/d 0.6+/0.6+ od 0.5+/0.5+ os
* handle (+0.01) language (see incr in CUP_DISC_UNILAT_PAT)
* handle 'disc-' as header
"""
import re

from eye_extractor.common.regex import coalesce_match
from eye_extractor.laterality import od_pattern, os_pattern, ou_pattern

cd_ratio = (rf'c(?:up)?\W*d(?:is[kc])?\W*?'
            rf'(?:ratios?\s*)?'
            rf'(?:\(.*?\))?[:-]?')
ratio = r'\d\.\d+'

CUP_DISK_PAT = re.compile(
    rf'\b(?:{cd_ratio}'
    rf'(?:'
    rf'\s*(?:{od_pattern}|pd)\s*(?P<od>{ratio})\W*'
    rf'\s*(?:{os_pattern})\s*(?P<os>{ratio})\b'
    rf'|'
    rf'\s*(?P<od2>{ratio})\s*(?:{od_pattern}|pd)\W*'
    rf'\s*(?P<os2>{ratio})\s*(?:{os_pattern})\b'
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

CUP_DISC_UNILAT_PAT = re.compile(
    rf'\b(?:'
    rf'(?:'
    rf'(?P<od>{od_pattern})|(?P<os>{os_pattern})|(?P<ou>{ou_pattern})'
    rf')\W*'
    rf'(?:linear\s*)?'
    rf'{cd_ratio}\s*'
    rf'(?P<ratio>{ratio})\s*'
    rf'(?:\(\+?(?P<incr>{ratio})\))?'
    rf')\b',
    re.I
)


CUP_DISC_HV_PAT = re.compile(
    rf'\b(?:{cd_ratio})',
    re.I
)


def followed_by_date(m, text):
    m = re.search(
        r'(?P<m>\d{1,2})[-/](?P<d>\d{1,2})[-/](?P<y>\d{2,4})',
        text[m.end():m.end() + 30],
        re.I
    )
    if m:
        year = m.group('y')
        if len(year) == 2:
            year = f'20{year}'
        month = m.group('m')
        day = m.group('d')
        return f'{year}-{month}-{day}'


def extract_cup_disk_ratio(text, *, headers=None, lateralities=None):
    data = []
    for pat_label, pat in [
        ('CUP_DISK_PAT', CUP_DISK_PAT),
        ('CUP_DISC_NO_LAT_LABEL_PAT', CUP_DISC_NO_LAT_LABEL_PAT),
    ]:
        for m in pat.finditer(text):
            data.append(
                {
                    'context': m.group(),
                    'cupdiscratio_rev': coalesce_match(m, 'od', 'od2', 'ou', 'ou2'),
                    'cupdiscratio_reh': coalesce_match(m, 'od', 'od2', 'ou', 'ou2'),
                    'cupdiscratio_lev': coalesce_match(m, 'os', 'os2', 'ou', 'ou2'),
                    'cupdiscratio_leh': coalesce_match(m, 'os', 'os2', 'ou', 'ou2'),
                    'measurement_date': followed_by_date(m, text),
                    'regex': pat_label, 'source': 'ALL',
                }
            )
    if len(data) == 0:
        for m in CUP_DISC_UNILAT_PAT.finditer(text):
            data.append(
                {
                    'context': m.group(),
                    'measurement_date': followed_by_date(m, text),
                    'regex': 'CUP_DISC_UNILAT_PAT', 'source': 'ALL',
                }
            )
            if coalesce_match(m, 'od', 'ou'):
                data[-1]['cupdiscratio_rev'] = m.group('ratio')
                data[-1]['cupdiscratio_reh'] = m.group('ratio')
            elif coalesce_match(m, 'os', 'ou'):
                data[-1]['cupdiscratio_lev'] = m.group('ratio')
                data[-1]['cupdiscratio_leh'] = m.group('ratio')

    if headers:
        pass
    return data
