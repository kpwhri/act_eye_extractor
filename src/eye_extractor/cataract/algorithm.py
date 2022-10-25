from eye_extractor.cataract.cataract import extract_cataract
from eye_extractor.cataract.cataract_type import get_cataract_type
from eye_extractor.cataract.intraocular_lens import extract_iol_lens
from eye_extractor.cataract.posterior_cap_opacity import extract_posterior_capsular_opacity


def extract_cataract_variables(text, *, headers=None, lateralities=None):
    results = {}
    results['cataract'] = extract_cataract(text, headers=headers, lateralities=lateralities)
    results['cataract_type'] = get_cataract_type(text, headers=headers, lateralities=lateralities)
    results['cataract_type'] = get_cataract_type(text, headers=headers, lateralities=lateralities)
    results['intraocular_lens'] = extract_iol_lens(text, headers=headers, lateralities=lateralities)
    results['posterior_cap_opacity'] = extract_posterior_capsular_opacity(text, headers=headers, lateralities=lateralities)
    return results
