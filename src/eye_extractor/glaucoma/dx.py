import enum
import re

from eye_extractor.nlp.negate.negation import has_before, is_negated, has_after
from eye_extractor.laterality import build_laterality_table, create_new_variable
from eye_extractor.sections.document import Document
from eye_extractor.sections.patterns import SectionName


class GlaucomaDx(enum.IntEnum):
    UNKNOWN = -1
    NONE = 0
    PREGLAUCOMA = 101
    SUSPECT = 102
    CUPPING = 103
    OCULAR_HYPERTENSIVE = 104
    GLAUCOMA = 110


class GlaucomaType(enum.IntEnum):
    UNKNOWN = -1
    NONE = 0
    POAG = 1
    NTG = 2
    LTG = 3
    PXG = 4  # exfoliative
    PG = 5  # pigmentary
    ACG = 6
    ICE = 7
    CONGENITAL = 8
    NV = 9
    UVEITIC = 10
    STEROID = 11
    PREGLAUCOMA = 101
    SUSPECT = 102
    CUPPING = 103
    OCULAR_HYPERTENSIVE = 104
    GLAUCOMA = 110


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
    rf'\b(?:pxg|p[de]x|pxf|xfs|peg)\b'
    rf'|'
    rf'capsulare'
    rf'|'
    rf'(?:pseudo\W*)?exfoll?iat\w*'
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
    rf'(?:angle\W*clos[ue]\w*|(?:clos[ue]\w*|narrow)\W*angle)'
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

TRAUMATIC_PAT = re.compile(
    rf'(?:'
    rf'trauma\w*'
    rf')',
    re.I
)

SUSPECT_PAT = re.compile(
    rf'(?:'
    rf'\b(?:suspect)\b'
    rf')',
    re.I
)

CUPPING_PAT = re.compile(
    rf'(?:'
    rf'\b(?:cupping)\b'
    rf')',
    re.I
)

OCULAR_HYPERTENSIVE_PAT = re.compile(
    rf'(?:'
    rf'\bocul\w+\W*hypertens\w+'
    rf'|'
    rf'\bohtn\b'
    rf')',
    re.I
)


def extract_glaucoma_dx(doc: Document):
    """
    1. Try to identify secondary glaucoma
    2. Try to identify primaries
    3. Look for 'suspect', etc., in glaucoma section
    4. Look for 'suspect', etc., everywhere
    :param text:
    :param headers:
    :param lateralities:
    :return: ordered result of variables -- should only take the first
    """
    data = []
    text = doc.get_text()
    lateralities = doc.get_lateralities()
    # secondary glaucoma first (nb: these might appear alongside primary)
    for gl_pat, pat_label, value in [
        (PXG_PAT, 'PXG_PAT', GlaucomaType.PXG),
        (PG_PAT, 'PG_PAT', GlaucomaType.PG),
        (ICE_PAT, 'ICE_PAT', GlaucomaType.ICE),
        (CONGENITAL_PAT, 'CONGENITAL_PAT', GlaucomaType.CONGENITAL),
        (NV_PAT, 'NV_PAT', GlaucomaType.NV),
        (UVEI_PAT, 'UVEI_PAT', GlaucomaType.UVEITIC),
        (STEROID_PAT, 'STEROID_PAT', GlaucomaType.STEROID),
        (NTG_PAT, 'NTG_PAT', GlaucomaType.NTG),
        (LTG_PAT, 'LTG_PAT', GlaucomaType.LTG),
        # primary
        (ACG_PAT, 'ACG_PAT', GlaucomaType.ACG),
        (POAG_PAT, 'POAG_PAT', GlaucomaType.POAG),
    ]:
        for m in gl_pat.finditer(text):
            matchedtext = m.group()
            # needs to mention glaucoma/syndrome
            if matchedtext.endswith('g'):
                pass
            elif 'glaucoma' in matchedtext.lower() or 'syndrome' in matchedtext.lower():
                pass
            elif has_before(m.start(), text, {'glauc', 'gl', 'glaucoma', 'syndrome'},
                            word_window=3, skip_n_boundary_chars=1):
                pass
            elif has_after(m.end(), text, {'glauc', 'gl', 'glaucoma', 'syndrome'}, word_window=3):
                pass
            else:
                continue  # no mention of glaucoma/syndrome
            negword = is_negated(m, text)
            data.append(
                create_new_variable(text, m, lateralities, 'glaucoma_type', {
                    'value': GlaucomaType.NONE if negword else value,
                    'term': matchedtext,
                    'label': 'no' if negword else 'yes',
                    'negated': negword,
                    'regex': pat_label,
                    'source': 'ALL',
                })
            )

    # look for 'suspect', etc. in glaucoma section(s)
    for section in doc.iter_sections(SectionName.GLAUCOMA_TYPE, SectionName.GLAUCOMA,
                                     SectionName.GLAUCOMA_FLOWSHEET):
        for pat, pat_label, value in [
            (SUSPECT_PAT, 'SUSPECT_PAT', GlaucomaDx.SUSPECT),
            (OCULAR_HYPERTENSIVE_PAT, 'OCULAR_HYPERTENSIVE_PAT', GlaucomaDx.OCULAR_HYPERTENSIVE),
            (CUPPING_PAT, 'CUPPING_PAT', GlaucomaDx.CUPPING),
        ]:
            for m in pat.finditer(section.text):
                negword = is_negated(m, section.text)
                data.append(
                    create_new_variable(section.text, m, section.lateralities, 'glaucoma_dx', {
                        'value': 0 if negword else value,
                        'term': m.group(),
                        'label': 'no' if negword else 'yes',
                        'negated': negword,
                        'regex': pat_label,
                        'source': section.name,
                    })
                )

    for m in SUSPECT_PAT.finditer(text):
        if not has_before(m.start(), text, {'glaucoma'}, word_window=5, skip_n_boundary_chars=1):
            continue  # TODO: exclude family history
        negword = is_negated(m, text)
        data.append(
            create_new_variable(text, m, lateralities, 'glaucoma_dx', {
                'value': 0 if negword else GlaucomaDx.SUSPECT,
                'term': m.group(),
                'label': 'no' if negword else 'yes',
                'negated': negword,
                'regex': 'SUSPECT_PAT',
                'source': 'ALL',
            })
        )
    return data
