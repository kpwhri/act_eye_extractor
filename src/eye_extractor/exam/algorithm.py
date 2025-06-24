from eye_extractor.exam.cmt import extract_cmt
from eye_extractor.exam.cup_disk_ratio import extract_cup_disk_ratio
from eye_extractor.exam.rnfl import extract_rnfl_values
from eye_extractor.sections.document import Document

_LABEL_TO_FUNC = [
    ('cd_ratio', extract_cup_disk_ratio),
    ('rnfl', extract_rnfl_values),
    ('cmt', extract_cmt),
]


def get_exam(doc: Document):
    data = {label: func(doc)
            for label, func in _LABEL_TO_FUNC}
    return data
