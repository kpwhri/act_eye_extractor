import enum
import re

from eye_extractor.common.negation import is_negated
from eye_extractor.laterality import build_laterality_table, create_new_variable


class CataractType(enum.IntEnum):
    UNKNOWN = 0
    NONE = 1
    NS = 2
    CS = 3
    ACS = 4
    PSC = 5


digit_pat = r'\d(?:\.\d)?(?:\-\d(?:\.\d)?)?\+?'  # digits are used to ensure
ns_pat = r'\b(?:NSC?|nuclear)\b'
NS_PAT = re.compile(
    rf'(?:'
    rf'{ns_pat}\s*(?P<severity1>{digit_pat})'
    rf'|(?P<severity2>{digit_pat})\s*{ns_pat}'
    rf'|nuclear(?:\s*sclerotic)?\s*cataract'
    rf'|nuclear\s*sclerosis'
    rf')',
    re.I)
cs_pat = r'\b(?:CS|cortical)\b'
CS_PAT = re.compile(
    rf'(?:'
    rf'{cs_pat}\s*(?P<severity1>{digit_pat})'
    rf'|(?P<severity2>{digit_pat})\s*{cs_pat}'
    rf'|cortical\s*cataract'
    rf')',
    re.I)
psc_pat = r'\b(?:PSC)\b'
PSC_PAT = re.compile(
    rf'(?:'
    rf'{psc_pat}\s*{digit_pat}'
    rf'|{digit_pat}\s*{psc_pat}'
    rf'|posterior\s*subcapsular\s*cataract'
    rf')',
    re.I)
acs_pat = r'\b(?:ACS)\b'
ACS_PAT = re.compile(
    rf'(?:'
    rf'{acs_pat}\s*(?P<severity1>{digit_pat})'
    rf'|(?P<severity2>{digit_pat})\s*{acs_pat}'
    rf')',
    re.I)


def get_cataract_type(text, *, headers=None, lateralities=None):
    if not lateralities:
        lateralities = build_laterality_table(text)
    data = []
    for pat, cattype, catlabel in [
        (NS_PAT, CataractType.NS, 'NS'),
        (CS_PAT, CataractType.CS, 'CS'),
        (ACS_PAT, CataractType.ACS, 'ACS'),
        (PSC_PAT, CataractType.PSC, 'PSC'),
    ]:
        for m in pat.finditer(text):
            negword = is_negated(m, text)
            gd = m.groupdict()
            if severity := gd.get('severity1', '') or gd.get('severity2', '') or None:
                severity = max(float(s.strip('+ ')) for s in severity.split('-'))
            else:
                severity = -1
            data.append(
                create_new_variable(text, m, lateralities, 'cataract_type', {
                    'value': CataractType.NONE if negword else cattype,
                    'term': m.group(),
                    'label': f'NO {catlabel}' if negword else catlabel,
                    'negated': negword,
                    'regex': f'{catlabel}_PAT', 'source': 'ALL',
                    'severity': severity,
                })
            )
    if headers:
        pass
    return data
