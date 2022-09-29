"""
Approach:
1. Find the score
2. Find the laterality
3. Find other classification
"""
import re
import enum

from loguru import logger

from eye_extractor.laterality import Laterality, LATERALITY, LATERALITY_PATTERN, lat_lookup
from eye_extractor.va.pattern import VA_LINE_CC, VA_LINE_SC, VA_LINE_GROUPED


class VisualAcuity(enum.Enum):
    OTHER = 0
    VISUAL_ACUITY = 1
    SNELLEN = 2
    CORRECTED = 3
    PINHOLE = 4
    UNCORRECTED = 5
    NEAR = 6
    HISTORICAL = 7
    RX = 8
    ETDRS = 9


VISUAL_ACUITY = {
    'BEST CORRECTED ACUITIES WITH ABOVE REFRACTION': [VisualAcuity.RX],
    'BEST CORRECTED VISION': [VisualAcuity.RX],
    'BEST CORRECTED': [VisualAcuity.OTHER],
    'REFRACTION': [VisualAcuity.OTHER],
    'NEAR VA': [VisualAcuity.VISUAL_ACUITY, VisualAcuity.NEAR],
    'PREVIOUS VISUAL ACUITY': [VisualAcuity.HISTORICAL],
    'VA': [VisualAcuity.VISUAL_ACUITY],
    'VISUAL ACUITY': [VisualAcuity.VISUAL_ACUITY],
    'VISUAL ACCUITY': [VisualAcuity.VISUAL_ACUITY],
    'SC': [VisualAcuity.UNCORRECTED],
    'PINHOLE': [VisualAcuity.PINHOLE],
    'PH': [VisualAcuity.PINHOLE],
    'CORRECTED': [VisualAcuity.CORRECTED],
    'UNCORRECTED': [VisualAcuity.UNCORRECTED],
    'IOL': [VisualAcuity.UNCORRECTED],
    'WITH GLASSES': [VisualAcuity.CORRECTED],
    'CORRECTION': [VisualAcuity.CORRECTED],
    'CC': [VisualAcuity.CORRECTED],
    'C': [VisualAcuity.CORRECTED],  # handle a typo
    'SNELLEN': [VisualAcuity.SNELLEN],
    'ETDRS': [VisualAcuity.ETDRS],
    'LIGHTHOUSE': [VisualAcuity.ETDRS],
}
KEYWORD_PATTERN = re.compile(
    fr'\b({"|".join(VISUAL_ACUITY.keys())})\b',
    re.IGNORECASE
)

STOPWORDS = {
    'HISTORY', 'DIABETES', 'HYPERTENSION', 'THYROID', 'HYPERTENSION',
    'DILATION', 'TONOMETRY', 'CATARACTS', 'BLINDNESS', 'DETACHMENT',
}

STOPWORDS_PATTERN = re.compile(
    fr'\b({"|".join(STOPWORDS)})\b',
    re.IGNORECASE
)

VA_PATTERN = re.compile(
    r'(?:\s|^|~|:)(?P<numerator>20|3E|E)/\s*(?P<score>(?:\d+|NT|NA))\s*(?P<sign>[+|-])*\s*(?P<diopter>\d)*'
    r'|(?:20/\s*)?(?P<test>HM|CF|LP|NLP)(?:\W+(?:@|at|x)?\s*'
    r'(?P<distance>\d+)\s*(?P<distance_metric>\'|"|in|ft|feet)'
    r'(?P<test2>HM|CF|LP|NLP)?'
    r'|$)',
    re.I
)


def get_all_keywords(text):
    """

    :param text:
    :return: keyword, start  index, labels, is_stopword
    """
    for m in KEYWORD_PATTERN.finditer(text):
        yield m.group(), m.start(), VISUAL_ACUITY[m.group().upper()], False


def get_all_stopwords(text):
    for m in STOPWORDS_PATTERN.finditer(text):
        yield m.group(), m.start(), None, True


def get_keywords_stopwords(text):
    return sorted(list(get_all_keywords(text)) + list(get_all_stopwords(text)),
                  key=lambda x: -x[1])


def get_laterality(lateralities, finding_start, finding_end):
    last = None
    for i, (term, start, label) in enumerate(lateralities):
        if start > finding_start:  # is after
            # is previous close by?
            if last and finding_start - last[1] < 50:
                return last[2]
            elif start - finding_end < 50:
                return label
            elif last:
                return last[2]
            else:
                return Laterality.UNKNOWN
        last = (term, start, label)
    return Laterality.UNKNOWN


def get_keywords_in_range(keywords, word_start, end_context):
    results = []
    not_list = set()
    for i, (keyword, start_idx, labels, is_stopword) in enumerate(keywords):  # from end of note
        if end_context <= start_idx:  # found end context
            continue  # too far after the word
        # if not results:  # nothing yet added
        #     if i > 0 and keywords[i-1][2] and VisualAcuity.PINHOLE in keywords[i-1][2]:
        #         not_list.add(VisualAcuity.PINHOLE)
        if start_idx < word_start and is_stopword:
            return results
        if is_stopword:
            continue
        if start_idx > word_start and (
                len(labels) > 1 or labels[0] not in (VisualAcuity.CORRECTED, VisualAcuity.UNCORRECTED)):
            continue  # only allow correction after the score
        for label in labels:
            if label not in results and label not in not_list:
                results.append(label)
        if len(results) >= 3:
            return results
    return results
    # look for categories
    # first date
    # first VA
    # first test type


