from eye_extractor.laterality import Laterality


def laterality_from_int(val):
    match val:
        case 0:
            return Laterality.OD
        case 1:
            return Laterality.OS
        case 2:
            return Laterality.OU
    return Laterality.UNKNOWN


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