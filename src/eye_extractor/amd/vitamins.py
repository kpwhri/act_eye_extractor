import enum
import re

from eye_extractor.nlp.negate.negation import is_negated
from eye_extractor.sections.document import Document


class Vitamin(enum.IntEnum):
    UNKNOWN = -1
    NO = 0
    YES = 1


vitamins = r'(?:ocuvite|preservision|areds2?|icaps?)'

CONTINUE_VITAMIN_PAT = re.compile(  # verb + med
    rf'\b'
    rf'(?:continu\w+|on|(?:us|tak)(?:ing|es?))\W*'
    rf'{vitamins}'
    rf'\b',
    re.I
)

VITAMIN_PAT = re.compile(
    rf'\b{vitamins}\b',
    re.I
)


def extract_amd_vitamin(doc: Document):
    """

    :param text:
    :param headers:
    :param lateralities: not required as this is an oral vitamin
    :return:
    """
    # TODO: handle 'smart phrase' fluff (e.g., provider says yes, but tech no)
    data = []
    if doc.sections:
        for section in doc.iter_sections('eye_meds', 'meds', 'plan'):  # TODO: other sections?
            for m in VITAMIN_PAT.finditer(section.text):
                negword = is_negated(m, section.text)
                data.append(
                    {'amd_vitamin': {
                        'value': Vitamin.NO if negword else Vitamin.YES,
                        'term': m.group(),
                        'label': 'no' if negword else 'yes',
                        'negated': negword,
                        'regex': 'VITAMIN_PAT',
                        'source': section.name,
                    }}
                )
    for m in CONTINUE_VITAMIN_PAT.finditer(doc.text):
        negword = is_negated(m, doc.text)
        data.append(
            {'amd_vitamin': {
                'value': Vitamin.NO if negword else Vitamin.YES,
                'term': m.group(),
                'label': 'no' if negword else 'yes',
                'negated': negword,
                'regex': 'CONTINUE_VITAMIN_PAT',
                'source': 'ALL',
            }}
        )
    return data
