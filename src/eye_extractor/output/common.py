from eye_extractor.laterality import Laterality
from eye_extractor.output.variable import has_valid_date


def macula_is_wnl(macula_wnl, note_date=None):
    if macula_wnl:
        if not has_valid_date(note_date, macula_wnl):
            return None
        if macula_wnl['value'] == 1:
            return Laterality(macula_wnl['lat'])
