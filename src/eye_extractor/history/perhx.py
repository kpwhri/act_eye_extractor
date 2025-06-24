import re

from eye_extractor.history.common import history_pat, create_history_from_doc
from eye_extractor.sections.document import Document
from eye_extractor.sections.patterns import SectionName

START_PER_HX_PAT = re.compile(
    rf'(?:'
    rf'(?:(?:past|personal|medical)\W*)?(?:ocular|eye)\W*{history_pat}\W*?(?:of\W*)?:'
    rf'|(?:(?:past|personal)\W*)?medical\W*{history_pat} ?:?'
    rf'|active\W*problem\W*list ?:?'
    rf'|\bpmhx?\W*?:'
    rf'|past\W*history\W*or\W*currently\W*being\W*treated\W*for\W*?:'
    rf')',
    re.I
)


def create_personal_history(doc: Document):
    return create_history_from_doc(doc, SectionName.EYE_HX, SectionName.MED_HX, SectionName.PROBLEM_LIST,
                                   is_personal_hx=True)
