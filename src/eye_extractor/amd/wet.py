import enum
import re

from eye_extractor.amd.utils import run_on_macula
from eye_extractor.nlp.negate.negation import is_negated
from eye_extractor.laterality import create_new_variable
from eye_extractor.sections.document import Document


class WetSeverity(enum.IntEnum):
    UNKNOWN = -1
    NO = 0
    YES = 1
    ACTIVE = 11  # TODO: unable to find any examples in the text
    INACTIVE = 12


amd = r'(?:ar?md|macul\w+\W*degen\w*)'
wet = r'(?:wet|(?:exudat|neovascul)\w+)'

# TODO: concerns: possible to have cnv before AMD is wet
#                 diabetic with nv of angle and disc, but no AMD
WET_AMD_PAT = re.compile(
    rf'\b(?:'
    rf'(?:{wet}|nv)\W*{amd}'
    rf'|{amd}\W*(?:{wet}|nv)'
    rf')\b',
    re.I
)

WET_PAT = re.compile(
    rf'\b{wet}\b',
    re.I
)


def extract_wetamd_severity(doc: Document):
    return run_on_macula(
        macula_func=_extract_wetamd_severity,
        default_func=_extract_wetamd_severity,  # for testing
        doc=doc,
        all_func=_extract_wetamd_severity_all,
    )


def _extract_wetamd_severity(text, lateralities, source):
    """Extract wet amd from macula section"""
    data = []
    for m in WET_PAT.finditer(text):
        negword = is_negated(m, text, word_window=4)
        data.append(
            create_new_variable(text, m, lateralities, 'wetamd_severity', {
                'value': WetSeverity.NO if negword else WetSeverity.YES,
                'term': m.group(),
                'label': 'no' if negword else 'yes',
                'negated': negword,
                'regex': 'WET_PAT',
                'source': source,
            })
        )
    return data


def _extract_wetamd_severity_all(text, lateralities, source):
    data = []
    for m in WET_AMD_PAT.finditer(text):
        negword = is_negated(m, text, word_window=4)
        data.append(
            create_new_variable(text, m, lateralities, 'wetamd_severity', {
                'value': WetSeverity.NO if negword else WetSeverity.YES,
                'term': m.group(),
                'label': 'no' if negword else 'yes',
                'negated': negword,
                'regex': 'WET_AMD_PAT',
                'source': source,
            })
        )
    return data
