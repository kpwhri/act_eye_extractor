import enum
import re

from eye_extractor.dr.binary_vars import get_dr_binary
from eye_extractor.dr.hemorrhage_type import get_hemorrhage_type


def extract_dr_variables(text: str, *, headers=None, lateralities=None) -> dict:
    return {
        'dr': get_dr_binary(text, headers=headers, lateralities=lateralities),
        'hemorrhage_type': get_hemorrhage_type(text, headers=headers, lateralities=lateralities)
    }
