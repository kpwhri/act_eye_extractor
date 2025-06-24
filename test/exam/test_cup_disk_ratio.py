import pytest

from eye_extractor.common.regex import coalesce_match
from eye_extractor.exam.cup_disk_ratio import CUP_DISK_PAT, CUP_DISC_NO_LAT_LABEL_PAT, CUP_DISC_UNILAT_PAT, OD_CUP_DISC, \
    OS_CUP_DISC
from eye_extractor.sections.document import create_doc_and_sections


@pytest.mark.parametrize('pat, text, exp_od, exp_os', [
    (CUP_DISK_PAT, 'C/D (0.27-0.55): OD 0.75 OS 0.60', '0.75', '0.60'),
    (CUP_DISK_PAT, 'C/D: OD 0.75 OS 0.60', '0.75', '0.60'),
    (CUP_DISK_PAT, 'C/D OD 0.75 OS 0.60', '0.75', '0.60'),
    (CUP_DISK_PAT, 'c/d OU 0.5', '0.5', '0.5'),
    (CUP_DISK_PAT, 'c/d 0.5 OU', '0.5', '0.5'),
    (CUP_DISK_PAT, 'c/d ratios OD 0.5 OS 0.6', '0.5', '0.6'),
    (CUP_DISK_PAT, 'c/d ratios OD 0.5 / OS 0.6', '0.5', '0.6'),
    (CUP_DISC_NO_LAT_LABEL_PAT, 'c/d ratio 0.5, 0.3', '0.5', '0.3'),
    (OD_CUP_DISC, 'OD CUP/DISC: 0.6', '0.6', None),
    (OS_CUP_DISC, 'OS CUP/DISC: 0.6', None, '0.6'),
])
def test_cup_disk_regex(pat, text, exp_od, exp_os):
    m = pat.search(text)
    if m is None:
        assert exp_od is None and exp_os is None
    else:
        assert coalesce_match(m, 'od', 'od2', 'ou', 'ou2') == exp_od
        assert coalesce_match(m, 'os', 'os2', 'ou', 'ou2') == exp_os


@pytest.mark.parametrize('text, exp_lat, exp_ratio', [
    ('OD: Linear CD 0.75 (+0.03)', 'od', '0.75'),
])
def test_disc_unilat_pat(text, exp_lat, exp_ratio):
    m = CUP_DISC_UNILAT_PAT.search(text)
    if m is None:
        assert exp_lat is None and exp_ratio is None
    else:
        assert m.group(exp_lat) is not None
        assert m.group('ratio') == exp_ratio


# TODO: OD CUP/DISC: V 0.55/ H 0.55 sl pale
#   OS CUP/DISC: V 0.55/ H 0.55 s
# large c/d
# TEST SECTIONS: doc = create_doc_and_sections(text, sections)
