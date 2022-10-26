import re

from eye_extractor.common.date import parse_nearest_date_to_line_start
from eye_extractor.common.negation import is_negated

MACULA_WNL = re.compile(
    rf'\b(?:'
    rf'WNL\s+OU'
    rf')\b',
    re.IGNORECASE
)


def extract_macula_wnl(text, headers=None, lateralities=None):
    """Check for cases when macula is normal. This effects AMD, DR, and RO."""
    if headers:
        for section_header, section_text in headers.iterate('MACULA', 'MAC'):
            print(section_text)
            for m in MACULA_WNL.finditer(section_text):
                print(m)
                print(is_negated(m, section_text))
                if not is_negated(m, section_text):
                    return {
                        'date': parse_nearest_date_to_line_start(m.start(), text),
                        'value': 1,
                        'term': m.group(),
                    }
    return {}
