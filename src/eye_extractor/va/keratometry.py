import re

from eye_extractor.common.date import parse_date_before
from eye_extractor.laterality import laterality_pattern, lat_lookup, Laterality

_km_curve = r'(?P<gen_curve#>\d{1,2}(?:\.\d{1,2})?)'
_km_axis = r'(?P<gen_axis#>\d{1,3})'
_km = fr'{_km_curve}\s*(?:x\s*{_km_axis})?'
keratometry_pat = rf'(?P<lat#>{laterality_pattern}):\s*{_km.replace("gen", "first")}\W*{_km.replace("gen", "second")}'
axial_pat = r'(?:iol master|ascans)\W+(?P<al_od>\d{1,2}(?:\.\d{1,2})?)\W+(?P<al_os>\d{1,2}(?:\.\d{1,2})?)'

KERATOMETRY_PAT = re.compile(keratometry_pat.replace('#', ''), re.I)
AXIAL_PAT = re.compile(axial_pat, re.I)

KERA_AX_PAT = re.compile(
    rf'{keratometry_pat.replace("#", "1")}\W*'
    rf'{keratometry_pat.replace("#", "2")}\W*'
    rf'{axial_pat}',
    re.I
)


def get_by_lat(m, groupname, target_lat, lat1):
    return float(m.group(f'{groupname}{1 if lat1 == target_lat else 2}'))


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
            # track where date is: important if analyzing a table
            has_date_before = False
            has_date_after = False
            for pat_label, pat in [
                ('KERA_AX_PAT', KERA_AX_PAT),
            ]:
                for m in pat.finditer(sect_text):
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
                    data.append(
                        {'keratometry': {
                            'keratometry_flatcurve_re': min(od_measures),
                            'keratometry_steepcurve_re': max(od_measures),
                            'keratometry_flataxis_re': (
                                od_axis if od_measures[0] > od_measures[1] else (od_axis + 90) % 180
                            ),
                            'keratometry_steepaxis_re': (
                                od_axis if od_measures[0] < od_measures[1] else (od_axis + 90) % 180
                            ),
                            'keratometry_flatcurve_le': min(os_measures),
                            'keratometry_steepcurve_le': max(os_measures),
                            'keratometry_flataxis_le': (
                                os_axis if os_measures[0] > os_measures[1] else (os_axis + 90) % 180
                            ),
                            'keratometry_steepaxis_le': (
                                os_axis if os_measures[0] < os_measures[1] else (os_axis + 90) % 180
                            ),
                            'ax_length_re': float(m.group('al_od')),
                            'ax_length_le': float(m.group('al_os')),
                            'term': m.group(),
                            'regex': pat_label,
                            'source': sect_name,
                            'date': date,
                        }}
                    )
    return data
