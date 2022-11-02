import enum
import re

from eye_extractor.laterality import build_laterality_table, create_new_variable

pco = r'(?:pco|(?:post\w*\s*)?capsular\s*opacity)'
trace = r'tr(?:ace)?'
grade = r'\b(?:grade|gd)'

TRACE_PCO_PAT = re.compile(
    rf'(?:'
    rf'\b{trace}\s*{pco}\b'
    rf'|{pco}\s*{trace}'
    rf')',
    re.I
)

TRACE_PAT = re.compile(
    rf'(?:\b{trace}\b)',
    re.I,
)


def build_from_number_pco(num):
    return re.compile(
        rf'(?:'
        rf'{num}\+\s*{pco}'
        rf'|{pco}\s*(?:\d\+?\s*-\s*)?{num}\+'
        rf'|{pco}\s*{grade}\s*{num}'
        rf'|{grade}\s*{num}\+?\s*{pco}'
        rf')',
        re.I
    )


def build_from_number(num):
    return re.compile(
        rf'(?:'
        rf'(?:\d\+?\s*-\s*)?{num}\+'
        rf'|{grade}\s*{num}'
        rf')',
        re.I
    )


PCO_PAT = re.compile(
    rf'(?:{pco})',
    re.I
)

NO_PCO_PAT = re.compile(
    rf'(?:\bno\s*{pco})',
    re.I
)


class PosteriorCapsuleOpacity(enum.IntEnum):
    NONE = 0
    P1 = 1
    P2 = 2
    P3 = 3
    P4 = 4
    TRACE = 5
    MATURE = 10
    OTHER = 11
    NO_INDICATION = -1


def extract_posterior_capsular_opacity(text, *, headers=None, lateralities=None):
    data = []
    if headers:
        for lens_header, lens_text in headers.iterate('LENS'):
            lens_lateralities = build_laterality_table(lens_text)
            # known patterns
            for label, pat, value in [
                ('NO_PCO_PAT', NO_PCO_PAT, PosteriorCapsuleOpacity.NONE),
                ('TRACE_PCO_PAT', TRACE_PCO_PAT, PosteriorCapsuleOpacity.TRACE),
                ('1_PCO_PAT', build_from_number_pco(1), PosteriorCapsuleOpacity.P1),
                ('2_PCO_PAT', build_from_number_pco(2), PosteriorCapsuleOpacity.P2),
                ('3_PCO_PAT', build_from_number_pco(3), PosteriorCapsuleOpacity.P3),
                ('4_PCO_PAT', build_from_number_pco(4), PosteriorCapsuleOpacity.P4),
            ]:
                _finditer(data, label, lens_lateralities, lens_header, lens_text, pat, value)
            if not data:
                # just numbers
                for label, pat, value in [
                    ('TRACE_PAT', TRACE_PCO_PAT, PosteriorCapsuleOpacity.TRACE),
                    ('1_PAT', build_from_number(1), PosteriorCapsuleOpacity.P1),
                    ('2_PAT', build_from_number(2), PosteriorCapsuleOpacity.P2),
                    ('3_PAT', build_from_number(3), PosteriorCapsuleOpacity.P3),
                    ('4_PAT', build_from_number(4), PosteriorCapsuleOpacity.P4),
                ]:
                    _finditer(data, label, lens_lateralities, lens_header, lens_text, pat, value)

            # heuristics
            if not data:
                for label, pat in [
                    ('PCO_PAT', PCO_PAT),
                ]:
                    for m in pat.finditer(lens_text):
                        data.append(
                            create_new_variable(lens_text, m, lens_lateralities, 'posterior_cap_opacity', {
                                'value': value,
                                'term': m.group(),
                                'source': lens_header,
                            })
                        )
    return data


def _finditer(data, label, lens_lateralities, lens_header, lens_text, pat, value):
    for m in pat.finditer(lens_text):
        data.append(
            create_new_variable(lens_text, m, lens_lateralities, 'posterior_cap_opacity', {
                'value': value,
                'term': m.group(),
                'regex': label,
                'source': lens_header,
            })
        )
