from eye_extractor.output.variable import column_from_variable_abbr


def build_uveitis_variables(data):
    curr = data['uveitis']
    note = data['note']
    results = {}
    results.update(build_uveitis(curr['uveitis'], note_date=note['date']))
    return results


def build_uveitis(data, *, note_date=None):
    return column_from_variable_abbr('uveitis_yesno', -1, data, restrict_date=note_date)
