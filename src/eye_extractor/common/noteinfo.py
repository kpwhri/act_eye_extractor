"""
Extract note-level information for laterality, disease.

This is primarily focused in the ASSESSMENT and CHIEF COMPLAINT sections.
"""
import enum
import itertools
import re

from eye_extractor.sections.document import Document
from eye_extractor.sections.section_builder import Section
from eye_extractor.laterality import LATERALITY_PATTERN, lat_lookup, Laterality
from eye_extractor.patterns import AMD_PAT, GLAUCOMA_PAT
from eye_extractor.ro.rao import RAO_PAT
from eye_extractor.ro.rvo import RVO_PAT
from eye_extractor.uveitis.uveitis import UVEITIS_PAT

TREATED_FOR_PAT = re.compile(
    rf'(?:'
    rf'(?P<name>being\s*treated\s*for)(?P<condition>.*?)[.:]'
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
            yield Section('treated_for', m.group('condition'), m.start('name'), m.end('name'),
                          m.start('condition'), m.end('condition'))


def extract_note_level_info(doc: Document):
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
    for section in itertools.chain(
            doc.iter_sections('assessment', 'cc', 'hpi', 'impression'),
            additional_sections(doc.text),
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
                if m := pattern.search(doc.text):
                    result[key] = True
                    end = m.end()
                    curr_lat = None
                    if lat_match := LATERALITY_PATTERN.search(doc.text[end: end + 30]):
                        curr_lat = lat_lookup(lat_match)
                        end += lat_match.end()
                        if result['default_lat'] == Laterality.UNKNOWN:
                            result['default_lat'] = curr_lat
                    if re.compile(r'(?:primary|principle)', re.I).search(doc.text[end: end + 30]):
                        if curr_lat:
                            result['default_lat'] = curr_lat
                        result['primary_dx'] = dx
    return result
