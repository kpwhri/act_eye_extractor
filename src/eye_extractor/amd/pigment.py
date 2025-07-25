"""

Summary of Changes:
* Removed pigmentary dispersion (implies glaucoma)
* Removed atrophy ('atrophy' to nonspecific except for geographic atrophy)

"""
import re

from eye_extractor.amd.utils import run_on_macula
from eye_extractor.nlp.negate.negation import is_negated, is_post_negated
from eye_extractor.laterality import create_new_variable, laterality_pattern, lat_lookup
from eye_extractor.sections.document import Document

change = r'(?:chang|disrupt|dispers|migrat|abnormal|clump|mottl|pigment)\w*'
pigment = r'(?:(?:hyper)?pigment\w*|\brpe\b)'

PIGMENTARY_PAT = re.compile(
    rf'(?:'
    rf'{pigment}\s*{change}'
    rf'|{change}\s*(\w+\s+){{0,3}}{pigment}'
    rf')',
    re.IGNORECASE
)

ATROPHY_PAT = re.compile(
    rf'(?:'
    rf'{change}\s*(?P<lat>{laterality_pattern})'
    rf')',
    re.IGNORECASE
)


def get_pigmentary_changes(doc: Document):
    return run_on_macula(
        macula_func=_get_pigmentary_changes,
        default_func=_get_pigmentary_changes,
        doc=doc,
    )


def _get_pigmentary_changes(text, lateralities, source):
    data = []
    for m in PIGMENTARY_PAT.finditer(text):
        # TODO: cannot appear in assessment section -- specifically exclude?
        if is_post_negated(m, text, terms={'syndrome', 'syndromes'}):
            continue  # pigment dispersion syndrome is a glaucoma
        negword = is_negated(m, text, word_window=3)
        data.append(
            create_new_variable(text, m, lateralities, 'pigmentchanges', {
                'value': 0 if negword else 1,
                'term': m.group(),
                'label': 'no' if negword else 'yes',
                'negated': negword,
                'regex': 'PIGMENTARY_PAT',
                'source': source,
            })
        )
    for m in ATROPHY_PAT.finditer(text):
        negword = is_negated(m, text, word_window=3)
        lat = lat_lookup(m, group='lat')
        data.append(
            create_new_variable(text, m, lateralities, 'pigmentchanges', {
                'value': 0 if negword else 1,
                'term': m.group(),
                'label': 'no' if negword else 'yes',
                'negated': negword,
                'regex': 'ATROPHY_PAT',
                'source': source,
            }, known_laterality=lat)
        )
    return data
