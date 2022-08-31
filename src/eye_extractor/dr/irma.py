import re

from eye_extractor.common.negation import is_negated
from eye_extractor.common.severity import extract_severity, Severity
from eye_extractor.laterality import build_laterality_table, create_new_variable

IRMA_PAT = re.compile(
    r'\b('
    r'irma|intraretinal\s+microvascular\s+abnormality'
    r')\b',
    re.I
)
