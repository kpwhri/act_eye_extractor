from eye_extractor.uveitis.uveitis import get_uveitis


def extract_uveitis(text, *, headers=None, lateralities=None):
    results = {}
    results['uveitis'] = get_uveitis(text, headers=headers, lateralities=lateralities)
    return results
