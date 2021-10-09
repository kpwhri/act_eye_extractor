import pytest

from eye_extractor import iop


@pytest.mark.parametrize('text, re, le', [
    ('TONOMETRY: Tnct  12/19', '12.0', '19.0'),
    ('Tonometry: Method: Ta- Goldman OD: 14 mmHg OS: 15 mmHg', '14.0', '15.0'),
    ('TONOMETRY: deferred to OD', '0', '0'),
    ('TONOMETRY: Tnct  OD Not Assessed  mmHg  OS 11 mmHg', '0', '11.0'),
    ('Tonometry: Method: NCT    Not assessed in wheel chair', '0', '0'),
    ('Tonometry; NON CONTACT METHOD:    OD 24    OS 25    mmHg', '24.0', '25.0'),
    ('TONOMETRY:nct 14//15mmHg', '14.0', '15.0'),
    ('IOP by NCT: see nursing notes  IOP Goldman: R 15mm L 16mm', '15.0', '16.0'),
    ('IOP by NCT: R 15mm L 16mm', '15.0', '16.0'),
    ('NCT performed at 10:25 PM  OD: 15  OS: 16', '15.0', '16.0'),
])
def test_iop_measurements(text, re, le):
    assert re == iop.iop_measurement_re(text)
    assert le == iop.iop_measurement_le(text)
