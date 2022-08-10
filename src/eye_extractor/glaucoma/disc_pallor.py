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

DISC_ATROPHY_PAT = re.compile(
    rf'\boptic\W*disc\W*atroph\w*',
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
                ('DISC_ATROPHY_PAT', DISC_ATROPHY_PAT, DiscPallor.YES),
            ]:
                for result in _extract_disc_pallor(pat_label, pat, value, sect_text, sect_name):
                    data.append(result)
    for result in _extract_disc_pallor(
            'DISC_ATROPHY_PAT', DISC_ATROPHY_PAT, DiscPallor.YES, text, 'ALL',
            lateralities=lateralities
    ):
        data.append(result)
    return data


def _extract_disc_pallor(pat_label, pat, value, sect_text, sect_name, lateralities=None):
    for m in pat.finditer(sect_text):
        negword = is_negated(m, sect_text, {'no', 'not', 'or', 'without'})
        yield create_new_variable(
            sect_text, m, lateralities, 'disc_pallor_glaucoma', {
                'value': DiscPallor.NO if negword else value,
                'term': m.group(),
                'label': 'no' if negword else value.name.lower(),
                'negated': negword,
                'regex': pat_label,
                'source': sect_name,
            }
        )
