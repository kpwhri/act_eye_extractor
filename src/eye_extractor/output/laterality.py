from eye_extractor.laterality import Laterality


def laterality_from_int(val):
    return Laterality(val)


def laterality_iter(lat: Laterality):
    match lat:
        case Laterality.OD:
            return 're',
        case Laterality.OS:
            return 'le',
        case Laterality.OU:
            return 'le', 're'
    # TODO: how to incorporate 'unknown'?
    return []
