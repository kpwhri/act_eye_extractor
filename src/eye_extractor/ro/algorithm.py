from eye_extractor.ro.rao import get_rao
from eye_extractor.ro.rvo import extract_rvo
from eye_extractor.sections.document import Document


def extract_ro_variables(doc: Document):
    results = {}
    results['rao'] = get_rao(doc)
    results['rvo'] = extract_rvo(doc)
    return results
