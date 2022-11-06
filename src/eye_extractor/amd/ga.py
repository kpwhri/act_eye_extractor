import enum
import re

from eye_extractor.amd.utils import run_on_macula
from eye_extractor.nlp.negate.negation import is_negated
from eye_extractor.laterality import create_new_variable


class GeoAtrophy(enum.IntEnum):
    UNKNOWN = -1
    NO = 0
    YES = 1


GA_PAT = re.compile(
    rf'\b(?:'
    rf'ga'
    rf'|geo\w*\s*atroph\w*'
    rf')\b',
    re.I
)


def extract_geoatrophy(text, *, headers=None, lateralities=None):
    return run_on_macula(
        macula_func=_extract_ga_macula,
        default_func=_extract_ga_macula,  # for testing
        text=text,
        headers=headers,
        lateralities=lateralities,
        all_func=None,
    )


def _extract_ga_macula(text, lateralities, source):
    """Extract GA from macula section"""
    data = []
    for m in GA_PAT.finditer(text):
        negword = is_negated(m, text)
        data.append(
            create_new_variable(text, m, lateralities, 'geoatrophy', {
                'value': GeoAtrophy.NO if negword else GeoAtrophy.YES,
                'term': m.group(),
                'label': 'no' if negword else 'yes',
                'negated': negword,
                'regex': 'GA_PAT',
                'source': source,
            })
        )
    return data
