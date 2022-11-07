import re

BOILERPLATE_PAT = re.compile(
    rf'\b(?:risk|discuss).*?\.',
    re.I
)


def remove_boilerplate(text):
    for pattern in (BOILERPLATE_PAT,):
        text = pattern.sub(' ', text)
    return text
