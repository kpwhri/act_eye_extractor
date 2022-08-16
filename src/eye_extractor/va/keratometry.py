import re

from eye_extractor.common.date import parse_date_before
from eye_extractor.laterality import laterality_pattern, lat_lookup, Laterality

_km_curve = r'(?P<gen_curve#>\d{1,2}(?:\.\d{1,2})?)'
_km_axis = r'(?P<gen_axis#>\d{1,3})'
_km = fr'{_km_curve}\s*(?:[x@]\s*{_km_axis})?'
keratometry_pat = rf'(?P<lat#>{laterality_pattern}):\s*{_km.replace("gen", "first")}\W*{_km.replace("gen", "second")}'
axial_pat = r'(?:iol master|ascans)\W+(?P<al_od>\d{1,2}(?:\.\d{1,2})?)\W+(?P<al_os>\d{1,2}(?:\.\d{1,2})?)'
_random_text = r'.{1,20}'  # allow notes/obs

KERATOMETRY_HEADER_PAT = re.compile(
    rf'(?:auto\W*)?keratometry',
    re.I
)

KERA_AX_PAT = re.compile(
    rf'{keratometry_pat.replace("#", "1")}{_random_text}'
    rf'{keratometry_pat.replace("#", "2")}{_random_text}'
    rf'{axial_pat}',
    re.I
)

KERATOMETRY_PAT = re.compile(
    rf'{keratometry_pat.replace("#", "1")}{_random_text}'
    rf'{keratometry_pat.replace("#", "2")}',
    re.I
)

AXIAL_PAT = re.compile(axial_pat, re.I)


def get_by_lat(m, groupname, target_lat, lat1):
    res = m.group(f'{groupname}{1 if lat1 == target_lat else 2}')
    if not res:
        return -1.0
    else:
        return float(res)


def extract_keratometry(text, *, headers=None, lateralities=None):
    """
    Flat is smaller than steep.

    :param text:
    :param headers:
    :param lateralities:
    :return:
    """
    data = []
    if headers:
        for sect_name, sect_text in headers.iterate(
                'KERATOMETRY'
        ):  # TODO: other sections?
            for result in _extract_keratometry(sect_name, sect_text):
                data.append(result)
    if not data:
        for m in KERATOMETRY_HEADER_PAT.finditer(text):
            for result in _extract_keratometry('ALL', text[m.end():m.end() + 150]):
                data.append(result)
    return data


def _extract_keratometry(sect_name, sect_text):
    # track where date is: important if analyzing a table
    has_date_before = False
    has_date_after = False
    for pat_label, pat in [
        ('KERA_AX_PAT', KERA_AX_PAT),
        ('KERATOMETRY_PAT', KERATOMETRY_PAT),
    ]:
        for m in pat.finditer(sect_text):
            gd = m.groupdict()
            date = None
            if not has_date_after:  # don't look before if date already found after
                if date := parse_date_before(m, sect_text):  # check before first
                    has_date_before = True
            if not has_date_before:  # don't look after if date already found before
                if date := parse_date_before(m, sect_text):
                    has_date_after = True
            lat1 = lat_lookup(m, group='lat1')
            lat2 = lat_lookup(m, group='lat2')
            od_measures = (
                get_by_lat(m, 'first_curve', Laterality.OD, lat1),
                get_by_lat(m, 'second_curve', Laterality.OD, lat1),
            )
            od_axis = get_by_lat(m, 'second_axis', Laterality.OD, lat1)
            os_measures = (
                get_by_lat(m, 'first_curve', Laterality.OS, lat1),
                get_by_lat(m, 'second_curve', Laterality.OS, lat1),
            )
            os_axis = get_by_lat(m, 'second_axis', Laterality.OS, lat1)
            yield {'keratometry': {
                'keratometry_flatcurve_re': min(od_measures),
                'keratometry_steepcurve_re': max(od_measures),
                'keratometry_flataxis_re': calc_axis(od_measures, od_axis, is_flat=True),
                'keratometry_steepaxis_re': calc_axis(od_measures, od_axis, is_flat=False),
                'keratometry_flatcurve_le': min(os_measures),
                'keratometry_steepcurve_le': max(os_measures),
                'keratometry_flataxis_le': calc_axis(os_measures, os_axis, is_flat=True),
                'keratometry_steepaxis_le': calc_axis(os_measures, os_axis, is_flat=False),
                'ax_length_re': float(gd.get('al_od', -1.0)),
                'ax_length_le': float(gd.get('al_os', -1.0)),
                'term': m.group(),
                'regex': pat_label,
                'source': sect_name,
                'date': date,
            }}
    # TODO: add just AXIAL pattern


def calc_axis(measures, axis, *, is_flat):
    if axis == -1:
        return -1
    elif is_flat:
        return axis if measures[0] > measures[1] else (axis + 90) % 180
    else:  # is steep
        return axis if measures[0] < measures[1] else (axis + 90) % 180
