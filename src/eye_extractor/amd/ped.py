import enum
import re

from eye_extractor.amd.utils import run_on_macula
from eye_extractor.nlp.negate.negation import is_negated
from eye_extractor.laterality import create_new_variable

detach = r'(?:detach)\w*'
pig_epith = r'(?:pig\w*\W*epith\w*)'


class PigEpiDetach(enum.IntEnum):
    UNKNOWN = -1
    NO = 0
    YES = 1


PED_PAT = re.compile(
    rf'\b(?:'
    rf'r?peds?'
    rf'|{pig_epith}\W*{detach}'
    rf'|{detach}\W+(?:\w+\W*){{,3}}{pig_epith}'
    rf')\b',
    re.IGNORECASE
)


def extract_ped(text, *, headers=None, lateralities=None):
    return run_on_macula(
        macula_func=_extract_ped,
        default_func=_extract_ped,
        text=text,
        headers=headers,
        lateralities=lateralities,
    )


def _extract_ped(text, lateralities, source):
    data = []
    for m in PED_PAT.finditer(text):
        negword = is_negated(m, text, word_window=3)
        data.append(
            create_new_variable(text, m, lateralities, 'ped', {
                'value': PigEpiDetach.NO if negword else PigEpiDetach.YES,
                'term': m.group(),
                'label': 'no' if negword else 'yes',
                'negated': negword,
                'regex': 'PED_PAT',
                'source': source,
            })
        )
    return data
