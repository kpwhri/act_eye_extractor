from eye_extractor.exam.cup_disk_ratio import extract_cup_disk_ratio


def get_exam(text, *, headers=None, lateralities=None):
    data = {}
    data['cd_ratio'] = extract_cup_disk_ratio(text, headers=headers, lateralities=lateralities)
    return data
