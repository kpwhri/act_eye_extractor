import json

import pytest

from eye_extractor.headers import Headers
from eye_extractor.output.keratometry import build_keratometry
from eye_extractor.va.keratometry import extract_keratometry, KERA_AX_PAT


@pytest.mark.parametrize('pat, text, exp', [
    (KERA_AX_PAT, 'OD: 41.50/39.00 x 060  OS: 41.00/38.00 x 125  IOL Master: 24.20, 23.80', True),
])
def test_keratometry_patterns(pat, text, exp):
    assert bool(pat.search(text)) == exp


@pytest.mark.parametrize(
    'text, headers, keratometry_flatcurve_re, keratometry_flatcurve_le, '
    'keratometry_steepcurve_re, keratometry_steepcurve_le, '
    'keratometry_flataxis_re, keratometry_flataxis_le, '
    'keratometry_steepaxis_re, keratometry_steepaxis_le, '
    'ax_length_re, ax_length_le', [
        ('', {'KERATOMETRY': 'OD: 41.50/39.00 x 060  OS: 41.00/38.00 x 125  IOL Master: 24.20, 23.80'},
         39.00, 38.00, 41.50, 41.00, 60, 125, 150, 35, 24.20, 23.80
         ),
        ('', {'KERATOMETRY': 'OD: 39.00/41.50 x 060  OS: 38.00/41.00 x 125  Ascans: 24.20, 23.80'},
         39.00, 38.00, 41.50, 41.00, 150, 35, 60, 125, 24.20, 23.80
         ),
        ('', {'KERATOMETRY': 'OD:45.00/44.00x180  OS:44.40/43.90   Ascans: 25.60, 26.21'},
         44.00, 43.90, 45.00, 44.40, 180, 0, 90, 90, 25.60, 26.21
         ),
        ('', {'KERATOMETRY': 'Auto-Keratometry  OD: 44.00 @ 175 / 45.00 @ 085  OS: 44.75 @ 005 / 46.00 @ 095'},
         44.00, 44.75, 45.00, 46.00, 175, 5, 85, 95, -1, -1,
         ),
        ('Auto-Keratometry  OD: 44.00 @ 175 / 45.00 @ 085  OS: 44.75 @ 005 / 46.00 @ 095', {},
         44.00, 44.75, 45.00, 46.00, 175, 5, 85, 95, -1, -1,
         ),
    ])
def test_extract_keratometry(
        text, headers, keratometry_flatcurve_re, keratometry_flatcurve_le,
        keratometry_steepcurve_re, keratometry_steepcurve_le,
        keratometry_flataxis_re, keratometry_flataxis_le,
        keratometry_steepaxis_re, keratometry_steepaxis_le,
        ax_length_re, ax_length_le):
    pre_json = extract_keratometry(text, headers=Headers(headers))
    post_json = json.loads(json.dumps(pre_json))
    print(post_json)
    result = build_keratometry(post_json)
    print(result)
    assert result['keratometry_flatcurve_re'] == keratometry_flatcurve_re
    assert result['keratometry_flatcurve_le'] == keratometry_flatcurve_le
    assert result['keratometry_steepcurve_re'] == keratometry_steepcurve_re
    assert result['keratometry_steepcurve_le'] == keratometry_steepcurve_le
    assert result['keratometry_flataxis_re'] == keratometry_flataxis_re
    assert result['keratometry_flataxis_le'] == keratometry_flataxis_le
    assert result['keratometry_steepaxis_re'] == keratometry_steepaxis_re
    assert result['keratometry_steepaxis_le'] == keratometry_steepaxis_le
    assert result['ax_length_re'] == ax_length_re
    assert result['ax_length_le'] == ax_length_le
