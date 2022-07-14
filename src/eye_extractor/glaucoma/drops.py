import enum
import re

from eye_extractor.common.negation import is_negated
from eye_extractor.laterality import build_laterality_table


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


DRUG_TO_ENUM = {
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

eye_meds_rx = r'(?:opt\w*|ophth\w*|eye)\W*med\w*'
NO_OPT_MED_RX = re.compile(
    rf'(?:'
    rf'(no)\s*active\s*{eye_meds_rx}'
    rf'|{eye_meds_rx}\W*(no(?:t|ne)?)\b'
    rf')',
    re.I
)
DROPS_RX = re.compile('|'.join(DRUG_TO_ENUM.keys()).replace(' ', r'\W*'), re.I)


def get_standardized_name(term):
    return re.sub(r'[^A-Za-z]+', ' ', term).lower()


def extract_glaucoma_drops(text, *, headers=None, lateralities=None):
    lateralities = lateralities or build_laterality_table(text)
    varname = 'glaucoma_rx_{}'
    data = []
    if m := NO_OPT_MED_RX.search(text):
        data.append(
            {
                varname.format(GenericDrop.NONE.name.lower()): {
                    'value': 1,
                    'term': m.group(1),
                    'regex': 'NO_OPT_MED_RX',
                    'source': 'ALL',
                }
            }
        )
        return data
    for m in DROPS_RX.finditer(text):
        # TODO: confirm presence of 'current medications'
        negword = is_negated(m, text, {'no', 'or', 'without'})
        term = m.group()
        standardized_name = get_standardized_name(term)
        for gd in DRUG_TO_ENUM[standardized_name]:
            data.append(
                {varname.format(gd.name.lower()): {
                    'value': 0 if negword else 1,
                    'term': term,
                    'standard': standardized_name,
                    'label': 'no' if negword else 'yes',
                    'negated': negword,
                    'regex': 'DROPS_RX',
                    'source': 'ALL',
                }}
            )
    # if headers:  # TODO: just look within medications section?
    #     if section_text := headers.get('SECTION', None):
    #         lateralities = build_laterality_table(section_text)
    #         for m in NEW_SECTION_PAT.finditer(text):
    #             if is_negated(m, text, {'no', 'or'}):
    #                 continue
    #             negword = is_negated(m, text, {'no', 'or', 'without'})
    #             data.append(
    #                 create_new_variable(text, m, lateralities, varname, {
    #                     'value': 0 if negword else 1,
    #                     'term': m.group(),
    #                     'label': 'no' if negword else 'yes',
    #                     'negated': negword,
    #                     'regex': 'NEW_SECTION_PAT',
    #                     'source': 'SECTION',
    #                 })
    #             )
    return data
