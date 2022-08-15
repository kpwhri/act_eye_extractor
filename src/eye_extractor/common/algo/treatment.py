import enum
import re

from eye_extractor.common.drug.all import ALL_DRUG_PAT
from eye_extractor.common.drug.antivegf import ANTIVEGF_RX, ANTIVEGF_TO_ENUM, ANTIVEGF_PAT
from eye_extractor.common.drug.shared import get_standardized_name
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
    # - steroiod
    STEROID = 300
    TRIAMCINOLONE = 301
    DEXAMETHASONE = 302
    IMPLANT = 303
    # -antivegf
    ANTIVEGF = 311
    AFLIBERCEPT = 312  # Eyelea
    BEVACIZUMAB = 313  # Avastin
    RANIBIZUMAB = 314  # Lucentis


# headers
PLAN_HEADERS = ('PLAN', 'PLAN COMMENTS', 'COMMENTS')
GLAUCOMA_HEADERS = ('PLAN', 'PLAN COMMENTS', 'COMMENTS')
AMD_HEADERS = ('ASSESSMENT', 'IMPRESSION', 'IMP', 'HX', 'PAST', 'ASSESSMENT COMMENTS', 'PLAN')
ANTIVEGF_HEADERS = ('SUBJECTIVE', 'CHIEF COMPLAINT', 'HISTORY OF PRESENT ILLNESS')

# regular expressions
medrx = rf'(?:med(?:ication?)?s?|rx|{ALL_DRUG_PAT})'

# - general
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

# - glaucoma
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

# - amd
LASER_PAT = re.compile(
    rf'\blaser(?:\W*photo\W?coagulation)?\b',
    re.I
)

PHOTODYNAMIC_PAT = re.compile(  # verb + med
    rf'\b(?:'
    rf'pdt'
    rf'|photodynamic(?:\W*therapy)?'
    rf')\b',
    re.I
)

THERMAL_PAT = re.compile(  # verb + med
    rf'\b(?:'
    rf'thermal(?:\W*laser)?'
    rf')\b',
    re.I
)

# - steroid for rvo
STEROID_PAT = re.compile(
    rf'\b(?:'
    rf'(?:cortico)?steroids?'
    rf')\b',
    re.I
)
IMPLANT_PAT = re.compile(
    rf'\b(?:'
    rf'implant'
    rf')\b',
    re.I
)
TRIAMCINOLONE_PAT = re.compile(
    rf'\b(?:'
    rf'triamcinolone\s*(?:acetonide)?'
    rf')\b',
    re.I
)
DEXAMETHASONE_PAT = re.compile(
    rf'\b(?:'
    rf'dexamethasone\s*(?:implant)?'
    rf')\b',
    re.I
)
OTHER_STEROID_PAT = re.compile(
    rf'\b(?:'
    rf'fluocinolone\s*(?:acetonide)?'
    rf'|retisert'
    rf'|illuvien'
    rf'|yutiq'
    rf')\b',
    re.I
)


def is_treatment_uncertain(m, text):
    return (
            is_negated(m, text, {'vs', 'or', 'consider', 'defer', 'option'})
            or is_post_negated(m, text, {'vs', 'or', 'defer'})
    )


def get_contextual_laterality(m, section_text):
    curr_laterality = None
    if has_before(m.start(), section_text, {'r', 'rt'}, char_window=6):
        curr_laterality = Laterality.OD
    elif has_before(m.start(), section_text, {'l', 'lt'}, char_window=6):
        curr_laterality = Laterality.OS
    return curr_laterality


