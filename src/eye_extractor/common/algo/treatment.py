import enum


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


def extract_treatment(text, *, headers=None, lateralities=None, target_headers=None):
    data = []
    if headers and target_headers:
        for section, section_text in headers.iterate(target_headers):
            pass
