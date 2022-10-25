import re

from eye_extractor.common.drug.drops import GenericDrop, DROP_TO_ENUM, DROPS_RX
from eye_extractor.common.drug.shared import get_standardized_name
from eye_extractor.common.negation import is_negated, NEGWORDS

eye_meds_rx = r'(?:opt\w*|ophth\w*|eye)\W*med\w*'
NO_OPT_MED_RX = re.compile(
    rf'(?:'
    rf'(no)\s*active\s*{eye_meds_rx}'
    rf'|{eye_meds_rx}\W*(no(?:t|ne)?)\b'
    rf')',
    re.I
)


def extract_glaucoma_drops(text, *, headers=None, lateralities=None):
    varname = 'glaucoma_rx_{}'
    data = []
    if m := NO_OPT_MED_RX.search(text):
        data.append({
            varname.format(GenericDrop.NONE.name.lower()): {
                'value': 1,
                'term': m.group(1),
                'regex': 'NO_OPT_MED_RX',
                'source': 'ALL',
            }
        })
        return data
    for m in DROPS_RX.finditer(text):
        # TODO: confirm presence of 'current medications'
        negword = is_negated(m, text)
        term = m.group()
        standardized_name = get_standardized_name(term)
        for gd in DROP_TO_ENUM[standardized_name]:
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
