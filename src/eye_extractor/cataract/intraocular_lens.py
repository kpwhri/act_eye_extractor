import enum
import re

from eye_extractor.common.negation import is_negated, is_post_negated
from eye_extractor.common.overlap import IndexOverlapChecker
from eye_extractor.laterality import create_new_variable, build_laterality_table


class IolLens(enum.IntEnum):
    NO = 0
    PCIOL = 2
    SIOL = 3
    ACIOL = 4
    PSEUDOPHAKIA = 10
    APHAKIA = 11
    IOL = 20
    UNKNOWN = -1


PCIOL_PAT = re.compile(r'\b(?:pc(\W*iol)?)\b', re.I)
ACIOL_PAT = re.compile(r'\b(?:ac(\W*iol)?)\b', re.I)
SIOL_PAT = re.compile(r'\b(?:s(\W*iol)?)\b', re.I)
PSEUDO_PAT = re.compile(r'\b(?:pseud[oa]phak\w+)', re.I)
APHAKIA_PAT = re.compile(r'\b(?:aphak\w+)', re.I)
IOL_PAT = re.compile(rf'(?:\biol\b)', re.I)


def extract_iol_lens(text, *, headers=None, lateralities=None):
    data = []
    if headers:
        for lens_header, lens_text in headers.iterate('LENS'):
            overlapper = IndexOverlapChecker()
            lens_lateralities = build_laterality_table(lens_text)
            for label, pat, value in [
                ('PCIOL_PAT', PCIOL_PAT, IolLens.PCIOL),
                ('ACIOL_PAT', ACIOL_PAT, IolLens.ACIOL),
                ('SIOL_PAT', SIOL_PAT, IolLens.SIOL),
                ('PSEUDO_PAT', PSEUDO_PAT, IolLens.PSEUDOPHAKIA),
                ('APHAKIA_PAT', APHAKIA_PAT, IolLens.APHAKIA),
                ('IOL_PAT', IOL_PAT, IolLens.IOL),
            ]:
                for m in pat.finditer(lens_text):
                    if overlapper.overlaps(m.start()):
                        continue  # prevent IOL from finding ACIOL, etc.
                    overlapper.add(m.start(), m.end())
                    negword = (
                            is_negated(m, lens_text, word_window=4)
                            or is_post_negated(m, lens_text, {'not'}, word_window=3)
                    )
                    data.append(
                        create_new_variable(lens_text, m, lens_lateralities, 'intraocular_lens', {
                            'value': IolLens.NO if negword else value,
                            'term': m.group(),
                            'label': 'no' if negword else 'yes',
                            'regex': label,
                            'source': lens_header,
                        })
                    )
    return data
