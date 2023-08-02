import re

BOILERPLATE_PAT = re.compile(
    rf'\b(?:risk|discuss).*?\.',
    re.I
)

TARGET_PATS = (BOILERPLATE_PAT,)


def remove_boilerplate(text):
    for pattern in TARGET_PATS:
        text = pattern.sub(' ', text)
    return text


def get_boilerplate(text):
    """
    DEBUG: get boilerplate pattern matches
    :param text:
    :return:
    """
    res = []
    for pattern in TARGET_PATS:
        for m in pattern.finditer(text):
            res.append(m.group())
    return {
        'boilerplate': res,
    }