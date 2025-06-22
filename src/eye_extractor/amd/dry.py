import enum
import re

from eye_extractor.amd.utils import run_on_macula
from eye_extractor.nlp.negate.negation import is_negated, is_post_negated
from eye_extractor.laterality import create_new_variable
from eye_extractor.sections.document import Document


class DrySeverity(enum.IntEnum):
    UNKNOWN = -1
    NO = 0
    YES = 1
    L1 = 11  # TODO: unable to find any examples in the text
    L2 = 12
    L3 = 13
    L4 = 14


amd = r'(?:ar?md|macul\w+\W*degen\w*)'
dry = r'(?:dry|atroph\w*|nnv|non\W*(?:exudat|neovascul)\w+)'
between = r'(?:senile)?'

DRY_AMD_PAT = re.compile(
    rf'\b(?:'
    rf'{dry}\W*{between}\W*{amd}'
    rf'|{amd}\W*{between}\W*{dry}'
    rf')\b',
    re.I
)

DRY_PAT = re.compile(
    rf'\b{dry}\b',
    re.I
)


def extract_dryamd_severity(doc: Document):
    return run_on_macula(
        macula_func=_extract_dryamd_severity,
        default_func=_extract_dryamd_severity,  # for testing
        doc=doc,
        all_func=_extract_dryamd_severity_all,
    )


def _extract_dryamd_severity(text, lateralities, source):
    """Extract dry amd from macula section"""
    data = []
    for m in DRY_PAT.finditer(text):
        if is_post_negated(m, text, {'eye', 'eyes'}) or is_negated(m, text, {'eye', 'eyes'}, word_window=4):
            continue
        negword = is_negated(m, text)
        data.append(
            create_new_variable(text, m, lateralities, 'dryamd_severity', {
                'value': DrySeverity.NO if negword else DrySeverity.YES,
                'term': m.group(),
                'label': 'no' if negword else 'yes',
                'negated': negword,
                'regex': 'DRY_PAT',
                'source': source,
            })
        )
    return data


def _extract_dryamd_severity_all(text, lateralities, source):
    data = []
    for m in DRY_AMD_PAT.finditer(text):
        if is_post_negated(m, text, {'eye', 'eyes'}):
            continue
        negword = is_negated(m, text)
        data.append(
            create_new_variable(text, m, lateralities, 'dryamd_severity', {
                'value': DrySeverity.NO if negword else DrySeverity.YES,
                'term': m.group(),
                'label': 'no' if negword else 'yes',
                'negated': negword,
                'regex': 'DRY_AMD_PAT',
                'source': source,
            })
        )
    return data
