from eye_extractor.rao.rao import get_rao


def extract_ro_variables(text, *, headers=None, lateralities=None):
    return {
        'ro': get_rao(text, headers=headers, lateralities=lateralities),
    }
