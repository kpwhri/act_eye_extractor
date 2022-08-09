import enum
import re

from eye_extractor.common.negation import is_negated
from eye_extractor.laterality import create_new_variable


class DiscPallor(enum.IntEnum):
    UNKNOWN = -1
    NO = 0
    YES = 1


DISC_PALLOR_PAT = re.compile(
    rf'\bpallor\b',  # unlikely 'atrophy', this tends to be PPA
    re.I
)


def extract_disc_pallor(text, *, headers=None, lateralities=None):
    """
    Building disc pallor variable for glaucoma.

    :param text:
    :param headers:
    :param lateralities:
    :return:
    """
    data = []
    if headers:
        for sect_name, sect_text in headers.iterate(
                'OPTIC NERVE', 'C/D'
        ):
            for pat_label, pat, value in [
                ('DISC_PALLOR_PAT', DISC_PALLOR_PAT, DiscPallor.YES),
            ]:
                for m in pat.finditer(sect_text):
                    negword = is_negated(m, sect_text, {'no', 'not', 'or', 'without'})
                    data.append(
                        create_new_variable(
                            sect_text, m, lateralities, 'disc_pallor_glaucoma', {
                                'value': DiscPallor.NO if negword else value,
                                'term': m.group(),
                                'label': 'no' if negword else value.name.lower(),
                                'negated': negword,
                                'regex': pat_label,
                                'source': sect_name,
                            }
                        )
                    )
    return data
