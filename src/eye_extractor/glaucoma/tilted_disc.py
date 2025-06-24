import re

from eye_extractor.nlp.negate.negation import is_negated, has_before, has_after
from eye_extractor.laterality import create_new_variable
from eye_extractor.sections.document import Document

tilt = r'(?:tilt\w*)'

TILTED_PLUS_PAT = re.compile(
    fr'(?:'
    fr'(?:myop\w*|dis[ck]s?)\W*{tilt}\b'
    fr'|'
    fr'\b{tilt}\W*(?:dis[ck]s?|myop\w*)'
    fr')',
    re.I
)

TILTED_PAT = re.compile(
    rf'\b(?:tilt(?:ed|ing)?)\b'
)


def extract_tilted_disc(doc: Document):
    """

    :param text:
    :param headers:
    :param lateralities:
    :return:
    """
    data = []

    text = doc.get_text()
    lateralities = doc.get_lateralities()
    for m in TILTED_PLUS_PAT.finditer(text):
        negword = is_negated(m, text)
        data.append(
            create_new_variable(text, m, doc.get_lateralities(), 'tilted_disc', {
                'value': 0 if negword else 1,
                'term': m.group(),
                'label': 'no' if negword else 'yes',
                'negated': negword,
                'regex': 'TILTED_PLUS_PAT',
                'source': 'ALL',
            })
        )
    if not data:
        pos_terms = {'saucer', 'saucered', 'disc', 'discs', 'od', 'os'}
        for m in TILTED_PAT.finditer(text):
            negword = is_negated(m, text)
            if (
                    has_before(m.start(), text, {'head', 'glasses', 'to'}, word_window=5)
                    or has_after(m.end(), text, {'head', 'glasses'}, word_window=5)
            ):
                continue
            elif (
                    has_before(m.start(), text, pos_terms, word_window=5, skip_n_boundary_chars=1)
                    or has_after(m.end(), text, pos_terms, word_window=5, skip_n_boundary_chars=1)
            ):
                data.append(
                    create_new_variable(text, m, lateralities, 'tilted_disc', {
                        'value': 0 if negword else 1,
                        'term': m.group(),
                        'label': 'no' if negword else 'yes',
                        'negated': negword,
                        'regex': 'TILTED_PAT',
                        'source': 'ALL',
                    })
                )
    return data
