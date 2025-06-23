import re

from eye_extractor.dr.hemorrhage_type import HEME_NOS_PAT
from eye_extractor.nlp.negate.negation import has_before, is_negated, is_post_negated, NEGWORD_UNKNOWN_PHRASES
from eye_extractor.laterality import build_laterality_table, create_new_variable
from eye_extractor.sections.document import Document

DIABETIC_RETINOPATHY_PATS = [
    ('disc_edema_DR', re.compile(
        r'\b('
        r'disc edema'
        r')\b',
        re.I
    )),
    ('hemorrhage_dr', HEME_NOS_PAT),
    ('dr_laser_scars', re.compile(
        r'\b('
        r'laser scars?'
        r')\b',
        re.I
    )),
    ('laserpanret_photocoag', re.compile(
        r'\b('
        r'prp|laser panretinal photo\W?coagulation|scatter photo\W?coagulation'
        r')\b',
        re.I
    )),
    ('drtreatment', re.compile(
        r'\b('
        r'PRP|pan retinal photocoagulation|Pars plana vitrectomy'
        r')\b',
        re.I
    )),
    ('dmacedema_clinsignif', re.compile(
        r'\b('
        r'CSME|clinically significant (diabetic )?macular edema'
        r')\b',
        re.I
    )),
    ('oct_centralmac', re.compile(
        r'\b('
        r'CMT|central macular thickness|macular thickness|thickness of macula'
        r')\b',
        re.I
    )),
]


def get_dr_binary(doc: Document):
    data = []
    for variable, PAT in DIABETIC_RETINOPATHY_PATS:
        for m in PAT.finditer(doc.get_text()):
            if variable == 'hemorrhage_dr':
                negated = is_negated(m, doc.get_text(), word_window=3, return_unknown=True)
                if negated in NEGWORD_UNKNOWN_PHRASES:  # e.g., 'no new' -> UNKNOWN
                    continue
                if has_before(m if isinstance(m, int) else m.start(),
                              doc.get_text(),
                              terms={'hx', 'h/o', 'resolved'},
                              boundary_chars='',
                              word_window=6):
                    continue
            else:
                negated = is_negated(m, doc.get_text(), word_window=4)
                if not negated:
                    negated = is_post_negated(m, doc.get_text(), {'or'}, word_window=2)
            data.append(
                create_new_variable(doc.get_text(), m, doc.get_lateralities(), variable, {
                    'value': 0 if negated else 1,
                    'term': m.group(),
                    'label': 'no' if negated else 'yes',
                    'negated': negated,
                    'regex': f'{variable}_PAT',
                    'source': 'ALL'
                })
            )
    return data
