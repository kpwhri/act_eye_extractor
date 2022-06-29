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
                    'cupdiscratio_rev': m.group('od') or m.group('ou') or m.group('ou2'),
                    'cupdiscratio_reh': m.group('od') or m.group('ou') or m.group('ou2'),
                    'cupdiscratio_lev': m.group('os') or m.group('ou') or m.group('ou2'),
                    'cupdiscratio_leh': m.group('os') or m.group('ou') or m.group('ou2'),
                    'measurement_date': followed_by_date(m, text),
                    'regex': pat_label, 'source': 'ALL',
                }
            )
    if headers:
        pass
    return data
