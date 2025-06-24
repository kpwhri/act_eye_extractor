import enum
import re

from eye_extractor.nlp.negate.negation import is_negated
from eye_extractor.exam.cup_disk_ratio import cd
from eye_extractor.glaucoma.dx import OCULAR_HYPERTENSIVE_PAT
from eye_extractor.laterality import create_new_variable
from eye_extractor.sections.document import Document


class Preglaucoma(enum.IntEnum):
    UNKNOWN = -1
    NONE = 0
    SUSPECT = 1
    PPG = 2  # pre-perimetric glaucoma
    INCREASED_CD = 3
    OHTN = 4  # ocular hypertension


SUSPECT_PAT = re.compile(
    rf'\b(?:'
    rf'gl\w*\W*suspect'
    rf'|suspect\W*gl\w*'
    rf')\b',
    re.I
)

PPG_PAT = re.compile(
    rf'(?:'
    rf'\bppg\b'
    rf'|pre\W*peri\W*metric\W*gl\w*'
    rf')',
    re.I
)

increased = r'(?:(?:increas|enlarg|high)\w*)'

HIGH_CD_PAT = re.compile(
    rf'(?:'
    rf'{increased}\W*{cd}'
    rf'|{cd}\W*{increased}'
    rf')',
    re.I
)


def extract_preglaucoma_dx(doc: Document):
    data = []

    text = doc.get_text()
    lateralities = doc.get_lateralities()

    for pat, pat_label, value in [
        (SUSPECT_PAT, 'SUSPECT_PAT', Preglaucoma.SUSPECT),
        (PPG_PAT, 'PPG_PAT', Preglaucoma.PPG),
        (HIGH_CD_PAT, 'HIGH_CD_PAT', Preglaucoma.INCREASED_CD),
        (OCULAR_HYPERTENSIVE_PAT, 'OCULAR_HYPERTENSIVE_PAT', Preglaucoma.OHTN),
    ]:
        for m in pat.finditer(text):
            negword = is_negated(m, text)
            data.append(
                create_new_variable(text, m, lateralities, 'preglaucoma', {
                    'value': Preglaucoma.NONE if negword else value,
                    'term': m.group(),
                    'label': 'no' if negword else value.name,
                    'negated': negword,
                    'regex': pat_label,
                    'source': 'ALL',
                })
            )
    return data
