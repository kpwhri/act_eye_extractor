import enum
import re

from eye_extractor.common.negation import is_negated, has_before
from eye_extractor.laterality import build_laterality_table, create_new_variable


class Gonio(enum.IntEnum):
    UNKNOWN = -1
    NONE = 0
    OPEN = 1
    CLOSED = 2


OPEN_PAT = re.compile(  # make more specific? this will likely be expensive
    rf'\b(?:'
    rf'open(?:ed)?'
    rf')\b',
    re.I
)

CLOSED_PAT = re.compile(
    rf'\b(?:'
    rf'closed?'
    rf')\b',
    re.I
)


def extract_gonio(text, *, headers=None, lateralities=None):
    """
    Extract open/closed result of gonioscopy
    :param text:
    :param headers:
    :param lateralities:
    :return:
    """
    lateralities = lateralities or build_laterality_table(text)
    data = []

    if headers:  # look for 'suspect', etc. in glaucoma section(s)
        for sect_name in ['GONIO', 'GONIOSCOPY']:
            if section_text := headers.get(sect_name, None):
                section_lateralities = build_laterality_table(section_text)
                for pat, pat_label, value in [
                    (OPEN_PAT, 'OPEN_PAT', Gonio.OPEN),
                    (CLOSED_PAT, 'CLOSED_PAT', Gonio.CLOSED),
                ]:
                    for m in pat.finditer(section_text):
                        negword = is_negated(m, section_text, {'no', 'or', 'without', 'not'})
                        data.append(
                            create_new_variable(section_text, m, section_lateralities, 'gonio', {
                                'value': Gonio.NONE if negword else value,
                                'term': m.group(),
                                'label': 'no' if negword else 'yes',
                                'negated': negword,
                                'regex': pat_label,
                                'source': sect_name,
                            })
                        )

    for gl_pat, pat_label, value in [
        (OPEN_PAT, 'OPEN_PAT', Gonio.OPEN),
        (CLOSED_PAT, 'CLOSED_PAT', Gonio.CLOSED),
    ]:
        for m in gl_pat.finditer(text):
            matchedtext = m.group()
            if not has_before(m.start(), text, {'gonio', 'gonioscopy'}, word_window=5, skip_n_boundary_chars=1):
                continue
            negword = is_negated(m, text, {'no', 'or', 'without', 'not'})
            data.append(
                create_new_variable(text, m, lateralities, 'gonio', {
                    'value': Gonio.NONE if negword else value,
                    'term': matchedtext,
                    'label': 'no' if negword else 'yes',
                    'negated': negword,
                    'regex': pat_label,
                    'source': 'ALL',
                })
            )
    return data
