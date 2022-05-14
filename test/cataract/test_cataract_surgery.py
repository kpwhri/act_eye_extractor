import datetime

import pytest

from eye_extractor.cataract.cataract_surgery import IOL_TYPE_PAT, get_iol_type, get_cataract_laterality, get_surgery_date, \
    cataractsurg_ioltype
from eye_extractor.laterality import Laterality


@pytest.mark.parametrize('text, kinds', [
    ('Primary IOL:  SN6AT5 17.5 diopter   TORIC LENS  Secondary IOL: SN60WF17.5 D, MA60AC 16.5 D',
     [('SN6AT5', 17.5),
      ('SN60WF', 17.5),
      ('MA60AC', 16.5)]
     ),
    (' Primary IOL: SN60WF: diopter with 23 Secondary IOL: MTA 400-AC: diopter with 20',
     [('SN60WF', 23),
      ('MTA 400-AC', 20)]
     )
])
def test_iol_primary_type(text, kinds):
    results = list(get_iol_type(text, get_kind=False))
    for res, (model, diopter) in zip(results, kinds):
        assert res['model'] == model
        assert res['power'] == diopter


@pytest.mark.parametrize('text, kinds', [
    ('Primary IOL:  SN6AT5 17.5 diopter   TORIC LENS  Secondary IOL: SN60WF17.5 D, MA60AC 16.5 D',
     {Laterality.UNKNOWN: [{'model': 'SN6AT5', 'power': 17.5, 'primary': True},
                           {'model': 'SN60WF', 'power': 17.5, 'primary': False},
                           {'model': 'MA60AC', 'power': 16.5, 'primary': False}]}
     ),
    (' Which eye?: LEFT Primary IOL: SN60WF: diopter with 23 Secondary IOL: MTA 400-AC: diopter with 20',
     {Laterality.OS: [{'model': 'SN60WF', 'power': 23, 'primary': True},
                      {'model': 'MTA 400-AC', 'power': 20, 'primary': False}]}
     )
])
def test_cataractsurg_ioltype(text, kinds):
    results = dict(cataractsurg_ioltype(text))
    for lat in results:
        for result, kind in zip(results[lat], kinds[lat]):
            assert result['model'] == kind['model']
            assert result['power'] == kind['power']
            assert result['primary'] == kind['primary']


@pytest.mark.parametrize('text, model, power', [
    ('SN6AT5 17.5 diopter', 'SN6AT5', '17.5'),
    ('SN60WF: diopter with 17.00', 'SN60WF', '17.00'),
    ('SN60WF: +18.5 D', 'SN60WF', '18.5'),
])
def test_iol_type_pat(text, model, power):
    m = IOL_TYPE_PAT.search(text)
    assert m is not None
    assert m.group('model') == model
    assert m.group('power') or m.group('power2') == power


@pytest.mark.parametrize('text, lat', [
    ('Which Side?: Left', Laterality.OS),
    ('Which Side?: Right', Laterality.OD),
])
def test_cataract_laterality(text, lat):
    res = list(get_cataract_laterality(text))[0]
    assert res['laterality'] == lat


@pytest.mark.parametrize('text, exp', [
    ('Surgery Date:   September 14,2012    H&P:  Schedule',
     datetime.datetime(2012, 9, 14)),
    ('Surgery Date:   12/6/2014   MORE TITLES H&P',
     datetime.datetime(2014, 12, 6))
])
def test_surgery_date(text, exp):
    date = get_surgery_date(text)
    assert exp == date
