import re

from eye_extractor.laterality import LATERALITY_PATTERN, laterality_finder, Laterality

AMD_RX = re.compile(
    r'('
    r'\bamd\b'
    r'|(age\Wrelated )?macular degener\w+'
    r'|macular\s+degener\w+'
    r')',
    re.I
)


def delimiter_split(text, keep_last=False):
    split = re.split(r'(?:\n\s*\n|:|\.)', text)
    if keep_last:
        return split[-1]
    return split[0]


def get_laterality(match, text):
    # check after
    lat = None
    for lat in laterality_finder(
            delimiter_split(text[match.end():match.end() + 50])
    ):
        print(f'Found pre-lat: {lat}')
        return lat
    # check latest in pre-text
    for lat in laterality_finder(
            delimiter_split(text[max(0, match.start()) - 50:match.start()], keep_last=True)
    ):
        print(f'Found post-lat: {lat}')
        pass
    if lat:
        return lat
    return Laterality.UNKNOWN


def get_amd(text):
    data = []
    for m in AMD_RX.finditer(text):
        data.append({
            'label': 'amd',
            'term': m.group(),
            'laterality': get_laterality(m, text),
        })
    return data


def get_amd_old(text):
    """
    Dx code: AMD (age related macular degeneration)     362.50, H35.30
    :return:
    """
    lats = set()
    for m in AMD_RX.finditer(text):
        print(f'Found AMD: {m.group()}')
        lats.add(get_laterality(m, text))
    return lats


def amd_le(text):
    lats = get_amd_old(text)
    print(f'Found lats: {lats}')
    if {Laterality.OS, Laterality.OU} & lats:
        return '1.0'  # yes
    elif lats:  # any mention
        return '0.0'
    return '8.0'  # no mention


def amd_re(text):
    lats = get_amd_old(text)
    print(f'Found lats: {lats}')
    if {Laterality.OD, Laterality.OU} & lats:
        return '1.0'  # yes
    elif lats:  # any mention
        return '0.0'
    return '8.0'  # no mention
