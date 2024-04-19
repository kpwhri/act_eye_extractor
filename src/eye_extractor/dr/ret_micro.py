import re

from eye_extractor.common.get_variable import get_variable
from eye_extractor.common.severity import extract_severity, Severity
from eye_extractor.nlp.negate.negation import is_negated
from eye_extractor.laterality import create_new_variable

RET_MICRO_PAT = re.compile(
    r'\b('
    r'(retinal|scattered|single)\W+(tr\W+)?ma\'?s?'
    r'|(retinal\W+)?micro\W?aneurysms?'
    r')\b',
    re.I
)


def get_ret_micro(text: str, *, headers=None, lateralities=None) -> list:
    return get_variable(text, _get_ret_micro, headers=headers, lateralities=lateralities)


def _get_ret_micro(text: str, lateralities, source: str) -> dict:
    for m in RET_MICRO_PAT.finditer(text):
        negated = is_negated(m, text, word_window=4, boundary_chars=':¶+')
        context = f'{text[max(0, m.start() - 40): m.start()]} {text[m.end():min(len(text), m.end() + 6)]}'
        severities = extract_severity(context)
        if severities:  # With severity quantifier.
            for sev in severities:
                yield create_new_variable(text, m, lateralities, 'ret_microaneurysm', {
                    'value': Severity.NONE if negated else sev,
                    'term': m.group(),
                    'label': 'Retinal microaneurysm',
                    'negated': negated,
                    'regex': 'RET_MICRO_PAT',
                    'source': source,
                })
        else:  # Without severity quantifier.
            yield create_new_variable(text, m, lateralities, 'ret_microaneurysm', {
                'value': Severity.NONE if negated else Severity.YES_NOS,
                'term': m.group(),
                'label': f'{"No r" if negated else "R"}etinal microaneurysm',
                'negated': negated,
                'regex': 'RET_MICRO_PAT',
                'source': source,
            })

