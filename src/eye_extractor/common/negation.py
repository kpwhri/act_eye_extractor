import re
from typing import Match

from eye_extractor.common.string import replace_punctuation

NEGWORDS = frozenset({'no', 'or', 'neg', 'without', 'w/out', '(-)'})


def _handle_negation_with_punctuation(text):
    """Hack to handle punctuation-infused negation words: replace with 'no'"""
    text = text.replace('w/out', 'without')
    text = text.replace('w/o', 'without')
    text = text.replace('(-)', ' no ')
    text = re.sub(r'(\D\W*)-([A-Za-z])', r'\g<1> no \g<2>', text)
    return text


def is_negated(m: Match | int, text: str, terms: set[str] = NEGWORDS,
               *, word_window: int = 2, char_window: int = 0,
               skip_regex: Match = None,
               boundary_chars=':', skip_n_boundary_chars=0, lowercase_text=True):
    """Look back from match for specified terms. Stop at `boundary_chars`.

    :param skip_n_boundary_chars: stop after N boundary chars;
        if set to 1, will stop when it runs into the second `boundary_chars`
    :param lowercase_text: force lowercase text
    :param skip_regex:
    :param boundary_chars:
    :param m: re.match object or int that should appear at end of text (i.e., m.start())
    :param text:
    :param terms:
    :param word_window: number of words to inspect for negation terms
    :param char_window: number of characters to look back to find target words
    :return:
    """
    return has_before(
        end_idx=m if isinstance(m, int) else m.start(), text=text, terms=terms,
        word_window=word_window, char_window=char_window,
        boundary_chars=boundary_chars, skip_n_boundary_chars=skip_n_boundary_chars,
        skip_regex=skip_regex, lowercase_text=lowercase_text,
        hack_punctuation=True,
    )


def has_before(end_idx: int, text: str, terms: set[str],
               *, word_window: int = 2, char_window: int = 0,
               skip_regex: Match = None,
               boundary_chars=':', skip_n_boundary_chars=0, lowercase_text=True,
               hack_punctuation=False):
    if not char_window:
        char_window = word_window * 10
    context = text[max(0, end_idx - char_window): end_idx]
    if boundary_chars:
        if skip_regex is not None:
            context = skip_regex.sub(' ', context)
        context_list = re.split(f'[{re.escape(boundary_chars)}]', context)
        context = ' '.join(context_list[-1 - skip_n_boundary_chars:])
    if lowercase_text:
        context = context.lower()
    if hack_punctuation:
        context = _handle_negation_with_punctuation(context)
    no_punct = replace_punctuation(context)
    words = no_punct.split()
    for word in words[-word_window:]:
        if word in terms:
            return word


def is_post_negated(m: Match | int, text: str, terms: set[str] = NEGWORDS,
                    *, word_window: int = 2, char_window: int = 0,
                    skip_n_boundary_chars=1, skip_regex: Match = None,
                    boundary_chars=':', lowercase_text=True):
    """

    :param skip_n_boundary_chars:
    :param skip_regex: remove these before splitting on boundary characters;
        useful for, e.g., removing 'OU:' which might not want to be counted as a section boundary
    :param boundary_chars: stop looking after this symbol (defaults to None)
    :param lowercase_text: force the input text to be lowercased
    :param m: re.Match or equivalent of re.Match.end() (where to start looking in text)
    :param text:
    :param terms:
    :param word_window: number of words to inspect for negation terms
    :param char_window: number of characters to look forward to find target words
    :return:
    """
    return has_after(
        start_idx=m if isinstance(m, int) else m.end(), text=text, terms=terms,
        word_window=word_window, char_window=char_window,
        skip_n_boundary_chars=skip_n_boundary_chars, skip_regex=skip_regex,
        boundary_chars=boundary_chars, lowercase_text=lowercase_text,
        hack_punctuation=True,
    )


def has_after(start_idx: int, text: str, terms: set[str],
              *, word_window: int = 2, char_window: int = 0,
              skip_n_boundary_chars=1, skip_regex: Match = None,
              boundary_chars=':', lowercase_text=True,
              hack_punctuation=False):
    """

    :param start_idx:
    :param text:
    :param terms:
    :param word_window:
    :param char_window:
    :param skip_n_boundary_chars:
    :param skip_regex: remove these before splitting on boundary characters;
        useful for, e.g., removing 'OU:' which might not want to be counted as a section boundary
    :param boundary_chars:
    :param lowercase_text:
    :return:
    """
    if not char_window:
        char_window = word_window * 10
    context = text[start_idx: start_idx + char_window]
    if boundary_chars:
        if skip_regex is not None:
            context = skip_regex.sub(' ', context)
        context_list = re.split(f'[{re.escape(boundary_chars)}]', context)
        context = ' '.join(context_list[:1 + skip_n_boundary_chars])
    if lowercase_text:
        context = context.lower()
    if hack_punctuation:
        context = _handle_negation_with_punctuation(context)
    no_punct = replace_punctuation(context)
    words = no_punct.split()
    for word in words[:word_window]:
        if word in terms:
            return word
