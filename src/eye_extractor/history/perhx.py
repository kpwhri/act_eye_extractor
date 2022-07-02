import re

from loguru import logger

from eye_extractor.history.common import create_history, history_pat

START_PER_HX_PAT = re.compile(
    rf'(?:'
    rf'(?:past|personal)\W*(?:ocular|eye)\W*{history_pat}\W*?(?:of\W*)?:'
    rf'|past\W*medical\W*history ?:?'
    rf'|active\W*problem\W*list ?:?'
    rf'|\bpmh\W*?:'
    rf'|past\W*history\W*or\W*currently\W*being\W*treated\W*for\W*?:'
    rf')',
    re.I
)


def create_personal_history(text, headers=None, lateralities=None):
    return create_history(text, [START_PER_HX_PAT])
