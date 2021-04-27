import re


def tokenize(s: str, *, regex=r'(\W)'):
    start_index = 0
    for val in re.split(regex, s):
        end_index = start_index + len(val)
        if val.strip():
            yield val, start_index, end_index
        start_index = end_index
