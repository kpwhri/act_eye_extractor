from eye_extractor.ro.rao import get_rao
from eye_extractor.ro.rvo import get_rvo


def extract_ro_variables(text, *, headers=None, lateralities=None):
    return {
        'rao': get_rao(text, headers=headers, lateralities=lateralities),
        'rvo': get_rvo(text, headers=headers, lateralities=lateralities),
    }
