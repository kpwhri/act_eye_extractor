import re
from typing import Match

from eye_extractor.common.string import replace_punctuation


def is_negated(m: Match, text: str, terms: set[str],
               *, word_window: int = 2, char_window: int = 0,
               boundary_chars=':', skip_n_boundary_chars=0, lowercase_text=True):
    """Look back from match for specified terms. Stop at `boundary_chars`.

    :param skip_n_boundary_chars: stop after N boundary chars;
        if set to 1, will stop when it runs into the second `boundary_chars`
    :param lowercase_text: force lowercase text
    :param boundary_chars:
    :param m:
    :param text:
    :param terms:
    :param word_window: number of words to inspect for negation terms
    :param char_window: number of characters to look back to find target words
    :return:
    """
    return has_before(
        end_idx=m.start(), text=text, terms=terms, word_window=word_window, char_window=char_window,
        boundary_chars=boundary_chars, skip_n_boundary_chars=skip_n_boundary_chars,
        lowercase_text=lowercase_text)


def has_before(end_idx: int, text: str, terms: set[str],
               *, word_window: int = 2, char_window: int = 0,
               boundary_chars=':', skip_n_boundary_chars=0, lowercase_text=True):
    if not char_window:
        char_window = word_window * 10
    context = text[max(0, end_idx - char_window): end_idx]
    if boundary_chars:
        context_list = re.split(f'[{re.escape(boundary_chars)}]', context)
        context = ' '.join(context_list[-1 - skip_n_boundary_chars:])
    if lowercase_text:
        context = context.lower()
    no_punct = replace_punctuation(context)
    words = no_punct.split()
    for word in words[-word_window:]:
        if word in terms:
            return word


def is_post_negated(m: Match, text: str, terms: set[str],
                    *, word_window: int = 2, char_window: int = 0,
                    skip_n_boundary_chars=1,
                    boundary_chars=':', lowercase_text=True):
    """

    :param skip_n_boundary_chars:
    :param boundary_chars: stop looking after this symbol (defaults to None)
    :param lowercase_text: force the input text to be lowercased
    :param m:
    :param text:
    :param terms:
    :param word_window: number of words to inspect for negation terms
    :param char_window: number of characters to look forward to find target words
    :return:
    """
    return has_after(
        start_idx=m.end(), text=text, terms=terms,
        word_window=word_window, char_window=char_window,
        skip_n_boundary_chars=skip_n_boundary_chars,
        boundary_chars=boundary_chars, lowercase_text=lowercase_text)


def has_after(start_idx: int, text: str, terms: set[str],
              *, word_window: int = 2, char_window: int = 0,
              skip_n_boundary_chars=1,
              boundary_chars=':', lowercase_text=True):
    if not char_window:
        char_window = word_window * 10
    context = text[start_idx: start_idx + char_window]
    if boundary_chars:
        context_list = re.split(f'[{re.escape(boundary_chars)}]', context)
        context = ' '.join(context_list[:1 + skip_n_boundary_chars])
    if lowercase_text:
        context = context.lower()
    no_punct = replace_punctuation(context)
    words = no_punct.split()
    for word in words[:word_window]:
        if word in terms:
            return word
