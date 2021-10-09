import pytest

from eye_extractor import iop


@pytest.mark.parametrize('text, re, le', [
    ('TONOMETRY: Tnct  12/19', '12.0', '19.0'),
    ('Tonometry: Method: Ta- Goldman OD: 14 mmHg OS: 15 mmHg', '14.0', '15.0'),
    ('TONOMETRY: deferred to OD', '0', '0'),
    ('Tonometry; NON CONTACT METHOD:    OD 24    OS 24    mmHg', '24.0', '24.0'),
])
def test_iop_measurements(text, re, le):
    assert re == iop.iop_measurement_re(text)
    assert le == iop.iop_measurement_le(text)
