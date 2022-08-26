from eye_extractor.dr.binary_vars import get_dr_binary
from eye_extractor.dr.cmt_value import get_cmt_value
from eye_extractor.dr.dr_type import get_dr_type
from eye_extractor.dr.hemorrhage_type import get_hemorrhage_type
from eye_extractor.dr.laser_scar_type import get_laser_scar_type


def extract_dr_variables(text: str, *, headers=None, lateralities=None) -> dict:
    return {
        'binary_vars': get_dr_binary(text, headers=headers, lateralities=lateralities),
        'cmt_value': get_cmt_value(text, headers=headers, lateralities=lateralities),
        'dr_type': get_dr_type(text, headers=headers,lateralities=lateralities),
        'hemorrhage_type': get_hemorrhage_type(text, headers=headers, lateralities=lateralities),
        'laser_scar_type': get_laser_scar_type(text, headers=headers, lateralities=lateralities),
    }
