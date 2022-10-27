import re

LINE_START_CHARACTERS = r'\n\r¶'


def get_previous_text_to_newline(index, text, line_start_chars=LINE_START_CHARACTERS):
    pat = re.compile(f'[{line_start_chars}]')
    line = pat.split(text[:index])[-1]
    return line


def get_next_text_to_newline(index, text, line_end_chars=LINE_START_CHARACTERS):
    pat = re.compile(f'[{line_end_chars}]')
    line = pat.split(text[index:])[0]
    return line


def get_next_index_of_newline(index, text, line_end_chars=LINE_START_CHARACTERS):
    i = index
    for i, letter in enumerate(text[index:], start=index):
        if letter in line_end_chars:
            return i
    return i


def get_previous_index_of_newline(index, text, line_end_chars=LINE_START_CHARACTERS):
    i = index
    for i, letter in enumerate(text[:index][::-1]):
        if letter in line_end_chars:
            return index - i
    return i
