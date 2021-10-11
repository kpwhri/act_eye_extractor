import pytest

from eye_extractor.cataract.cataract import IOL_TYPE_PAT, get_iol_type


@pytest.mark.parametrize('text, kinds', [
    ('Primary IOL:  SN6AT5 17.5 diopter   TORIC LENS  Secondary IOL: SN60WF17.5 D, MA60AC 16.5 D',
     [('SN6AT5', 17.5), ('SN60WF', 17.5), ('MA60AC', 16.5)]
     ),
    (' Primary IOL: SN60WF: diopter with 23 Secondary IOL: MTA 400-AC: diopter with 20',
     [('SN60WF', 23), ('MTA 400-AC', 20)]
     )
])
def test_iol_primary_type(text, kinds):
    results = list(get_iol_type(text))
    for res, (model, diopter) in zip(results, kinds):
        assert res['model'] == model
        assert res['power'] == diopter


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
