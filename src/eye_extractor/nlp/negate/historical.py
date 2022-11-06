from typing import Match

from eye_extractor.nlp.negate.negation import is_negated

HISTORY_WORDS = frozenset({
    'hx', 'history', 'phx'
})


def is_historical_before(m: Match | int, text: str, terms: set[str] | frozenset[str] | dict = HISTORY_WORDS, **kwargs):
    return is_negated(m, text, terms, **kwargs)


def is_historical_after(m: Match | int, text: str, terms: set[str] | frozenset[str] | dict = HISTORY_WORDS, **kwargs):
    return is_negated(m, text, terms, **kwargs)


def is_historical(m: Match | int, text: str):
    return is_historical_before(m, text) or is_historical_after(m, text)
