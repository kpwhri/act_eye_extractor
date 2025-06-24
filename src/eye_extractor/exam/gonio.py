import enum
import re

from eye_extractor.nlp.negate.negation import is_negated, has_before, NEGWORD_SET
from eye_extractor.laterality import create_new_variable
from eye_extractor.sections.document import Document
from eye_extractor.sections.patterns import SectionName


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
    rf'close(?:ure|d)?'
    rf')\b',
    re.I
)

OPEN_4_PAT = re.compile(
    rf'\b(?:'
    rf'open(?:ed)?'
    rf'|4'
    rf'|iv'
    rf')\b',
    re.I
)

CLOSED_0_PAT = re.compile(
    rf'\b(?:'
    rf'close(?:ure|d)?'
    rf'|0'
    rf')\b',
    re.I
)


def extract_gonio(doc: Document):
    """
    Extract open/closed result of gonioscopy
    :param text:
    :param headers:
    :param lateralities:
    :return:
    """
    data = []

    for section in doc.iter_sections(SectionName.ANGLE, SectionName.GONIOSCOPY):
        for pat, pat_label, value in [
            (OPEN_4_PAT, 'OPEN_4_PAT', Gonio.OPEN),
            (CLOSED_0_PAT, 'CLOSED_0_PAT', Gonio.CLOSED),
        ]:
            for m in pat.finditer(section.text):
                negword = is_negated(m, section.text, NEGWORD_SET | {'such'})
                data.append(
                    create_new_variable(section.text, m, section.lateralities, 'gonio', {
                        'value': Gonio.NONE if negword else value,
                        'term': m.group(),
                        'label': 'no' if negword else 'yes',
                        'negated': negword,
                        'regex': pat_label,
                        'source': section.name,
                    })
                )

    for gl_pat, pat_label, value in [
        (OPEN_PAT, 'OPEN_PAT', Gonio.OPEN),
        (CLOSED_PAT, 'CLOSED_PAT', Gonio.CLOSED),
    ]:
        for m in gl_pat.finditer(doc.get_text()):
            matchedtext = m.group()
            if not has_before(m.start(), doc.get_text(), {'gonio', 'gonioscopy'},
                              word_window=5, skip_n_boundary_chars=1):
                continue
            negword = is_negated(m, doc.get_text())
            data.append(
                create_new_variable(doc.get_text(), m, doc.get_lateralities(), 'gonio', {
                    'value': Gonio.NONE if negword else value,
                    'term': matchedtext,
                    'label': 'no' if negword else 'yes',
                    'negated': negword,
                    'regex': pat_label,
                    'source': 'ALL',
                })
            )
    return data
