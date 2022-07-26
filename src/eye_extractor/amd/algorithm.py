from eye_extractor.amd.amd import get_amd
from eye_extractor.amd.drusen import get_drusen
from eye_extractor.amd.fluid import get_fluid
from eye_extractor.amd.ped import extract_ped
from eye_extractor.amd.pigment import get_pigmentary_changes
from eye_extractor.amd.srh import get_subretinal_hemorrhage


def extract_amd_variables(text, *, headers=None, lateralities=None):
    return {
        'amd': list(get_amd(text)),
        'drusen': get_drusen(text, headers=headers, lateralities=lateralities),
        'srh': get_subretinal_hemorrhage(text, headers=headers, lateralities=lateralities),
        'pigment': get_pigmentary_changes(text, headers=headers, lateralities=lateralities),
        'fluid': get_fluid(text, headers=headers, lateralities=lateralities),
        'ped': extract_ped(text, headers=headers, lateralities=lateralities),
    }
