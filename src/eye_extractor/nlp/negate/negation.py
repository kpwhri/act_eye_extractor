import enum
import re
from typing import Match, Pattern

from eye_extractor.common.string import replace_punctuation


class NegationStatus(enum.IntEnum):
    UNKNOWN = -1
    NOT_NEGATED = 0
    NEGATED = 1


NEGWORDS = {
    'no': {
        'new': NegationStatus.UNKNOWN,  # this should be UNKNOWN
        'increased': False,
        'worsening': False,
        None: True,
    },
    'not': {
        'only': False,
        'just': False,
        None: True,
    },
    'or': True,
    'neg': True,
    'non': True,
    'negative': True,
    'without': True,
    'w/out': True,
    'w/o': True,
    'h/o': True,
    '(-)': True,
    'if': True,
    'possible': True,
    'resolved': True,
    'resolution': True,
    'cleared': True,
    'hx': True,
    'risk': {
        'of': {
            'exacerbating': NegationStatus.UNKNOWN,
            'worsening': NegationStatus.UNKNOWN,
            None: True,
        },
        None: True,
    },
    'history': True,
    None: False,
}

NEGWORD_UNKNOWN_PHRASES = {'no new', 'risk of exacerbating', 'risk of worsening'}

NEGWORD_SET = frozenset({key for key in NEGWORDS if key})

NEGWORDS_POST = frozenset(
    {'not', 'cleared', 'resolved', 'or'}
)

DEFAULT_BOUNDARY_REGEX = re.compile(r'\b(?:od|os|ou)\b')

# Negated list of variable size separated by ','.
NEGATED_LIST_PATTERN_COMMA = re.compile(
    rf'(no\s+|\(-\)\s*)([^¶.;\n]*,)+\s+[^¶.;\n]+',
    re.IGNORECASE
)

# Negated list of two items separated by 'or'.
# Final list item may not contain any spaces.
NEGATED_LIST_PATTERN_OR = re.compile(
    rf'(no\s+|\(-\)\s*)[^¶.;\n]+\s+or\s+\w+',
    re.IGNORECASE
)

# Negated list of variable size separated by '/'.
# Final list item may not contain any spaces.
NEGATED_LIST_PATTERN_SLASH = re.compile(
    rf'(no\s+|\(-\)\s*)[^¶.;\n]+/\w+',
    re.IGNORECASE
)

NEGATED_LIST_PATTERNS = [
    {'pattern': NEGATED_LIST_PATTERN_COMMA, 'sep': ','},
    # Surround `sep` with spaces to prevent accidental capture. Example - 'oranges'.
    {'pattern': NEGATED_LIST_PATTERN_OR, 'sep': ' or '},
    {'pattern': NEGATED_LIST_PATTERN_SLASH, 'sep': '/'},
]


def _prep_negation_tree(words, fsa, *, return_unknown=False):
    """Build FSA to make it backwards-compatible with simple set."""
    if isinstance(fsa, dict):
        pass  # desired state
    elif isinstance(fsa, (list, set, frozenset)):  # one-level -> convert to dict
        fsa = {x: True for x in fsa} | {None: False}
    else:
        raise ValueError(f'Unrecognized type containing negation: {type(fsa)}')
    return _recurse_negation_tree(words, fsa, return_unknown=return_unknown)


def _recurse_negation_tree(words, fsa, level=0, return_unknown=False):
    """
    Use FSA to determine if negation word present; this allows for
        affirmative mentions like 'not only'.
    See `NEGWORDS` for example of `fsa`.
    """
    for i, word in enumerate(words):
        if word in fsa:
            val = fsa[word]
            if isinstance(val, dict):  # branch node
                val = _recurse_negation_tree(words[i + 1:], val, level + 1, return_unknown=return_unknown)
            if not return_unknown and val == NegationStatus.UNKNOWN:
                return False
            elif val:
                return f'{word} {val}' if isinstance(val, str) else word
            elif level > 0:
                return False
            else:  # level0 False: target not found
                continue
    return fsa[None] or None


def _handle_negation_with_punctuation(text):
    """Hack to handle punctuation-infused negation words: replace with 'no'"""
    text = text.replace('w/out', 'without')
    text = text.replace('w/o', 'without')
    text = text.replace('h/o', 'history')
    text = text.replace('(-)', ' no ')
    text = re.sub(r'((?:^|\D\s+)\s*)-([A-Za-z]|$)', r'\g<1> no \g<2>', text)
    return text


def is_any_negated(m: Match | int, text: str):
    return is_negated(m, text) or is_post_negated(m, text)


