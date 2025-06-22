from eye_extractor.common.algo.fluid import extract_fluid
from eye_extractor.common.algo.macula_wnl import extract_macula_wnl
from eye_extractor.common.algo.treatment import extract_treatment
from eye_extractor.sections.document import Document


def extract_common_algorithms(doc: Document):
    data = {}
    data['treatment'] = extract_treatment(doc)
    data['fluid'] = extract_fluid(doc)
    data['macula_wnl'] = extract_macula_wnl(doc)
    return data
