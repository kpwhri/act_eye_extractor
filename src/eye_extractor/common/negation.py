from typing import Match

from eye_extractor.common.string import replace_punctuation


def is_negated(m: Match, text: str, terms: set[str],
               *, word_window: int = 2, char_window: int = 0):
    """

    :param m:
    :param text:
    :param terms:
    :param word_window: number of words to inspect for negation terms
    :param char_window: number of characters to look back to find target words
    :return:
    """
    if not char_window:
        char_window = word_window * 10
    context = text[max(0, m.start() - char_window): m.start()]
    no_punct = replace_punctuation(context)
    words = no_punct.split()
    for word in words[-word_window:]:
        if word in terms:
            return word