def extract_treatment(text, *, headers=None, lateralities=None, target_headers=None):
    data = []
    if headers:
        # default values to 'continue', etc.
        for result in _extract_treatment_section(
                headers,
                PLAN_HEADERS,
                'ALL',
                ('OBSERVE_PAT', OBSERVE_PAT, Treatment.OBSERVE),
                ('CONTINUE_RX_PAT', CONTINUE_RX_PAT, Treatment.CONTINUE_RX),
                ('NEW_MEDICATION_PAT', NEW_MEDICATION_PAT, Treatment.NEW_MEDICATION),
        ):
            data.append(result)
        # laser targets
        for result in _extract_treatment_section(
                headers,
                PLAN_HEADERS,
                'LASER',
                ('LASER_PAT', LASER_PAT, Treatment.LASER),
                ('PHOTODYNAMIC_PAT', PHOTODYNAMIC_PAT, Treatment.PHOTODYNAMIC),
                ('THERMAL_PAT', THERMAL_PAT, Treatment.THERMAL),
                ('TRABECULOPLASTY_PAT', TRABECULOPLASTY_PAT, Treatment.TRABECULOPLASTY),
                ('ALT_PAT', ALT_PAT, Treatment.ALT),
                ('SLT_PAT', SLT_PAT, Treatment.SLT),
        ):
            data.append(result)
        # glaucoma targets
        for result in _extract_treatment_section(
                headers,
                GLAUCOMA_HEADERS,
                'GLAUCOMA',
                ('ALT_PAT', ALT_PAT, Treatment.ALT),
                ('SLT_PAT', SLT_PAT, Treatment.SLT),
                ('SURGERY_PAT', SURGERY_PAT, Treatment.SURGERY),
                ('TRABECULOPLASTY_PAT', TRABECULOPLASTY_PAT, Treatment.TRABECULOPLASTY),
        ):
            data.append(result)
        # amd targets
        for result in _extract_treatment_section(
                headers,
                AMD_HEADERS,
                'AMD',
                ('LASER_PAT', LASER_PAT, Treatment.LASER),
                ('PHOTODYNAMIC_PAT', PHOTODYNAMIC_PAT, Treatment.PHOTODYNAMIC),
                ('THERMAL_PAT', THERMAL_PAT, Treatment.THERMAL),
        ):
            data.append(result)
        for result in _extract_treatment_section(
                headers,
                AMD_HEADERS,
                'ANTIVEGF',
                ('ANTIVEGF_RX', ANTIVEGF_RX, lambda m: ANTIVEGF_TO_ENUM[get_standardized_name(m.group())]),
        ):
            data.append(result)
        for result in _extract_treatment_section(
                headers,
                PLAN_HEADERS,
                'RVO',
                ('STEROID_PAT', STEROID_PAT, Treatment.STEROID),
                ('TRIAMCINOLONE_PAT', TRIAMCINOLONE_PAT, Treatment.TRIAMCINOLONE),
                ('DEXAMETHASONE_PAT', DEXAMETHASONE_PAT, Treatment.DEXAMETHASONE),
                ('IMPLANT_PAT', IMPLANT_PAT, Treatment.IMPLANT),
        ):
            data.append(result)
    # all text
    for result in _extract_treatment(
            'ALL', text, lateralities, 'ANTIVEGF',
            ('ANTIVEGF_RX',
             re.compile(fr's/p\W*(?P<term>{ANTIVEGF_PAT})', re.I),
             lambda m: ANTIVEGF_TO_ENUM[get_standardized_name(m.group('term'))]
             )
    ):
        data.append(result)
    return data


def _extract_treatment_section(headers, target_headers, category, *patterns):
    for section, section_text in headers.iterate(*target_headers):
        section_lateralities = build_laterality_table(section_text)
        yield from _extract_treatment(section, section_text, section_lateralities, category, *patterns)


def _extract_treatment(section, section_text, section_lateralities, category, *patterns):
    for pat_label, pat, value in patterns:
        for m in pat.finditer(section_text):
            if is_treatment_uncertain(m, section_text):
                continue
            negword = is_negated(m, section_text, {'no', 'or', 'without', 'if'})
            curr_laterality = get_contextual_laterality(m, section_text)
            # TODO: check if disease is mentioned in vicinity (e.g., DR, AMD, etc.)
            if callable(value):
                value = value(m)
            yield create_new_variable(section_text, m, section_lateralities, 'tx', {
                'value': Treatment.NONE if negword else value,
                'term': m.group(),
                'label': 'no' if negword else value.name,
                'negated': negword,
                'regex': pat_label,
                'category': category,
                'source': section,
            }, known_laterality=curr_laterality)
