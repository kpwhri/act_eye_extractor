from eye_extractor.amd.amd import extract_amd
from eye_extractor.amd.cnv import extract_choroidalneovasc
from eye_extractor.amd.cyst import extract_macular_cyst
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


def extract_amd_variables(doc):
    return {
        'amd': extract_amd(doc),
        'drusen': extract_drusen(doc),
        'srh': extract_subretinal_hemorrhage(doc),
        'pigment': get_pigmentary_changes(doc),
        'ped': extract_ped(doc),
        'cnv': extract_choroidalneovasc(doc),
        'scar': extract_subret_fibrous(doc),
        'ga': extract_geoatrophy(doc),
        'dry': extract_dryamd_severity(doc),
        'wet': extract_wetamd_severity(doc),
        'vitamin': extract_amd_vitamin(doc),
        'lasertype': extract_lasertype(doc),
        'fluid': extract_fluid(doc),
        'cyst': extract_macular_cyst(doc),
    }
