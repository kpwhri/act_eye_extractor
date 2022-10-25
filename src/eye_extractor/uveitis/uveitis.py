import re

from eye_extractor.common.negation import is_negated, is_post_negated
from eye_extractor.laterality import create_new_variable

ALL_UVEITIS_PAT = re.compile(
    r'(?:'
    r'uveitis'
    r'|scleritis'
    r'|iridocyclitis'
    r'|iritis'
    r')',
    re.IGNORECASE
)

UVEITIS_PAT = re.compile(
    # IU and AU do not appear
    # WARN: careful with 'IU' and the unit 'IU' if pursued
    # WARN: AU might also appear under allergies as 'gold'
    r'(?:'
    r'(?:anterior'
    r'|intermediate'
    r'|posterior'
    r'|pan'
    r')\W*'
    r'uveitis'
    r'|scleritis'
    r'|iridocyclitis'
    r'|iritis'
    r')',
    re.I
)


def get_uveitis(text, *, headers=None, lateralities=None):
    data = []
    for pat, label in [
        (UVEITIS_PAT, 'UVEITIS_PAT'),
        (ALL_UVEITIS_PAT, 'ALL_UVEITIS_PAT'),
    ]:
        for m in pat.finditer(text):
            negword = (
                    is_negated(m, text, word_window=4)
                    or is_post_negated(m, text, {'not'}, word_window=3)
            )
            histword = (
                is_negated(m, text, {'hx', 'history'}, word_window=3)
            )
            data.append(
                create_new_variable(text, m, lateralities, 'uveitis_yesno', {
                    'value': 0 if negword else 1,
                    'term': m.group(),
                    'label': 'no' if negword else 'yes',
                    'negated': negword,
                    'historical': histword,
                    'regex': label,
                    'source': 'ALL',
                })
            )
    return data
