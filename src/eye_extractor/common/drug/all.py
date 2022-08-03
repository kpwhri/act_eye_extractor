from eye_extractor.common.drug.antivegf import ANTIVEGF_TO_ENUM
from eye_extractor.common.drug.drops import DROP_TO_ENUM
from eye_extractor.common.drug.shared import build_pattern_from_dict, build_regex_from_dict

ALL_TO_ENUM = DROP_TO_ENUM | ANTIVEGF_TO_ENUM
ALL_DRUG_PAT = build_pattern_from_dict(ALL_TO_ENUM)
ALL_DRUG_RX = build_regex_from_dict(ALL_TO_ENUM)
