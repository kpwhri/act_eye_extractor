import re

from eye_extractor.history.common import create_history, history_pat

START_PER_HX_PAT = re.compile(
    rf'(?:'
    rf'(?:(?:past|personal|medical)\W*)?(?:ocular|eye)\W*{history_pat}\W*?(?:of\W*)?:'
    rf'|(?:(?:past|personal)\W*)?medical\W*{history_pat} ?:?'
    rf'|active\W*problem\W*list ?:?'
    rf'|\bpmhx?\W*?:'
    rf'|past\W*history\W*or\W*currently\W*being\W*treated\W*for\W*?:'
    rf')',
    re.I
)


def create_personal_history(text, headers=None, lateralities=None):
    return create_history(text, [START_PER_HX_PAT], is_personal_hx=True)
