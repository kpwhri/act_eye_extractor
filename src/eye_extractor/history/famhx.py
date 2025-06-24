import re

from eye_extractor.history.common import create_history, create_history_from_doc
from eye_extractor.sections.document import Document
from eye_extractor.sections.patterns import SectionName

START_FAM_HX_PAT = re.compile(
    rf'\b(?:'
    rf'family\W*(?:(?:eye|ocular)\W*)?history\W*(?:of\W*)?'
    rf'|famhx'
    rf'|fhx'
    rf'):',
    re.I
)


def create_family_history(doc: Document):
    return create_history_from_doc(doc, SectionName.FAMILY_EYE_HX, SectionName.FAMILY_HX)
