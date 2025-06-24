import enum
import re

from eye_extractor.nlp.negate.negation import is_negated
from eye_extractor.laterality import create_new_variable
from eye_extractor.sections.document import Document
from eye_extractor.sections.patterns import SectionName


class DiscPallor(enum.IntEnum):
    UNKNOWN = -1
    NO = 0
    YES = 1


DISC_PALLOR_PAT = re.compile(
    rf'\bpallor\b',  # unlikely 'atrophy', this tends to be PPA
    re.I
)

DISC_ATROPHY_PAT = re.compile(
    rf'\boptic\W*disc\W*atroph\w*',
    re.I
)


def extract_disc_pallor(doc: Document):
    """
    Building disc pallor variable for glaucoma.

    :param text:
    :param headers:
    :param lateralities:
    :return:
    """
    data = []
    for section in doc.iter_sections(
            SectionName.OPTIC_NERVE, SectionName.CUP_DISC, SectionName.CUP_DISC_OS, SectionName.CUP_DISC_OD,
    ):
        for pat_label, pat, value in [
            ('DISC_PALLOR_PAT', DISC_PALLOR_PAT, DiscPallor.YES),
            ('DISC_ATROPHY_PAT', DISC_ATROPHY_PAT, DiscPallor.YES),
        ]:
            for result in _extract_disc_pallor(pat_label, pat, value, section.text, section.name,
                                               section.lateralities, section.known_laterality):
                data.append(result)
    for result in _extract_disc_pallor(
            'DISC_ATROPHY_PAT', DISC_ATROPHY_PAT, DiscPallor.YES, doc.get_text(), 'ALL',
            lateralities=doc.get_lateralities(),
    ):
        data.append(result)
    return data


def _extract_disc_pallor(pat_label, pat, value, sect_text, sect_name, lateralities, known_lat=None):
    for m in pat.finditer(sect_text):
        negword = is_negated(m, sect_text)
        yield create_new_variable(
            sect_text, m, lateralities, 'disc_pallor_glaucoma', {
                'value': DiscPallor.NO if negword else value,
                'term': m.group(),
                'label': 'no' if negword else value.name.lower(),
                'negated': negword,
                'regex': pat_label,
                'source': sect_name,
            },
            known_laterality=None,  # C/D often has OS or OD in title
        )
