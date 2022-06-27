import pytest

from eye_extractor.exam.cup_disk_ratio import CUP_DISK_PAT


@pytest.mark.parametrize('text, exp_od, exp_os', [
    ('C/D (0.27-0.55): OD 0.75 OS 0.60', '0.75', '0.60'),
])
def test_cup_disk_regex(text, exp_od, exp_os):
    m = CUP_DISK_PAT.search(text)
    assert m.group('od') == exp_od
    assert m.group('os') == exp_os
