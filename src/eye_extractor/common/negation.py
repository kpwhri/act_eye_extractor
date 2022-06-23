import re
from typing import Match

from eye_extractor.common.string import replace_punctuation


def is_negated(m: Match, text: str, terms: set[str],
               *, word_window: int = 2, char_window: int = 0,
               boundary_chars=':', lowercase_text=True):
    """

    :param lowercase_text: force lowercase text
    :param boundary_chars:
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
    if boundary_chars:
        context = re.split(f'[{re.escape(boundary_chars)}]', context)[-1]
    if lowercase_text:
        context = context.lower()
    no_punct = replace_punctuation(context)
    words = no_punct.split()
    for word in words[-word_window:]:
        if word in terms:
            return word


def is_post_negated(m: Match, text: str, terms: set[str],
                    *, word_window: int = 2, char_window: int = 0,
                    boundary_chars=None, lowercase_text=True):
    """

    :param boundary_chars: stop looking after this symbol (defaults to None)
    :param lowercase_text: force the input text to be lowercased
    :param m:
    :param text:
    :param terms:
    :param word_window: number of words to inspect for negation terms
    :param char_window: number of characters to look forward to find target words
    :return:
    """
    if not char_window:
        char_window = word_window * 10
    context = text[m.end(): m.end() + char_window]
    if boundary_chars:
        context = re.split(f'[{re.escape(boundary_chars)}]', context)[0]
    if lowercase_text:
        context = context.lower()
    no_punct = replace_punctuation(context)
    words = no_punct.split()
    for word in words[:word_window]:
        if word in terms:
            return word
