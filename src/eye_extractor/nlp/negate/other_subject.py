import re
from typing import Match

from eye_extractor.nlp.negate.negation import is_negated

FAMILY_RELATIONS = [
    'brother', 'sister', 'mother', 'father', 'aunt', 'grandmother', 'grandma',
    'bro', 'sis', 'mom', 'mama', 'dad', 'papa', 'uncle', 'grandfather', 'grandpa',
]
FAMILY_RELATION_PAT = re.compile(rf'(?:{"|".join(FAMILY_RELATIONS)})', re.I)

OTHER_SUBJECT_WORDS = frozenset({'friend'} | set(FAMILY_RELATIONS))


def is_other_subject_before(m: Match | int, text: str,
                            terms: set[str] | frozenset[str] | dict = OTHER_SUBJECT_WORDS,
                            **kwargs):
    return is_negated(m, text, terms, **kwargs)


def is_other_subject_after(m: Match | int, text: str,
                           terms: set[str] | frozenset[str] | dict = OTHER_SUBJECT_WORDS,
                           **kwargs):
    return is_negated(m, text, terms, **kwargs)


def is_other_subject(m: Match | int, text: str):
    return is_other_subject_before(m, text) or is_other_subject_after(m, text)
