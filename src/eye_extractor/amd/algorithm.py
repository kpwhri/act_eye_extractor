from eye_extractor.amd.amd import get_amd
from eye_extractor.amd.drusen import get_drusen
from eye_extractor.amd.srh import get_subretinal_hemorrhage


def extract_amd_variables(text, *, headers=None, lateralities=None):
    return {
        'amd': list(get_amd(text)),
        'drusen': get_drusen(text, headers=headers, lateralities=lateralities),
        'srh': get_subretinal_hemorrhage(text, headers=headers, lateralities=lateralities),
    }
