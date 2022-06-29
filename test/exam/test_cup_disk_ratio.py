import pytest

from eye_extractor.exam.cup_disk_ratio import CUP_DISK_PAT, CUP_DISC_NO_LAT_LABEL_PAT


@pytest.mark.parametrize('pat, text, exp_od, exp_os', [
    (CUP_DISK_PAT, 'C/D (0.27-0.55): OD 0.75 OS 0.60', '0.75', '0.60'),
    (CUP_DISK_PAT, 'C/D: OD 0.75 OS 0.60', '0.75', '0.60'),
    (CUP_DISK_PAT, 'C/D OD 0.75 OS 0.60', '0.75', '0.60'),
    (CUP_DISK_PAT, 'c/d OU 0.5', '0.5', '0.5'),
    (CUP_DISK_PAT, 'c/d 0.5 OU', '0.5', '0.5'),
    (CUP_DISK_PAT, 'c/d ratios OD 0.5 OS 0.6', '0.5', '0.6'),
    (CUP_DISK_PAT, 'c/d ratios OD 0.5 / OS 0.6', '0.5', '0.6'),
    (CUP_DISC_NO_LAT_LABEL_PAT, 'c/d ratio 0.5, 0.3', '0.5', '0.3'),
])
def test_cup_disk_regex(pat, text, exp_od, exp_os):
    m = pat.search(text)
    if m is None:
        assert exp_od is None and exp_os is None
    assert m.group('od') or m.group('ou') or m.group('ou2') == exp_od
    assert m.group('os') or m.group('ou') or m.group('ou2') == exp_os
