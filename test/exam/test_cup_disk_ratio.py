import pytest

from eye_extractor.exam.cup_disk_ratio import CUP_DISK_PAT, CUP_DISC_NO_LAT_LABEL_PAT, CUP_DISC_UNILAT_PAT


@pytest.mark.parametrize('pat, text, exp_od, exp_os', [
    (CUP_DISK_PAT, 'C/D (0.27-0.55): OD 0.75 OS 0.60', '0.75', '0.60'),
    (CUP_DISK_PAT, 'C/D: OD 0.75 OS 0.60', '0.75', '0.60'),
    (CUP_DISK_PAT, 'C/D OD 0.75 OS 0.60', '0.75', '0.60'),
    (CUP_DISK_PAT, 'c/d OU 0.5', '0.5', '0.5'),
    (CUP_DISK_PAT, 'c/d 0.5 OU', '0.5', '0.5'),
    (CUP_DISK_PAT, 'c/d ratios OD 0.5 OS 0.6', '0.5', '0.6'),
    (CUP_DISK_PAT, 'c/d ratios OD 0.5 / OS 0.6', '0.5', '0.6'),
    (CUP_DISC_NO_LAT_LABEL_PAT, 'c/d ratio 0.5, 0.3', '0.5', '0.3'),
    (CUP_DISC_UNILAT_PAT, 'OD: Linear CD 0.75 (+0.03)', '0.75', None)
])
def test_cup_disk_regex(pat, text, exp_od, exp_os):
    m = pat.search(text)
    if m is None:
        assert exp_od is None and exp_os is None
    d = m.groupdict()
    assert d.get('od', None) or d.get('ou', None) or d.get('ou2', None) == exp_od
    assert d.get('os', None) or d.get('ou', None) or d.get('ou2', None) == exp_os
