import pytest

from eye_extractor.exam.cup_disk_ratio import CUP_DISK_PAT


@pytest.mark.parametrize('text, exp_od, exp_os', [
    ('C/D (0.27-0.55): OD 0.75 OS 0.60', '0.75', '0.60'),
    ('C/D: OD 0.75 OS 0.60', '0.75', '0.60'),
    ('C/D OD 0.75 OS 0.60', '0.75', '0.60'),
    ('c/d OU 0.5', '0.5', '0.5'),
    ('c/d 0.5 OU', '0.5', '0.5'),
    ('c/d ratios OD 0.5 OS 0.6', '0.5', '0.6'),
    ('c/d ratios OD 0.5 / OS 0.6', '0.5', '0.6'),
])
def test_cup_disk_regex(text, exp_od, exp_os):
    m = CUP_DISK_PAT.search(text)
    assert m is not None
    assert m.group('od') or m.group('ou') or m.group('ou2') == exp_od
    assert m.group('os') or m.group('ou') or m.group('ou2') == exp_os
