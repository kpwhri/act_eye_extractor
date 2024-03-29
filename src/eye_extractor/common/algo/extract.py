from eye_extractor.common.algo.fluid import extract_fluid
from eye_extractor.common.algo.macula_wnl import extract_macula_wnl
from eye_extractor.common.algo.treatment import extract_treatment


def extract_common_algorithms(text, *, headers=None, lateralities=None):
    data = {}
    data['treatment'] = extract_treatment(text, headers=headers, lateralities=lateralities)
    data['fluid'] = extract_fluid(text, headers=headers, lateralities=lateralities)
    data['macula_wnl'] = extract_macula_wnl(text, headers=headers, lateralities=lateralities)
    return data
