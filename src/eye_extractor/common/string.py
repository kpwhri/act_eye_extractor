import re
import string

TABLE = str.maketrans(' ', ' ', string.punctuation)
REPLACE = re.compile(
    r'(?:'
    r'[^A-Za-z0-9]/'  # e.g., d/b
    r'|/[^A-Za-z0-9]'  # e.g., d/b
    r'|[^A-Za-z0-9/]'
    r')+'
)


def remove_punctuation(text):
    return text.translate(TABLE)


def replace_punctuation(text):
    return REPLACE.sub(' ', text)
