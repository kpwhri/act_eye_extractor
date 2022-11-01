import re

from loguru import logger

from eye_extractor.history.common import create_history

START_FAM_HX_PAT = re.compile(
    rf'\b(?:'
    rf'family\W*(?:(?:eye|ocular)\W*)?history\W*(?:of\W*)?'
    rf'|famhx'
    rf'|fhx'
    rf'):',
    re.I
)


def create_family_history(text, headers=None, lateralities=None):
    return create_history(text, [START_FAM_HX_PAT])
