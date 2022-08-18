from eye_extractor.exam.cmt import extract_cmt
from eye_extractor.exam.cup_disk_ratio import extract_cup_disk_ratio
from eye_extractor.exam.rnfl import extract_rnfl_values

_LABEL_TO_FUNC = [
    ('cd_ratio', extract_cup_disk_ratio),
    ('rnfl', extract_rnfl_values),
    ('cmt', extract_cmt),
]


def get_exam(text, *, headers=None, lateralities=None):
    data = {label: func(text, headers=headers, lateralities=lateralities)
            for label, func in _LABEL_TO_FUNC}
    return data
