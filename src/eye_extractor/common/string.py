import re
import string

TABLE = str.maketrans(' ', ' ', string.punctuation)
REPLACE = re.compile(r'[^A-Za-z0-9]+')


def remove_punctuation(text):
    return text.translate(TABLE)


def replace_punctuation(text):
    return REPLACE.sub(text, ' ')
