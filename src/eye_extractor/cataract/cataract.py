import re

iol_models = '|'.join([
    'sn60wf', 'ma60ac', 'sn6at5',
])

power = r'[+-]?\d{1,2}\.?[05]*'
diopter = r'd(iopter)?'


IOL_TYPE_PAT = re.compile(
    rf'(?P<model>{iol_models})\W*'
    rf'(?:'
    rf'(?P<power>{power})\W*{diopter}'
    rf'|{diopter} with (?P<power2>{power})'
    rf')',
    re.I
)


def get_iol_type(text):
    return None
