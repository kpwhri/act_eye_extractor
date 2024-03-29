"""
Extract note-level information for laterality, disease.

This is primarily focused in the ASSESSMENT and CHIEF COMPLAINT sections.
"""
import enum
import itertools
import re

from eye_extractor.headers import extract_headers_and_text
from eye_extractor.laterality import LATERALITY_PATTERN, lat_lookup, Laterality
from eye_extractor.patterns import AMD_PAT, GLAUCOMA_PAT
from eye_extractor.ro.rao import RAO_PAT
from eye_extractor.ro.rvo import RVO_PAT
from eye_extractor.uveitis.uveitis import UVEITIS_PAT

TREATED_FOR_PAT = re.compile(
    rf'(?:'
    rf'being\s*treated\s*for(?P<condition>.*?)[.:]'
    rf')',
    re.I
)


class Diagnosis(enum.IntEnum):
    NONE = 0
    AMD = 1
    DR = 2
    CATARACT = 3
    GLAUCOMA = 4
    PREGLAUCOMA = 5
    RVO = 6
    RAO = 7
    UVEITIS = 8


def additional_sections(text):
    for pat in (TREATED_FOR_PAT,):
        if m := pat.search(text):
            yield 'TREATED_FOR', m.group('condition')


def extract_note_level_info(text, *, headers=None, lateralities=None):
    headers = headers or extract_headers_and_text(text)
    result = {
        'is_amd': False,
        'is_dr': False,
        'is_cataract': False,
        'is_glaucoma': False,
        'is_rvo': False,
        'is_rao': False,
        'is_uveitis': False,
        'default_lat': Laterality.UNKNOWN,
        'primary_dx': False,
    }
    for header, text in itertools.chain(
            headers.iterate(
                'ASSESSMENT', 'ASSESSMENT_COMMENTS', 'CHIEF_COMPLAINT', 'HPI',
                'IMPRESSION',
            ),
            additional_sections(text)
    ):
        for key, pattern, dx in [
            ('is_amd', AMD_PAT, Diagnosis.AMD),
            ('is_dr', re.compile(r'diabetic\s*retinopathy', re.I), Diagnosis.DR),
            ('is_cataract', re.compile(r'cataract', re.I), Diagnosis.CATARACT),
            ('is_glaucoma', GLAUCOMA_PAT, Diagnosis.GLAUCOMA),
            ('is_rvo', RVO_PAT, Diagnosis.RVO),
            ('is_rao', RAO_PAT, Diagnosis.RAO),
            ('is_uveitis', UVEITIS_PAT, Diagnosis.UVEITIS),
        ]:
            if not result[key]:
                if m := pattern.search(text):
                    result[key] = True
                    end = m.end()
                    curr_lat = None
                    if lat_match := LATERALITY_PATTERN.search(text[end: end + 30]):
                        curr_lat = lat_lookup(lat_match)
                        end += lat_match.end()
                        if result['default_lat'] == Laterality.UNKNOWN:
                            result['default_lat'] = curr_lat
                    if re.compile(r'(?:primary|principle)', re.I).search(text[end: end + 30]):
                        if curr_lat:
                            result['default_lat'] = curr_lat
                        result['primary_dx'] = dx
    return result
