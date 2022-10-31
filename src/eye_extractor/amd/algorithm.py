from eye_extractor.amd.amd import extract_amd
from eye_extractor.amd.cnv import extract_choroidalneovasc
from eye_extractor.amd.drusen import extract_drusen
from eye_extractor.amd.dry import extract_dryamd_severity
from eye_extractor.amd.ga import extract_geoatrophy
from eye_extractor.amd.lasertype import extract_lasertype
from eye_extractor.amd.ped import extract_ped
from eye_extractor.amd.pigment import get_pigmentary_changes
from eye_extractor.amd.scar import extract_subret_fibrous
from eye_extractor.amd.srh import extract_subretinal_hemorrhage
from eye_extractor.amd.vitamins import extract_amd_vitamin
from eye_extractor.amd.wet import extract_wetamd_severity
from eye_extractor.common.algo.fluid import extract_fluid


def extract_amd_variables(text, *, headers=None, lateralities=None):
    return {
        'amd': extract_amd(text, headers=headers, lateralities=lateralities),
        'drusen': extract_drusen(text, headers=headers, lateralities=lateralities),
        'srh': extract_subretinal_hemorrhage(text, headers=headers, lateralities=lateralities),
        'pigment': get_pigmentary_changes(text, headers=headers, lateralities=lateralities),
        'ped': extract_ped(text, headers=headers, lateralities=lateralities),
        'cnv': extract_choroidalneovasc(text, headers=headers, lateralities=lateralities),
        'scar': extract_subret_fibrous(text, headers=headers, lateralities=lateralities),
        'ga': extract_geoatrophy(text, headers=headers, lateralities=lateralities),
        'dry': extract_dryamd_severity(text, headers=headers, lateralities=lateralities),
        'wet': extract_wetamd_severity(text, headers=headers, lateralities=lateralities),
        'vitamin': extract_amd_vitamin(text, headers=headers, lateralities=lateralities),
        'lasertype': extract_lasertype(text, headers=headers, lateralities=lateralities),
        'fluid': extract_fluid(text, headers=headers, lateralities=lateralities),
    }
