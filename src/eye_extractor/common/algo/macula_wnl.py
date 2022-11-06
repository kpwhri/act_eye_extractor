import re

from eye_extractor.common.date import parse_nearest_date_to_line_start
from eye_extractor.nlp.negate.negation import is_negated
from eye_extractor.laterality import lat_lookup

MACULA_WNL = re.compile(
    rf'\b(?:'
    rf'wnl'
    rf'|normal\W*appearance\W*without\W*edema\W*exudates\W*or\W*hemorrhage'
    rf')'
    rf'[\s,]*(?P<lat>ou|od|os)'
    rf'\b',
    re.IGNORECASE
)


def extract_macula_wnl(text, headers=None, lateralities=None):
    """Check for cases when macula is normal. This effects AMD, DR, and RO."""
    if headers:
        for section_header, section_text in headers.iterate('MACULA', 'MAC'):
            for m in MACULA_WNL.finditer(section_text):
                if not is_negated(m, section_text):
                    return {
                        'date': parse_nearest_date_to_line_start(m.start(), text),
                        'value': 1,
                        'term': m.group(),
                        'lat': lat_lookup(m, group='lat'),
                    }
    return {}
