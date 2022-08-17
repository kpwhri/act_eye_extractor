import re

from eye_extractor.common.date import parse_date_before
from eye_extractor.laterality import laterality_pattern, lat_lookup, Laterality

TABLE_HEADER_PAT = re.compile(
    rf'(?:'
    rf'rnfl\s+sup\s+inf\s+nas\s+temp\s+global'
    rf')',
    re.I
)

_value = r'\d{1,3}[rgy]?'
VALUE_PAT = re.compile(_value, re.I)
TABLE_ROW_PAT = re.compile(
    rf'(?:'
    rf'(?P<lat>{laterality_pattern})\W*'
    rf'(?P<sup>{_value}|\S+)\s+'
    rf'(?P<inf>{_value}|\S+)\s+'
    rf'(?P<nas>{_value}|\S+)\s+'
    rf'(?P<temp>{_value}|\S+)\s+'
    rf'(?P<global>{_value}|\S+)'
    rf')',
    re.I
)


def extract_rnfl_values(text, *, headers=None, lateralities=None):
    data = []
    for header_match in TABLE_HEADER_PAT.finditer(text):
        result = {}
        result['date'] = parse_date_before(header_match, text, as_string=True)
        end = header_match.end()
        for _ in range(2):
            if m := TABLE_ROW_PAT.search(text[end:end + 75]):
                if lat_lookup(m, group='lat') == Laterality.OD:
                    result.update(_unpack_matches(m, 're'))
                elif lat_lookup(m, group='lat') == Laterality.OS:
                    result.update(_unpack_matches(m, 'le'))
                end += m.end()
            else:
                break
        data.append(result)
    return data


def _unpack_matches(m, lat_string):
    def if_matches(label):
        _val = m.group(label)
        return int(_val.strip('gry')) if VALUE_PAT.match(_val) else -1
    return {
        f'rnfloct_temporal_sup_{lat_string}': if_matches('sup'),
        f'rnfloct_temporal_inf_{lat_string}': if_matches('inf'),
        f'rnfloct_nasal_{lat_string}': if_matches('nas'),
        f'rnfloct_temporal_{lat_string}': if_matches('temp'),
        f'rnfloct_globalscore_{lat_string}': if_matches('global'),
    }
