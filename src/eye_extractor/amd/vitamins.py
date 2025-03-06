import enum
import re

from eye_extractor.nlp.negate.negation import is_negated


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


def extract_amd_vitamin(text, *, headers=None, lateralities=None):
    """

    :param text:
    :param headers:
    :param lateralities: not required as this is an oral vitamin
    :return:
    """
    # TODO: handle 'smart phrase' fluff (e.g., provider says yes, but tech no)
    data = []
    if headers:
        for sect_name, sect_text in headers.iterate(
                'CURRENT_EYE_MEDICATIONS', 'EYE_MEDICATIONS', 'MEDICATIONS', 'PLAN',
        ):  # TODO: other sections?
            for m in VITAMIN_PAT.finditer(sect_text):
                negword = is_negated(m, sect_text)
                data.append(
                    {'amd_vitamin': {
                        'value': Vitamin.NO if negword else Vitamin.YES,
                        'term': m.group(),
                        'label': 'no' if negword else 'yes',
                        'negated': negword,
                        'regex': 'VITAMIN_PAT',
                        'source': sect_name,
                    }}
                )
    for m in CONTINUE_VITAMIN_PAT.finditer(text):
        negword = is_negated(m, text)
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
