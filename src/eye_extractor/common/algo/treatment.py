import enum
import re

from eye_extractor.common.drug.all import ALL_DRUG_PAT
from eye_extractor.common.negation import is_negated, is_post_negated, has_before
from eye_extractor.laterality import build_laterality_table, Laterality, create_new_variable


class Treatment(enum.IntEnum):
    UNKNOWN = -1
    NONE = 0
    # find in plan
    OBSERVE = 1
    CONTINUE_RX = 2
    NEW_MEDICATION = 3
    # laser 100s
    # - glaucoma 100s
    ALT = 100
    SLT = 101
    TRABECULOPLASTY = 102
    # - amd 110s
    LASER = 110
    PHOTODYNAMIC = 111
    THERMAL = 112
    # surgery
    SURGERY = 200
    # medicine


# headers
PLAN_HEADERS = ('PLAN', 'PLAN COMMENTS', 'COMMENTS')

# regular expressions
medrx = rf'(?:med(?:ication?)?s?|rx|{ALL_DRUG_PAT})'

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


def is_treatment_uncertain(m, text):
    return (
            is_negated(m, text, {'vs', 'or', 'consider'})
            or is_post_negated(m, text, {'vs', 'or'})
    )


def get_contextual_laterality(m, section_text):
    curr_laterality = None
    if has_before(m.start(), section_text, {'r'}, char_window=4):
        curr_laterality = Laterality.OD
    elif has_before(m.start(), section_text, {'l'}, char_window=4):
        curr_laterality = Laterality.OS
    return curr_laterality


def extract_treatment(text, *, headers=None, lateralities=None, target_headers=None):
    data = []
    if headers:
        # default values to 'continue', etc.
        for section, section_text in headers.iterate(*PLAN_HEADERS):
            for pat_label, pat, value in [
                ('OBSERVE_PAT', OBSERVE_PAT, Treatment.OBSERVE),
                ('CONTINUE_RX_PAT', CONTINUE_RX_PAT, Treatment.CONTINUE_RX),
                ('NEW_MEDICATION_PAT', NEW_MEDICATION_PAT, Treatment.NEW_MEDICATION)
            ]:
                section_lateralities = build_laterality_table(section_text)
                for m in pat.finditer(section_text):
                    if is_treatment_uncertain(m, section_text):
                        continue
                    negword = is_negated(m, section_text, {'no', 'or', 'without'})
                    curr_laterality = get_contextual_laterality(m, section_text)
                    data.append(
                        create_new_variable(text, m, section_lateralities, 'tx', {
                            'value': Treatment.NONE if negword else value,
                            'term': m.group(),
                            'label': 'no' if negword else value.name,
                            'negated': negword,
                            'regex': pat_label,
                            'source': section,
                        }, known_laterality=curr_laterality)
                    )
    return data
