import pytest

from eye_extractor.cataract.cataract_type import NS_PAT, CS_PAT, PSC_PAT, ACS_PAT, get_cataract_type, CataractType
from eye_extractor.output.cataract import build_cataract_type, build_nscataract_severity, build_pscataract_severity, \
    build_cortcataract_severity


@pytest.mark.parametrize('text', [
    'NS 3-4',
    '2-3 NS',
    'nuclear cataract',
])
def test_ns_cataract_pattern(text):
    assert NS_PAT.match(text)


@pytest.mark.parametrize('text', [
    'ACS 3-4',
    '2-3 ACS',
])
def test_acs_cataract_pattern(text):
    assert ACS_PAT.match(text)


@pytest.mark.parametrize('text', [
    'PSC 1',
    'PSC 1+',
])
def test_psc_cataract_pattern(text):
    assert PSC_PAT.match(text)


@pytest.mark.parametrize('text', [
    'CS 2',
    'CS 2-4',
    'cortical cataract',
])
def test_cs_cataract_pattern(text):
    assert CS_PAT.match(text)


@pytest.mark.parametrize('text, exp_value, exp_negword, exp_severity', [
    ('no nuclear cataract', CataractType.NONE, 'no', -1),
    ('nuclear cataract', CataractType.NS, None, -1),
    ('CS 1+', CataractType.CS, None, 1),
    ('NSC 2-4', CataractType.NS, None, 4),
    ('2 - 4 NSC', CataractType.NS, None, 4),
    ('ACS 3.5', CataractType.ACS, None, 3.5),
    ('cortical cataract', CataractType.CS, None, -1),
])
def test_cataract_value_first_variable(text, exp_value, exp_negword, exp_severity):
    data = get_cataract_type(text)
    assert len(data) > 0
    first_variable = list(data[0].values())[0]
    assert first_variable['value'] == exp_value
    assert first_variable['negated'] == exp_negword
    assert first_variable['severity'] == exp_severity


@pytest.mark.parametrize('data, exp_cataract_type_re, exp_cataract_type_le', [
    ([], CataractType.UNKNOWN, CataractType.UNKNOWN),
    ([{'cataract_type_le': 1}], CataractType.UNKNOWN, CataractType.NONE),
    ([{'cataract_type_le': 2, 'cataract_type_re': 3}], CataractType.CS, CataractType.NS),
])
def test_cataract_to_column(data, exp_cataract_type_re, exp_cataract_type_le):
    result = build_cataract_type(data)
    assert result['cataract_type_le'] == exp_cataract_type_le
    assert result['cataract_type_re'] == exp_cataract_type_re


@pytest.mark.parametrize('data, exp_nscataract_severity_re, exp_nscataract_severity_le', [
    ([], -1, -1),
    ([{'cataract_type_le': {'value': CataractType.NS.value, 'severity': -1}}], -1, -1),
    ([{'cataract_type_re': {'value': CataractType.CS.value, 'severity': 3.5}}], -1, -1),
    ([{'cataract_type_re': {'value': CataractType.NS.value, 'severity': 3.5}}], 3.5, -1),
    ([
         {'cataract_type_re': {'value': CataractType.NS.value, 'severity': 3.5},
          'cataract_type_le': {'value': CataractType.NS.value, 'severity': 3.5},
          },
         {'cataract_type_re': {'value': CataractType.NS.value, 'severity': 4},
          'cataract_type_le': {'value': CataractType.NS.value, 'severity': 2},
          },
     ],
     4, 3.5),
])
def test_nscataract_severity(data, exp_nscataract_severity_re, exp_nscataract_severity_le):
    result = build_nscataract_severity(data)
    assert result['nscataract_severity_le'] == exp_nscataract_severity_le
    assert result['nscataract_severity_re'] == exp_nscataract_severity_re


@pytest.mark.parametrize('data, exp_cortcataract_severity_re, exp_cortcataract_severity_le', [
    ([], -1, -1),
    ([{'cataract_type_le': {'value': CataractType.CS.value, 'severity': -1}}], -1, -1),
    ([{'cataract_type_le': {'value': CataractType.ACS.value, 'severity': -1}}], -1, -1),
    ([{'cataract_type_re': {'value': CataractType.NS.value, 'severity': 3.5}}], -1, -1),
    ([{'cataract_type_re': {'value': CataractType.CS.value, 'severity': 3.5}}], 3.5, -1),
    ([{'cataract_type_re': {'value': CataractType.ACS.value, 'severity': 3.5}}], 3.5, -1),
    ([
         {'cataract_type_re': {'value': CataractType.CS.value, 'severity': 3.5},
          'cataract_type_le': {'value': CataractType.CS.value, 'severity': 3.5},
          },
         {'cataract_type_re': {'value': CataractType.ACS.value, 'severity': 4},
          'cataract_type_le': {'value': CataractType.ACS.value, 'severity': 2},
          },
     ],
     4, 3.5),
])
def test_nscataract_severity(data, exp_cortcataract_severity_re, exp_cortcataract_severity_le):
    result = build_cortcataract_severity(data)
    assert result['cortcataract_severity_le'] == exp_cortcataract_severity_le
    assert result['cortcataract_severity_re'] == exp_cortcataract_severity_re


@pytest.mark.parametrize('data, exp_pscataract_severity_re, exp_pscataract_severity_le', [
    ([], -1, -1),
    ([{'cataract_type_le': {'value': CataractType.PSC.value, 'severity': -1}}], -1, -1),
    ([{'cataract_type_re': {'value': CataractType.CS.value, 'severity': 3.5}}], -1, -1),
    ([{'cataract_type_re': {'value': CataractType.PSC.value, 'severity': 3.5}}], 3.5, -1),
    ([
         {'cataract_type_re': {'value': CataractType.PSC.value, 'severity': 3.5},
          'cataract_type_le': {'value': CataractType.PSC.value, 'severity': 3.5},
          },
         {'cataract_type_re': {'value': CataractType.PSC.value, 'severity': 4},
          'cataract_type_le': {'value': CataractType.PSC.value, 'severity': 2},
          },
     ],
     4, 3.5),
])
def test_pscataract_severity(data, exp_pscataract_severity_re, exp_pscataract_severity_le):
    result = build_pscataract_severity(data)
    assert result['pscataract_severity_le'] == exp_pscataract_severity_le
    assert result['pscataract_severity_re'] == exp_pscataract_severity_re
