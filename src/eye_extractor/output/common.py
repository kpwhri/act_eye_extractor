from eye_extractor.output.variable import has_valid_date


def macula_is_wnl(macula_wnl, note_date=None):
    if macula_wnl:
        if not has_valid_date(note_date, macula_wnl):
            return False
        return bool(macula_wnl['value'])
