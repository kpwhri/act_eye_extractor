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
from eye_extractor.sections.document import Document


def extract_dr_variables(doc: Document) -> dict:
    return {
        'binary_vars': get_dr_binary(doc),
        'cmt_value': get_cmt_value(doc),
        'cottonwspot': get_cottonwspot(doc),
        'dme_yesno': get_dme_yesno(doc),
        'dr_type': get_dr_type(doc),
        'dr_yesno': get_dr_yesno(doc),
        'exudates': get_exudates(doc),
        'hemorrhage_type': get_hemorrhage_type(doc),
        'irma': get_irma(doc),
        'laser_scar_type': get_laser_scar_type(doc),
        'nv_types': get_nv_types(doc),
        'pdr': get_pdr(doc),
        'ret_micro': get_ret_micro(doc),
        'venous_beading': get_ven_beading(doc),
    }
