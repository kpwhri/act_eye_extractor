import re

from eye_extractor.common.date import parse_nearest_date_to_line_start
from eye_extractor.nlp.negate.negation import is_negated
from eye_extractor.laterality import lat_lookup
from eye_extractor.sections.document import Document

MACULA_WNL = re.compile(
    rf'\b(?:'
    rf'wnl'
    rf'|clr|clear'
    rf'|normal\W*appearance\W*without\W*edema\W*exudates\W*or\W*hemorrhage'
    rf')'
    rf'[\s,]*(?P<lat>ou|od|os)'
    rf'\b',
    re.IGNORECASE
)


def extract_macula_wnl(doc: Document):
    """Check for cases when macula is normal. This effects AMD, DR, and RO."""
    if doc.sections:
        for section in doc.iter_sections('macula'):
            for m in MACULA_WNL.finditer(section.text):
                if not is_negated(m, section.text):
                    return {
                        'date': parse_nearest_date_to_line_start(m.start(), section.text),
                        'value': 1,
                        'term': m.group(),
                        'lat': lat_lookup(m, group='lat'),
                    }
    return {}
