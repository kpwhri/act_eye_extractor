from eye_extractor.sections.document import Document
from eye_extractor.uveitis.uveitis import get_uveitis


def extract_uveitis(doc: Document):
    results = {}
    results['uveitis'] = get_uveitis(doc)
    return results
