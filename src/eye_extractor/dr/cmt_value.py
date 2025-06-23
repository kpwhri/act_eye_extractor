import re

from eye_extractor.nlp.negate.negation import is_negated
from eye_extractor.laterality import create_new_variable, Laterality, LateralityLocator
from eye_extractor.sections.document import Document

CMT_VALUE_OD_OS_UNK_PAT = re.compile(
    r'\b('
    r'(CMT|central macular thickness:?)\s+'
    r'(OD:?\s*(?P<od_value>\d{3}))?\s?'
    r'(OS:?\s*(?P<os_value>\d{3}))?'
    r'(?P<unk_value>\d{3})?'
    r')\b',
    re.I
)
CMT_VALUE_OD_SEP_OS_PAT = re.compile(
    r'\b('
    r'(CMT|central macular thickness:?)\s+'
    r'(OD:?\s*(?P<od_value>\d{3}))'
    r'(.*)(?=OS)'
    r'(OS:?\s*(?P<os_value>\d{3}))'
    r')\b',
    re.I
)

CMT_VALUE_PATS = [
    ('CMT_VALUE_OD_SEP_OS_PAT', CMT_VALUE_OD_SEP_OS_PAT),
    ('CMT_VALUE_OS_OS_UNK_PAT', CMT_VALUE_OD_OS_UNK_PAT),
]


def get_cmt_value(doc: Document) -> list:
    data = []
    for new_var in _get_cmt_value(doc.get_text(), doc.get_lateralities(), 'ALL'):
        data.append(new_var)

    return data


def _create_new_cmt_var(text: str,
                        match: str,
                        match_name: str,
                        match_value: int,
                        lateralities: LateralityLocator,
                        negated: bool | str,
                        pat_label: str,
                        source: str) -> dict:
    match2lat = {
        'od_value': Laterality.OD,
        'os_value': Laterality.OS,
        'unk_value': Laterality.UNKNOWN,
    }
    return create_new_variable(text, match, lateralities, 'dmacedema_cmt',
                               {
                                   'value': 0 if negated else match_value,
                                   'term': match.group(),
                                   'label': f'No CMT value' if negated else 'CMT value',
                                   'negated': negated,
                                   'regex': pat_label,
                                   'source': source,
                               },
                               # If `known_laterality == Laterality.UNKNOWN`, laterality will be searched for.
                               known_laterality=match2lat[match_name])


def _get_cmt_value(text: str, lateralities, source: str) -> dict:
    for pat_label, pat in CMT_VALUE_PATS:
        for match in pat.finditer(text):
            negated = is_negated(match, text, word_window=1)
            for match_name, match_value in match.groupdict().items():
                if match_value:
                    yield _create_new_cmt_var(text,
                                              match,
                                              match_name,
                                              int(match_value),
                                              lateralities,
                                              negated,
                                              pat_label,
                                              source)
