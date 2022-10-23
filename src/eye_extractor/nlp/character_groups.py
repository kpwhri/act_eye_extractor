import re

LINE_START_CHARACTERS = r'\n\r¶'


def get_previous_text_to_newline(index, text, line_start_chars=LINE_START_CHARACTERS):
    pat = re.compile(f'[{line_start_chars}]')
    line = pat.split(text[:index])[-1]
    return line
