import enum
import re

from eye_extractor.amd.utils import run_on_macula
from eye_extractor.common.negation import is_negated
from eye_extractor.laterality import create_new_variable


class DrySeverity(enum.IntEnum):
    UNKNOWN = -1
    NO = 0
    UNSPECIFIED = 1
    L1 = 11  # TODO: unable to find any examples in the text
    L2 = 12
    L3 = 13
    L4 = 14


amd = r'(?:ar?md|age\W*related\W*macul\w+\W*degen\w*)'
dry = r'(?:dry|atroph\w*|nnv|non\W*(?:exudat|neovascul)\w+)'

DRY_AMD_PAT = re.compile(
    rf'\b(?:'
    rf'{dry}\W*{amd}'
    rf'|{amd}\W*{dry}'
    rf')\b',
    re.I
)

DRY_PAT = re.compile(
    rf'\b{dry}\b',
    re.I
)


def extract_dryamd_severity(text, *, headers=None, lateralities=None):
    return run_on_macula(
        macula_func=_extract_dryamd_severity,
        default_func=_extract_dryamd_severity,  # for testing
        text=text,
        headers=headers,
        lateralities=lateralities,
        all_func=_extract_dryamd_severity_all,
    )


def _extract_dryamd_severity(text, lateralities, source):
    """Extract dry amd from macula section"""
    data = []
    for m in DRY_PAT.finditer(text):
        negword = is_negated(m, text, {'no', 'or', 'without'})
        data.append(
            create_new_variable(text, m, lateralities, 'dryamd_severity', {
                'value': DrySeverity.NO if negword else DrySeverity.UNSPECIFIED,
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
        negword = is_negated(m, text, {'no', 'or', 'without'})
        data.append(
            create_new_variable(text, m, lateralities, 'dryamd_severity', {
                'value': DrySeverity.NO if negword else DrySeverity.UNSPECIFIED,
                'term': m.group(),
                'label': 'no' if negword else 'yes',
                'negated': negword,
                'regex': 'DRY_AMD_PAT',
                'source': source,
            })
        )
    return data
