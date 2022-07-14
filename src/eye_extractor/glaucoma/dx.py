import enum
import re

from eye_extractor.common.negation import has_before, is_negated
from eye_extractor.laterality import build_laterality_table, create_new_variable


class GlaucomaDx(enum.IntEnum):
    UNKNOWN = -1
    NONE = 0
    PREGLAUCOMA = 1
    GLAUCOMA_SUSPECT = 2
    GLAUCOMA = 3


class GlaucomaType(enum.IntEnum):
    UNKNOWN = -1
    NONE = 0
    POAG = 1
    NTG = 2
    LTG = 3
    PXG = 4
    PG = 5  # pigmentary
    ACG = 6
    ICE = 7
    CONGENITAL = 8
    NV = 9
    UVEI = 10
    STEROID = 11


POAG_PAT = re.compile(
    rf'(?:'
    rf'\bp?oag\b'
    rf'|'
    rf'(?:primary\W*)?open\W*angle'
    rf')',
    re.I
)

NTG_PAT = re.compile(
    rf'(?:'
    rf'\bntg\b'
    rf'|'
    rf'normal\W*(?:pressure|tension)'
    rf')',
    re.I
)

LTG_PAT = re.compile(
    rf'(?:'
    rf'\bltg\b'
    rf'|'
    rf'low\W*(?:pressure|tension)'
    rf')',
    re.I
)

PXG_PAT = re.compile(
    rf'(?:'
    rf'\b(?:pxg|pex|pxf|xfs)\b'
    rf'|'
    rf'capsulare'
    rf'|'
    rf'(?:pseudo\W*)exfoliat\w*'
    rf')',
    re.I
)

PG_PAT = re.compile(
    rf'(?:'
    rf'\b(?:pg|pds)\b'
    rf'|'
    rf'(?:pigment\w*|pigment\w* dispersion)'
    rf')',
    re.I
)

ACG_PAT = re.compile(
    rf'(?:'
    rf'\b(?:acg)\b'
    rf'|'
    rf'(?:angle\W*clos[ue]\w*|clos[ue]\w*\W*angle)'
    rf')',
    re.I
)

CONGENITAL_PAT = re.compile(
    rf'(?:'
    rf'(?:childhood|congenital)'
    rf')',
    re.I
)

ICE_PAT = re.compile(
    rf'(?:'
    rf'\bice\b'
    rf'|'
    rf'irid\w*\W*cornea\w*\W*endo\w+'
    rf')',
    re.I
)

NV_PAT = re.compile(
    rf'(?:'
    rf'neo\W*vascular'
    rf')',
    re.I
)

UVEI_PAT = re.compile(
    rf'(?:'
    rf'uveitic'
    rf')',
    re.I
)

STEROID_PAT = re.compile(
    rf'(?:'
    rf'steroid\W*(?:induc|respon[ds])\w*'
    rf')',
    re.I
)

GLAUCOMA_DX_PAT = re.compile(
    rf'(?:'
    rf'\b(?:gl|poag|ntg|ltg|pxg)\b'
    rf'|'
    rf'(?:pigmentary)\W*glauc'
    rf')'
)


def get_glaucoma_dx(text, *, headers=None, lateralities=None):
    lateralities = lateralities or build_laterality_table(text)
    data = []
    if headers:
        for sect_name in ['TYPE OF GLAUCOMA', 'GLAUCOMA FLOWSHEET']:
            if section_text := headers.get(sect_name, None):
                section_lateralities = build_laterality_table(section_text)
                for m in GLAUCOMA_DX_PAT.finditer(section_text):
                    negword = is_negated(m, section_text, {'no', 'or', 'without'})
                    data.append(
                        create_new_variable(text, m, section_lateralities, 'glaucoma_dx', {
                            'value': 0 if negword else 1,
                            'term': m.group(),
                            'label': 'no' if negword else 'yes',
                            'negated': negword,
                            'regex': 'GLAUCOMA_DX_PAT',
                            'source': sect_name,
                        })
                    )
    if not data:  # no results yet
        for m in GLAUCOMA_DX_PAT.finditer(text):
            if not has_before(m.start(), text, {'glaucoma'}, word_window=5, skip_n_boundary_chars=1):
                continue  # TODO: exclude family history
            negword = is_negated(m, text, {'no', 'or', 'without'})
            data.append(
                create_new_variable(text, m, lateralities, 'glaucoma_dx', {
                    'value': 0 if negword else 1,
                    'term': m.group(),
                    'label': 'no' if negword else 'yes',
                    'negated': negword,
                    'regex': 'GLAUCOMA_DX_PAT',
                    'source': 'ALL',
                })
            )
    return data
