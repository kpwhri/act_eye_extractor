import enum
import re

from eye_extractor.common.date import parse_date_after
from eye_extractor.nlp.negate.negation import is_negated
from eye_extractor.laterality import create_new_variable
from eye_extractor.sections.document import Document


class Laser(enum.IntEnum):
    UNKNOWN = -1
    NONE = 0
    LASER = 1  # laser photocoagulation
    PHOTODYNAMIC = 2  # PDT
    THERMAL = 3
    OTHER = 4
    UNSPECIFIED = 5
    # MACUGEN = 4  # pegaptanib sodium injection


LASER_PAT = re.compile(
    rf'\blaser(?:\W*photo\W?coagulation)?\b',
    re.I
)

PHOTODYNAMIC_PAT = re.compile(  # verb + med
    rf'\b(?:'
    rf'pdt'
    rf'|photodynamic(?:\W*therapy)?'
    rf')\b',
    re.I
)

THERMAL_PAT = re.compile(  # verb + med
    rf'\b(?:'
    rf'thermal(?:\W*laser)?'
    rf')\b',
    re.I
)


def extract_lasertype(doc: Document):
    """
    Only look within particular headers. Often discussed as an 'option' in a PLAN-like section.

    :param doc:
    :return:
    """
    data = []
    if doc.sections:
        for section in doc.iter_sections('assessment', 'impression', 'comments'):
            for pat_label, pat, value in [
                ('LASER_PAT', LASER_PAT, Laser.LASER),
                ('PHOTODYNAMIC_PAT', PHOTODYNAMIC_PAT, Laser.PHOTODYNAMIC),
                ('THERMAL_PAT', THERMAL_PAT, Laser.THERMAL),
            ]:
                for m in pat.finditer(section.text):
                    negword = is_negated(m, section.text)
                    date = parse_date_after(m, section.text)
                    data.append(
                        create_new_variable(
                            section.text, m, section.lateralities, 'amd_lasertype', {
                                'value': Laser.NONE if negword else value,
                                'term': m.group(),
                                'label': 'no' if negword else value.name,
                                'negated': negword,
                                'regex': pat_label,
                                'source': section.name,
                                'date': date,
                            }
                        )
                    )
    return data
