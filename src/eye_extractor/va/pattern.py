import re
from collections import namedtuple

from eye_extractor.laterality import Laterality

VA = (r'('
      r'(?P<numerator##>20|3E|E|\d+(\'|ft))/\s*(?P<score##>\d+|ni|no improvement)\s*(?P<diopter##>[+-]\d?)*'
      r'|'
      r'(20/\s*)?(?P<test##>HM|CF|LP|NLP)((\W+(@|at|x))?\s*'  # open paren: distance
      r'(?P<distance##>\d+(-\d+)?)\s*(?P<distance_metric##>\'|"|in|ft|feet)?'
      r'(?P<test2##>HM|CF|LP|NLP)?'
      r')'  # close paren: distance
      r'|'
      r'(20/\s*)?(?P<test3##>HM|CF|LP|NLP)'
      r'|'
      r'(20/\D*|ni|na|nt|no improvement|)'
      r'|'
      r'enucleated'
      r')')
OD = r'(O\W*D|R(ight)?\W*E(ye)?)'
OS = r'(O\W*S|L(eft)?\W*E(ye)?)'
PH = r'(P\W*H|Pinhole)'
CC = r'(va\'s\s*)?(C\W*C|with glasses|(with\s*)?specs|specs|with correction|best corrected)'
SC = r'(S\W*C|without glasses|uncorrected|without correction|unaided)'
PREVIOUS = r'(?P<previous>(Last|past|previous)\W+)?'

VaPattern = namedtuple('VaPattern', 'pattern metadata')

MD_OD_CC = {
    'laterality': Laterality.OD,
    'exam': 'vacc',
}
MD_OS_CC = {
    'laterality': Laterality.OS,
    'exam': 'vacc',
}
MD_OD_SC = {
    'laterality': Laterality.OD,
    'exam': 'vasc',
}
MD_OS_SC = {
    'laterality': Laterality.OS,
    'exam': 'vasc',
}
MD_OD_PH = {
    'laterality': Laterality.OD,
    'exam': 'vaph',
}
MD_OS_PH = {
    'laterality': Laterality.OS,
    'exam': 'vaph',
}

VA_MENTION = rf'{PREVIOUS}(Visual\s*acc?uity|VA|vision)\W+((snellen|distance)\W+)*'

VA_LINE_GROUPED = VaPattern(
    re.compile(
        rf'{VA_MENTION}'
        rf'{CC}\W+({OD}\W+)?{VA.replace("##", "_0")}\W+'
        rf'({CC}\W+)?({OS}\W+)?{VA.replace("##", "_1")}\W+'
        rf'{SC}\W+({OD}\W+)?{VA.replace("##", "_2")}\W+'
        rf'({SC}\W+)?({OS}\W+)?{VA.replace("##", "_3")}\W+'
        rf'{PH}\W+({OD}\W+)?{VA.replace("##", "_4")}\W+'
        rf'({PH}\W+)?({OS}\W+)?{VA.replace("##", "_5")}'
        , re.I
    ),
    [MD_OD_CC, MD_OS_CC, MD_OD_SC, MD_OS_SC, MD_OD_PH, MD_OS_PH]
)
VA_LINE_SC_CC = VaPattern(
    re.compile(
        rf'{VA_MENTION}'
        rf'{SC}\W+({OD}\W+)?{VA.replace("##", "_0")}\W+'
        rf'({SC}\W+)?({OS}\W+)?{VA.replace("##", "_1")}\W+'
        rf'{CC}\W+({OD}\W+)?{VA.replace("##", "_2")}\W+'
        rf'({CC}\W+)?({OS}\W+)?{VA.replace("##", "_3")}\W+'
        , re.I
    ),
    [MD_OD_SC, MD_OS_SC, MD_OD_CC, MD_OS_CC]
)
VA_LINE_CC = VaPattern(
    re.compile(
        rf'{VA_MENTION}'
        rf'({CC}\W+)+{OD}\W+{VA.replace("##", "_0")}\W+'
        rf'({PH}\W+({OD}\W+)?{VA.replace("##", "_1")}\W+)?'
        rf'({CC}\W+)?{OS}\W+{VA.replace("##", "_2")}\W*'
        rf'(({PH}\W+)?({OS}\W+)?{VA.replace("##", "_3")})?',
        re.I
    ),
    [MD_OD_CC, MD_OD_PH, MD_OS_CC, MD_OS_PH]
)
VA_LINE_SC = VaPattern(
    re.compile(
        rf'{VA_MENTION}'
        rf'{SC}\W+{OD}\W+{VA.replace("##", "_0")}\W+'
        rf'({PH}\W+({OD}\W+)?{VA.replace("##", "_1")}\W+)?'
        rf'({SC}\W+)?{OS}\W+{VA.replace("##", "_2")}\W*'
        rf'(({PH}\W+)?({OS}\W+)?{VA.replace("##", "_3")})?'
        , re.I
    ),
    [MD_OD_SC, MD_OD_PH, MD_OS_SC, MD_OS_PH]
)
VA_LINE_SC_OD = VaPattern(
    re.compile(
        rf'{VA_MENTION}'
        rf'{SC}\W+{OD}\W+{VA.replace("##", "_0")}\W+'
        rf'({PH}\W+({OD}\W+)?{VA.replace("##", "_1")}\W+)?'
        , re.I
    ),
    [MD_OD_SC, MD_OD_PH]
)
VA_LINE_SC_OS = VaPattern(
    re.compile(
        rf'{VA_MENTION}'
        rf'{SC}\W+{OS}\W+{VA.replace("##", "_0")}\W+'
        rf'({PH}\W+({OS}\W+)?{VA.replace("##", "_1")}\W+)?'
        , re.I
    ),
    [MD_OS_SC, MD_OS_PH]
)


