import enum
import re

from eye_extractor.common.negation import is_negated
from eye_extractor.common.severity import extract_severity, Severity
from eye_extractor.laterality import build_laterality_table, create_new_variable

VEN_BEADING_PAT = re.compile(
    r'\b('
    r'venous beading|vb'
    r')\b',
    re.I
)


def get_ven_beading(text: str, *, headers=None, lateralities=None) -> list:
    # if not lateralities:
    #     lateralities = build_laterality_table(text)
    # data = []
    # for new_var in _get_hemorrhage_type(text, lateralities, 'ALL'):
    #     data.append(new_var)
    # if headers:
    #     pass
    #
    # return data
    pass
