import re

from eye_extractor.common.date import parse_date_before
from eye_extractor.headers import Headers

CMT_PAT = re.compile(
    rf'\b(?:'
    rf'cmt\W+od\W+(?P<od_value>\d+)'
    r'[\w\s,.;()-]{0,100}'
    rf'os\W+(?P<os_value>\d+)'
    rf')\b',
    re.I
)


def extract_cmt(text, *, headers: Headers = None, lateralities=None):
    data = []
    if headers:
        for section_name, section_text in headers.iterate('OCT MAC', 'OCT MACULA'):
            for m in CMT_PAT.finditer(section_text):
                date = parse_date_before(m, section_text, as_string=True)
                data.append({'macularoct_thickness_re': {
                    'value': int(m.group('od_value')),
                    'date': date,
                    'term': m.group(),
                    'source': section_name,
                    'regex': 'CMT_PAT',
                }})
                data.append({'macularoct_thickness_le': {
                    'value': int(m.group('os_value')),
                    'date': date,
                    'term': m.group(),
                    'source': section_name,
                    'regex': 'CMT_PAT',
                }})
    return data
