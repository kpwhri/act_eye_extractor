import enum

from eye_extractor.common.drug.shared import build_regex_from_dict, build_pattern_from_dict


class GenericDrop(enum.IntEnum):
    UNKNOWN = -1
    NONE = 0
    DORZOLAMIDE = 1
    ECHOTHIOPHATE_IODIDE = 2
    TIMOLOL = 3
    ACETYLCHOLINE = 4
    LATANOPROSTENE_BUNOD = 5
    APRACLONIDINE = 6
    CARBACHOL = 7
    NETARSUDIL = 8
    METIPRANOLOL = 9
    BIMATOPROST = 10
    BRIMONIDINE = 11
    CARTEOLOL = 12
    EPINEPHRINE = 13
    LATANOPROST = 14
    BETAXOLOL = 15
    UNOPROSTONE = 16
    TRAVOPROST = 17
    DIPIVEFRIN = 18
    LEVOBUNOLOL = 19
    PILOCARPINE = 20
    PHYSOSTIGMINE = 21
    BRINZOLAMIDE = 22
    TAFLUPROST = 23


DROP_TO_ENUM = {
    # prescription
    'rhopressa': [GenericDrop.NETARSUDIL],
    'simbrinza': [GenericDrop.BRIMONIDINE, GenericDrop.BRINZOLAMIDE],
    'lumigan': [GenericDrop.BIMATOPROST],
    'combigan': [GenericDrop.BRIMONIDINE, GenericDrop.TIMOLOL],
    'rocklatan': [GenericDrop.LATANOPROST, GenericDrop.NETARSUDIL],
    'zioptan': [GenericDrop.TAFLUPROST],
    'xalatan': [GenericDrop.LATANOPROST],
    'vyzulta': [GenericDrop.LATANOPROSTENE_BUNOD],
    'travatan': [GenericDrop.TRAVOPROST],
    'alphagan': [GenericDrop.BRIMONIDINE],
    'trusopt': [GenericDrop.DORZOLAMIDE],
    'cosopt': [GenericDrop.DORZOLAMIDE, GenericDrop.TIMOLOL],
    'azopt': [GenericDrop.BRINZOLAMIDE],
    'phospholine': [GenericDrop.ECHOTHIOPHATE_IODIDE],
    'istalol': [GenericDrop.TIMOLOL],
    'timoptic': [GenericDrop.TIMOLOL],
    'xelpros': [GenericDrop.LATANOPROST],
    'rescula': [GenericDrop.UNOPROSTONE],
    'propine': [GenericDrop.DIPIVEFRIN],
    'pilopine': [GenericDrop.PILOCARPINE],
    'pilocar': [GenericDrop.PILOCARPINE],
    'optipranolol': [GenericDrop.METIPRANOLOL],
    'ocupress': [GenericDrop.CARTEOLOL],
    'ocu carpine': [GenericDrop.PILOCARPINE],
    'miostat': [GenericDrop.CARBACHOL],
    'miochol': [GenericDrop.ACETYLCHOLINE],
    'izba': [GenericDrop.TRAVOPROST],
    'isopto carpine': [GenericDrop.PILOCARPINE],
    'isopto carbachol': [GenericDrop.CARBACHOL],
    'iopidine': [GenericDrop.APRACLONIDINE],
    'eserine sulfate ophthalmic': [GenericDrop.PHYSOSTIGMINE],
    'epinal': [GenericDrop.EPINEPHRINE],
    'durysta': [GenericDrop.BIMATOPROST],
    'carbastat': [GenericDrop.CARBACHOL],
    'betoptics': [GenericDrop.BETAXOLOL],
    'betoptic s': [GenericDrop.BETAXOLOL],
    'betoptic': [GenericDrop.BETAXOLOL],
    'betimol': [GenericDrop.TIMOLOL],
    'betagan': [GenericDrop.LEVOBUNOLOL],
    # generic
    'dorzolamide': [GenericDrop.DORZOLAMIDE],
    'echothiophate iodide': [GenericDrop.ECHOTHIOPHATE_IODIDE],
    'timolol': [GenericDrop.TIMOLOL],
    'acetylcholine': [GenericDrop.ACETYLCHOLINE],
    'latanoprostene bunod': [GenericDrop.LATANOPROSTENE_BUNOD],
    'apraclonidine': [GenericDrop.APRACLONIDINE],
    'carbachol': [GenericDrop.CARBACHOL],
    'netarsudil': [GenericDrop.NETARSUDIL],
    'metipranolol': [GenericDrop.METIPRANOLOL],
    'bimatoprost': [GenericDrop.BIMATOPROST],
    'brimonidine': [GenericDrop.BRIMONIDINE],
    'carteolol': [GenericDrop.CARTEOLOL],
    'epinephrine': [GenericDrop.EPINEPHRINE],
    'latanoprost': [GenericDrop.LATANOPROST],
    'betaxolol': [GenericDrop.BETAXOLOL],
    'unoprostone': [GenericDrop.UNOPROSTONE],
    'travoprost': [GenericDrop.TRAVOPROST],
    'dipivefrin': [GenericDrop.DIPIVEFRIN],
    'levobunolol': [GenericDrop.LEVOBUNOLOL],
    'pilocarpine': [GenericDrop.PILOCARPINE],
    'physostigmine': [GenericDrop.PHYSOSTIGMINE],
    'brinzolamide': [GenericDrop.BRINZOLAMIDE],
    'tafluprost': [GenericDrop.TAFLUPROST],
}

DROPS_PAT = build_pattern_from_dict(DROP_TO_ENUM)
DROPS_RX = build_regex_from_dict(DROP_TO_ENUM)
