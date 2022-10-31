import json
import pytest

from eye_extractor import iop
from eye_extractor.output.iop import build_iop


@pytest.mark.parametrize('text, re, le', [
    ('TONOMETRY: Tnct  12/19', '12.0', '19.0'),
    ('Tonometry: Method: Ta- Goldman OD: 14 mmHg OS: 15 mmHg', '14.0', '15.0'),
    ('TONOMETRY: deferred to OD', '0', '0'),
    ('INTRAOCULAR PRESSURE (IOP) by NCT:  OD n/a  mmHg OS n/a mmHg', '0', '0'),
    ('TONOMETRY: Tnct  OD Not Assessed  mmHg  OS 11 mmHg', '0', '11.0'),
    ('Tonometry: Method: NCT    Not assessed in wheel chair', '0', '0'),
    ('Tonometry; NON CONTACT METHOD:    OD 24    OS 25    mmHg', '24.0', '25.0'),
    ('TONOMETRY:nct 14//15mmHg', '14.0', '15.0'),
    ('IOP by NCT: see nursing notes  IOP Goldman: R 15mm L 16mm', '15.0', '16.0'),
    ('IOP by NCT: R 15mm L 16mm', '15.0', '16.0'),
    ('IOP by NCT: see nursing notes  IOP Goldman: R 15mm', '15.0', '0'),
    ('IOP by NCT: see nursing notes  IOP Goldman: L 15mm', '0', '15.0'),
    ('NCT performed at 10:25 PM  OD: 15  OS: 16', '15.0', '16.0'),
    ('NCT done at 10:25  OD: 11  OS: 12', '11.0', '12.0'),
    pytest.param(
        'INTRAOCULAR PRESSURE (IOP) by NCT:  OD 13  OS 12', '13.0', '12.0',
        marks=pytest.mark.skip(reason='Fix LE assumed to have 13')
    ),
    (' TONOMETRY: O.D. 12 mm; OS 13 mm', '12.0', '13.0'),
    ('Applanation Tonometry, if measured: 18OD 19OS', '18.0', '19.0'),
    ('Tonometry: Method: nt', '0', '0'),
    ('Past IOP: ¶2/22/2020»OD 10  OS 8', '10.0', '8.0'),
    ('Tonometry: Method: nt ¶Pupillary Dilation: No 2:50 PM ¶REVIEWED AND UPDATED: 12/15/2006', '0', '0'),
    ('IOPs by applanation: RE 16, LE 12 @ 0920', '16.0', '12.0'),
    ('IOPs by tech  ¶ ¶Dilated: yes, by tech   ¶Posterior Segment ¶  ¶Vitreous: RE no pigment, cells, or hg; LE no '
     'pigment, cells, or hg ¶Discs: flat, sharp, pink ¶Cupping: RE 0.9V x 0.9H; LE 0.9V x 0.9H', '0', '0'),
    ('INTRAOCULAR PRESSURE (IOP) by NCT:  OD 120 mmHg  OS 120 mmHg @ 12pm', '0', '0'),
    ('INTRAOCULAR PRESSURE (IOP) by NCT: OD *** mmHg OS *** mmHg @ ***', '0', '0'),
    ('Tonometry: Method: not done    OD:  mmHg   OS:  mmHg   6:32 PM', '0', '0'),
])
def test_iop_measurements(text, re, le):
    assert re == iop.iop_measurement_re(text)
    assert le == iop.iop_measurement_le(text)


# Test extract and build.
_iop_extract_and_build_cases = [
    ('Past IOP: ¶2/22/2020»OD 10  OS 8', 10.0, 8.0),
    ('IOPs by applanation: RE 16, LE 12 @ 0820', 16.0, 12.0),
    ('TONOMETRY (app): OD 17 OS 17 @ 1:13 PM', 17.0, 17.0),
    ('IOPs (NCT) OD 17 OS 15 @ 1211pm', 17.0, 15.0),
    ('IOPs:  15/15', 15.0, 15.0),
    ('Untreated IOP:  ¶Target IOP: OD:    OS:  ¶Date treatment started: Tmax:  ¶IOPs:  15/15', 15.0, 15.0),
    ('¶  ¶INTRAOCULAR PRESSURE(IOP)by NCT:OD 15 mmHg  OS 16 mmHg @ 1003 am ¶', 15.0, 16.0),


]


@pytest.mark.parametrize('text, exp_iop_measurement_re, exp_iop_measurement_le',
                         _iop_extract_and_build_cases)
def test_iop_extract_and_build(text, exp_iop_measurement_re, exp_iop_measurement_le):
    pre_json = list(iop.get_iop(text))
    post_json = json.loads(json.dumps(pre_json))
    result = build_iop(post_json)
    assert result['iop_measurement_re'] == exp_iop_measurement_re
    assert result['iop_measurement_le'] == exp_iop_measurement_le
