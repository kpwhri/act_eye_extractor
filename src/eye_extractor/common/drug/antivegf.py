import enum

from eye_extractor.common.drug.shared import build_regex_from_dict, build_pattern_from_dict


class AntiVegf(enum.IntEnum):
    UNKNOWN = -1
    NONE = 0
    YES = 311
    AFLIBERCEPT = 312  # Eyelea
    BEVACIZUMAB = 313  # Avastin
    RANIBIZUMAB = 314  # Lucentis


ANTIVEGF_TO_ENUM = {
    'aflibercept': AntiVegf.AFLIBERCEPT,
    'eyelea': AntiVegf.AFLIBERCEPT,
    'bevacizumab': AntiVegf.BEVACIZUMAB,
    'avastin': AntiVegf.BEVACIZUMAB,
    'ranibizumab': AntiVegf.RANIBIZUMAB,
    'ranibuzumab': AntiVegf.RANIBIZUMAB,
    'lucentis': AntiVegf.RANIBIZUMAB,
    'anti vegf': AntiVegf.YES  # '-' is removed by `common.drug.shared.get_standardized_name` before lookup
}

ANTIVEGF_PAT = build_pattern_from_dict(ANTIVEGF_TO_ENUM)
ANTIVEGF_RX = build_regex_from_dict(ANTIVEGF_TO_ENUM)


def rename_antivegf(val: AntiVegf) -> int:
    # convert to output values
    match val:
        case AntiVegf.BEVACIZUMAB:
            return 1
        case AntiVegf.AFLIBERCEPT:
            return 2
        case AntiVegf.RANIBIZUMAB:
            return 3
        case AntiVegf.YES:
            return 4
        case _:
            return val.value
