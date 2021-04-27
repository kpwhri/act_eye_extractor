import re
from collections import namedtuple

from eye_extractor.laterality import Laterality

VA = (r'('
      r'(?P<numerator##>20|3E|E|\d+(\'|ft))/\s*(?P<score##>\d+|ni|no improvement)\s*(?P<diopter##>[+-]\d?)*'
      r'|'
      r'(20/\D*|ni|na|nt|no improvement)'
      r'|'
      r'(20/\s*)?(?P<test##>HM|CF|LP|NLP)(\W+(@|at|x)?\s*'  # open paren: distance
      r'(?P<distance##>\d+)\s*(?P<distance_metric##>\'|"|in|ft|feet)'
      r'(?P<test2##>HM|CF|LP|NLP)?'
      r')'  # close paren: distance
      r')')
OD = r'(O\W*D|R(ight)?\W*E(ye)?)'
OS = r'(O\W*S|L(eft)?\W*E(ye)?)'
PH = r'(P\W*H|Pinhole)'
CC = r'(C\W*C|with glasses|specs|with correction)'
SC = r'(S\W*C|without glasses)'
PREVIOUS = r'(?P<previous>(Last|past|previous)\W+)?'

VaPattern = namedtuple('VaPattern', 'pattern metadata')

metadata = {
    0: {
        'laterality': Laterality.OD,
        'exam': 'vacc',
    },
    1: {
        'laterality': Laterality.OD,
        'exam': 'vaph',
    },
    2: {
        'laterality': Laterality.OS,
        'exam': 'vacc',
    },
    3: {
        'laterality': Laterality.OS,
        'exam': 'vaph',
    }
}
VA_LINE_CC = VaPattern(
    re.compile(
        rf'{PREVIOUS}(Visual\s*acc?uity|VA)\W+((snellen|distance)\W+)*'
        rf'({CC}\W+)+{OD}\W+{VA.replace("##", "_0")}\W+'
        rf'({PH}\W+({OD}\W+)?{VA.replace("##", "_1")}\W+)?'
        rf'({CC}\W+)?{OS}\W+{VA.replace("##", "_2")}\W*'
        rf'(({PH}\W+)?({OS}\W+)?{VA.replace("##", "_3")})?',
        re.I
    ), metadata
)
VA_LINE_SC = VaPattern(
    re.compile(
        rf'{PREVIOUS}(Visual\s*acc?uity|VA)\W+((snellen|distance)\W+)*'
        rf'{SC}\W+{OD}\W+{VA.replace("##", "_0")}\W+'
        rf'({PH}\W+({OD}\W+)?{VA.replace("##", "_1")}\W+)?'
        rf'({SC}\W+)?{OS}\W+{VA.replace("##", "_2")}\W*'
        rf'(({PH}\W+)?({OS}\W+)?{VA.replace("##", "_3")})?',
        re.I
    ), metadata
)
