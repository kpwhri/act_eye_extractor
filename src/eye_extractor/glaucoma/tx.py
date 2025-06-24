"""
Glaucoma Treatment Plan `glaucoma_tx`
"""
import enum
import re

from eye_extractor.common.drug.drops import DROPS_PAT
from eye_extractor.nlp.negate.negation import is_negated, is_post_negated, has_before
from eye_extractor.laterality import build_laterality_table, create_new_variable, Laterality
from eye_extractor.sections.document import Document
from eye_extractor.sections.patterns import SectionName


class GlaucomaTreatment(enum.IntEnum):
    UNKNOWN = -1
    NONE = 0
    OBSERVE = 1
    CONTINUE_RX = 2
    NEW_MEDICATION = 3
    ALT = 4
    SLT = 5
    SURGERY = 6
    TRABECULOPLASTY = 7


medrx = rf'(?:med(?:ication?)?s?|rx|{DROPS_PAT})'

OBSERVE_PAT = re.compile(
    rf'(?:'
    rf'(?:continue\W*to\W*)?observe'
    rf')',
    re.I
)

CONTINUE_RX_PAT = re.compile(
    rf'(?:'
    rf'continue\W*{medrx}?'
    rf')',
    re.I
)
NEW_MEDICATION_PAT = re.compile(
    rf'(?:'
    rf'(?:change|add|new|start)\W*{medrx}'
    rf'|{medrx}\W*as\W*(?:\w+\W+){{0,2}}(?:below|above)'
    rf')',
    re.I
)
ALT_PAT = re.compile(
    rf'\b(?:'
    rf'alt|argon\W*laser\W*(?:trabecul\w+)?'
    rf')\b',
    re.I
)
SLT_PAT = re.compile(
    rf'\b(?:'
    rf'slt|selective\W*laser\W*(?:trabecul\w+)?'
    rf')\b',
    re.I
)
SURGERY_PAT = re.compile(
    rf'(?:'
    rf'surgery'
    rf')',
    re.I
)
TRABECULOPLASTY_PAT = re.compile(
    rf'\b(?:'
    rf'trabecul\w+'
    rf')\b',
    re.I
)


def extract_tx(doc: Document):
    data = []
    for section in doc.iter_sections(SectionName.PLAN, SectionName.COMMENT):
        for pat_label, pat, value in [
            ('OBSERVE_PAT', OBSERVE_PAT, GlaucomaTreatment.OBSERVE),
            ('CONTINUE_RX_PAT', CONTINUE_RX_PAT, GlaucomaTreatment.CONTINUE_RX),
            ('NEW_MEDICATION_PAT', NEW_MEDICATION_PAT, GlaucomaTreatment.NEW_MEDICATION),
            ('ALT_PAT', ALT_PAT, GlaucomaTreatment.ALT),
            ('SLT_PAT', SLT_PAT, GlaucomaTreatment.SLT),
            ('SURGERY_PAT', SURGERY_PAT, GlaucomaTreatment.SURGERY),
            ('TRABECULOPLASTY_PAT', TRABECULOPLASTY_PAT, GlaucomaTreatment.TRABECULOPLASTY),
        ]:
            for m in pat.finditer(section.text):
                if (is_negated(m, section.text, {'vs'})
                        or is_post_negated(m, section.text, {'vs'})):
                    continue
                curr_laterality = None
                negword = is_negated(m, section.text)
                if has_before(m.start(), section.text, {'r'}, char_window=4):
                    curr_laterality = Laterality.OD
                elif has_before(m.start(), section.text, {'l'}, char_window=4):
                    curr_laterality = Laterality.OS
                data.append(
                    create_new_variable(section.text, m, section.lateralities, 'glaucoma_tx', {
                        'value': GlaucomaTreatment.NONE if negword else value,
                        'term': m.group(),
                        'label': 'no' if negword else value.name,
                        'negated': negword,
                        'regex': pat_label,
                        'source': section.name,
                    }, known_laterality=curr_laterality)
                )
    return data