def sum_diopter(diopter):
    """
    Sum diopter values. Assumes no value > 9
    :param diopter:
    :return:
    """
    start = 0
    nums = {str(x) for x in range(10)}
    i = 0
    while diopter and i < len(diopter):
        if diopter[i] in {'-', '+'}:
            if i + 1 < len(diopter) and diopter[i + 1] in nums:
                start += int(diopter[i:i + 2])
                i += 2
            else:
                start += int(f'{diopter[i]}1')
                i += 1
        elif diopter[i] in nums:
            start += int(diopter[i])
            i += 1
        else:
            raise ValueError(f'Unexpected diopter value: {diopter[i]} in {diopter}')
    return start


def handle_test_from_groups(groupdict):
    """
    G
    :type groupdict: match.groupdict for basic visual acuity pattern
    :return: 
    """
    test = groupdict['test'] or groupdict.get('test2', None) or groupdict.get('test3', None)
    if not test:
        return {
            'numerator': groupdict['numerator'],
            'denominator': groupdict['score'],
            'correct': sum_diopter(groupdict['diopter']),
        }
    elif test.upper() in {'CF', 'HM', 'LP', 'NLP'}:
        return {
            'distance': groupdict['distance'],
            'distance_metric': groupdict['distance_metric'],
            'test': test,
        }
    logger.info(f'Not handled exam: {test}')


def get_elements_from_line(m, metadata):
    d = m.groupdict()
    shared = d.get('shared', dict())
    lst = []
    for i in range(len(metadata)):
        src = {k.rsplit('_', 1)[0]: v for k, v in d.items() if k.endswith(f'_{i}')}
        dest = metadata[i] | shared
        dest['text'] = m.group()
        dest |= handle_test_from_groups(src)
        lst.append(dest)
    return lst


def get_number_correct(sign, diopter):
    if sign and diopter:
        return f'{sign}{diopter}'
    if sign:
        return f'{sign}1'
    if diopter:
        return f'+{diopter}'
    return ''


def extract_va_precise(text):
    rows = []
    for va_pat in (VA_LINE_GROUPED, VA_LINE_CC, VA_LINE_SC):
        for m in va_pat.pattern.finditer(text):
            rows += get_elements_from_line(m, va_pat.metadata)
        text = va_pat.pattern.sub(' ', text)
    return rows, text


def extract_va(text):
    # TODO: Remove pilcrows and other frivolous punctuation.
    rows, text = extract_va_precise(text)
    # TODO: Add function for missing VA values.
    yield rows
    # find other terms
    keywords = get_keywords_stopwords(text)
    lateralities = [(m.group(), m.start(), lat_lookup(m)) for m in LATERALITY_PATTERN.finditer(text)]
    matches = [(m, m.start(), m.end()) for m in VA_PATTERN.finditer(text)]
    for i, (m, start, end) in enumerate(matches):
        not_list = set()  # handle table order where CC/PH -> CC/PH
        if len(matches) > i + 1:
            next_start = matches[i + 1][1] - m.end()
        else:
            next_start = 1000
        try:
            next_sc = text[m.end():].index(':')
            for j, letter in enumerate(text[m.end():m.end() + next_sc][::-1]):
                if letter == ' ':
                    next_sc -= j
                    if text[m.end() + next_sc:m.end() + next_sc + j].upper() == 'PH':
                        # if the next section is PH, then I cannot be in PH section right now
                        not_list.add(VisualAcuity.PINHOLE)
                    if text[m.end() + next_sc:m.end() + next_sc + j].upper() == 'SC':
                        # if the next section is SC, then I cannot be in SC section right now
                        not_list.add(VisualAcuity.UNCORRECTED)
                    if text[m.end() + next_sc:m.end() + next_sc + j].upper() == 'CC':
                        # if the next section is CC, then I cannot be in CC section right now
                        not_list.add(VisualAcuity.CORRECTED)
                    break
        except ValueError as e:
            next_sc = 1000
        end_context = m.end() + min((next_start, next_sc, 50))
        results = get_keywords_in_range(keywords, start, end_context)
        if not results:
            continue
        results = list(set(results) - not_list)
        values = handle_test_from_groups(m.groupdict())
        if not values:
            continue
        values['laterality'] = get_laterality(lateralities, m.start(), m.end())

        if VisualAcuity.HISTORICAL in results:
            values['historical'] = 'historical'
        if VisualAcuity.OTHER in results and VisualAcuity.RX not in results:
            values['ignore'] = True

        if VisualAcuity.RX in results:
            values['exam'] = 'varx'
        elif VisualAcuity.PINHOLE in results:
            values['exam'] = 'vaph'
        elif VisualAcuity.CORRECTED in results:
            values['exam'] = 'vacc'
        elif VisualAcuity.UNCORRECTED in results:
            values['exam'] = 'vasc'
        elif VisualAcuity.SNELLEN in results:  # not sure why this works?
            values['exam'] = 'vasc'
        else:
            # print(f'Unrecognized exam: {results} {values}')
            continue

        values['format'] = 'etdrs' if VisualAcuity.ETDRS in results else 'snellen'
        yield values


def vacc_numbercorrect(text, laterality):
    for result in extract_va(text):
        if result['laterality'] == laterality and result['exam'] == 'vacc':
            yield int(result.get('denominator', -1) or -1)  # handle None/''


def vacc_numbercorrect_le(text):
    return max(vacc_numbercorrect(text, Laterality.OS), default=None)


def vacc_numbercorrect_re(text):
    return max(vacc_numbercorrect(text, Laterality.OD), default=None)