def is_negated(m: Match | int, text: str, terms: set[str] | frozenset[str] | dict = NEGWORDS,
               *, word_window: int = 2, char_window: int = 0,
               skip_regex: Pattern = None, boundary_regex: Pattern = DEFAULT_BOUNDARY_REGEX,
               boundary_chars=':¶', skip_n_boundary_chars=0,
               lowercase_text=True, return_unknown=False):
    """Look back from match for specified terms. Stop at `boundary_chars`.

    :param return_unknown:
    :param boundary_regex: create a boundary
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
        word_window=word_window, char_window=char_window, boundary_regex=boundary_regex,
        boundary_chars=boundary_chars, skip_n_boundary_chars=skip_n_boundary_chars,
        skip_regex=skip_regex, lowercase_text=lowercase_text,
        hack_punctuation=True, return_unknown=return_unknown,
    )


def has_before(end_idx: int, text: str, terms: set[str] | dict,
               *, word_window: int = 2, char_window: int = 0,
               skip_regex: Pattern = None, boundary_regex: Pattern = None,
               boundary_chars=':¶', skip_n_boundary_chars=0, lowercase_text=True,
               hack_punctuation=False, return_unknown=False):
    if not char_window:
        char_window = word_window * 10
    context = text[max(0, end_idx - char_window): end_idx]
    if boundary_chars:
        if skip_regex is not None:
            context = skip_regex.sub(' ', context)
        boundary_pattern = f'[{re.escape(boundary_chars)}]'
        if boundary_regex:
            boundary_pattern = f'(?:{boundary_regex.pattern}|{boundary_pattern})'
        context_list = re.split(boundary_pattern, context)
        context = ' '.join(context_list[-1 - skip_n_boundary_chars:])
    if lowercase_text:
        context = context.lower()
    if hack_punctuation:
        context = _handle_negation_with_punctuation(context)
    no_punct = replace_punctuation(context)
    words = no_punct.split()
    return _prep_negation_tree(words[-word_window:], terms, return_unknown=return_unknown)


def is_post_negated(m: Match | int, text: str, terms: set[str] | frozenset[str] | dict = NEGWORDS_POST,
                    *, word_window: int = 2, char_window: int = 0, boundary_regex: Pattern = DEFAULT_BOUNDARY_REGEX,
                    skip_n_boundary_chars=1, skip_regex: Match = None,
                    boundary_chars=':¶', lowercase_text=True, return_unknown=False):
    """

    :param return_unknown:
    :param boundary_regex:
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
        word_window=word_window, char_window=char_window, boundary_regex=boundary_regex,
        skip_n_boundary_chars=skip_n_boundary_chars, skip_regex=skip_regex,
        boundary_chars=boundary_chars, lowercase_text=lowercase_text,
        hack_punctuation=True, return_unknown=return_unknown,
    )


def has_after(start_idx: int, text: str, terms: set[str] | dict,
              *, word_window: int = 2, char_window: int = 0, boundary_regex: Pattern = None,
              skip_n_boundary_chars=1, skip_regex: Match = None,
              boundary_chars=':¶', lowercase_text=True,
              hack_punctuation=False, return_unknown=False):
    """

    :param return_unknown:
    :param boundary_regex:
    :param hack_punctuation:
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
        boundary_pattern = f'[{re.escape(boundary_chars)}]'
        if boundary_regex:
            boundary_pattern = f'(?:{boundary_regex.pattern}|{boundary_pattern})'
        context_list = re.split(boundary_pattern, context)
        context = ' '.join(context_list[:1 + skip_n_boundary_chars])
    if lowercase_text:
        context = context.lower()
    if hack_punctuation:
        context = _handle_negation_with_punctuation(context)
    no_punct = replace_punctuation(context)
    words = no_punct.split()
    return _prep_negation_tree(words[:word_window], terms, return_unknown=return_unknown)


def _find_negated_list_spans(text: str) -> list[tuple[int, int, str]]:
    """Find index spans for all negated lists in a text.

    :param text: Text to search for negated list.
    :return: List of all negated list spans as tuples with three elements.
        1) Start index (inclusive), 2) end index (exclusive), 3) separator.
    """
    matches = []
    cursor = 0
    for pattern_dict in NEGATED_LIST_PATTERNS:
        for match in pattern_dict['pattern'].finditer(text):
            start_index, end_index = match.span()
            if start_index >= cursor:
                cursor = end_index
                matches.append((start_index, end_index, pattern_dict['sep']))

    return matches


def find_unspecified_negated_list_items(text: str, lat_pattern: re.Pattern) -> list[tuple]:
    """Find all negated list items in text with unspecified laterality.

    :param text: Text to search for unspecified negated list items.
    :param lat_pattern: Laterality pattern used to determine list item laterality.
    :return: List of all unspecified negated list item spans as tuples. Items may come from multiple negated lists.
        Start index is inclusive, end index is exclusive.
    """
    unspecified_item_spans = []
    negation_pattern = re.compile(
        rf'(no\s+|\(-\)\s*)',
        re.IGNORECASE
    )
    negated_list_spans = _find_negated_list_spans(text)
    negated_lists = [text[start_index:end_index] for start_index, end_index, _ in negated_list_spans]
    for neg_list, neg_list_span in zip(negated_lists, negated_list_spans):
        neg_list_start_idx = neg_list_span[0]  # Start of negated list index.
        sep = neg_list_span[2]
        # Remove initial negation string.
        neg_removed = negation_pattern.sub('', neg_list, count=1)
        # Isolate all negated list items. Split `negated_lists` on separator.
        items = [item.strip() for item in re.split(rf'{sep}', neg_removed)]
        # Verify negated list item does not have laterality.
        unspecified_items = [item for item in items if not lat_pattern.search(item)]
        # Find index spans for each unspecified list item.
        for unspec_item in unspecified_items:
            # `unspec_item_span` contains item indices within `neg_list`.
            unspec_item_span = re.search(re.escape(unspec_item), neg_list).span()
            # `adjusted_unspec_item_span` contains item indices within `text`.
            adjusted_unspec_item_span = (
                unspec_item_span[0] + neg_list_start_idx
                , unspec_item_span[1] + neg_list_start_idx
            )
            unspecified_item_spans.append(adjusted_unspec_item_span)

    return unspecified_item_spans
