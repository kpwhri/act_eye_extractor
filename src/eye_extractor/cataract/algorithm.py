from eye_extractor.cataract.cataract import extract_cataract
from eye_extractor.cataract.cataract_type import get_cataract_type
from eye_extractor.cataract.intraocular_lens import extract_iol_lens
from eye_extractor.cataract.posterior_cap_opacity import extract_posterior_capsular_opacity
from eye_extractor.sections.document import Document


def extract_cataract_variables(doc: Document):
    results = {}
    results['cataract'] = extract_cataract(doc)
    results['cataract_type'] = get_cataract_type(doc)
    results['intraocular_lens'] = extract_iol_lens(doc)
    results['posterior_cap_opacity'] = extract_posterior_capsular_opacity(doc)
    return results
