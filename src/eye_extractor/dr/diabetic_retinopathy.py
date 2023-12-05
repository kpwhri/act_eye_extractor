from eye_extractor.dr.binary_vars import get_dr_binary
from eye_extractor.dr.cmt_value import get_cmt_value
from eye_extractor.dr.cws import get_cottonwspot
from eye_extractor.dr.dme_yesno import get_dme_yesno
from eye_extractor.dr.dr_type import get_dr_type, get_pdr
from eye_extractor.dr.dr_yesno import get_dr_yesno
from eye_extractor.dr.exudates import get_exudates
from eye_extractor.dr.hemorrhage_type import get_hemorrhage_type
from eye_extractor.dr.irma import get_irma
from eye_extractor.dr.laser_scar_type import get_laser_scar_type
from eye_extractor.dr.nv_types import get_nv_types
from eye_extractor.dr.ret_micro import get_ret_micro
from eye_extractor.dr.venous_beading import get_ven_beading


def extract_dr_variables(text: str, *, headers=None, lateralities=None) -> dict:
    return {
        'binary_vars': get_dr_binary(text, headers=headers, lateralities=lateralities),
        'cmt_value': get_cmt_value(text, headers=headers, lateralities=lateralities),
        'cottonwspot': get_cottonwspot(text, headers=headers, lateralities=lateralities),
        'dme_yesno': get_dme_yesno(text, headers=headers, lateralities=lateralities),
        'dr_type': get_dr_type(text, headers=headers, lateralities=lateralities),
        'dr_yesno': get_dr_yesno(text, headers=headers, lateralities=lateralities),
        'exudates': get_exudates(text, headers=headers, lateralities=lateralities),
        'hemorrhage_type': get_hemorrhage_type(text, headers=headers, lateralities=lateralities),
        'irma': get_irma(text, headers=headers, lateralities=lateralities),
        'laser_scar_type': get_laser_scar_type(text, headers=headers, lateralities=lateralities),
        'nv_types': get_nv_types(text, headers=headers, lateralities=lateralities),
        'pdr': get_pdr(text, headers=headers, lateralities=lateralities),
        'ret_micro': get_ret_micro(text, headers=headers, lateralities=lateralities),
        'venous_beading': get_ven_beading(text, headers=headers, lateralities=lateralities),
    }
