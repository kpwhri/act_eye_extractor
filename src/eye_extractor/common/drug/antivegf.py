import enum

from eye_extractor.common.drug.shared import build_regex_from_dict


class AntiVegf(enum.IntEnum):
    UNKNOWN = -1
    NONE = 0
    YES = 1
    AFLIBERCEPT = 2  # Eyelea
    BEVACIZUMAB = 3  # Avastin
    RANIBIZUMAB = 4  # Lucentis


ANTIVEGF_TO_ENUM = {
    'aflibercept': AntiVegf.AFLIBERCEPT,
    'eyelea': AntiVegf.AFLIBERCEPT,
    'bevacizumab': AntiVegf.BEVACIZUMAB,
    'avastin': AntiVegf.BEVACIZUMAB,
    'ranibuzumab': AntiVegf.RANIBIZUMAB,
    'lucentis': AntiVegf.RANIBIZUMAB,
}

ANTIVEGF_RX = build_regex_from_dict(ANTIVEGF_TO_ENUM)
