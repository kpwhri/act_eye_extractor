from eye_extractor.ro.rao import get_rao
from eye_extractor.ro.rvo import extract_rvo


def extract_ro_variables(text, *, headers=None, lateralities=None):
    results = {}
    results['rao'] = get_rao(text, headers=headers, lateralities=lateralities)
    results['rvo'] = extract_rvo(text, headers=headers, lateralities=lateralities)
    return results
