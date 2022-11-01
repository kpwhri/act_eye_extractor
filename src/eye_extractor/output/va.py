from eye_extractor.output.laterality import laterality_from_int, laterality_iter

from loguru import logger

etdrs_lookup = {
    'vacc': 'wc',
    'vasc': 'nc',
    'vaph': 'ph',
}


def parse_va_exam(row, prev_denom, results):
    exam = row['exam']
    denom = row['denominator']
    num_correct = row['correct']
    text = row.get('text', '')
    is_etdrs = row.get('format') == 'etdrs'
    laterality = laterality_from_int(row['laterality'])
    if not denom:
        return
    for lat in laterality_iter(laterality):
        if is_etdrs:
            continue  # TODO: not sure how to capture: too few examples
            variable = f'etdrs_{etdrs_lookup[exam]}_{lat}'
            num_correct = int(num_correct)
            results[variable] = num_correct
        else:  # snellen
            # denominator
            variable = f'{exam}_denominator_{lat}'
            if isinstance(denom, int):
                pass
            elif denom.upper() in {'NI', 'NO IMPROVEMENT'}:
                if lat in prev_denom:
                    denom = prev_denom[lat][0]
                    num_correct = prev_denom[lat][1]
                else:
                    logger.warning(f'Did not find previous score for "ni" in "{text}".')
                    continue
            elif denom.upper() in {'NT', 'NA'}:  # not taken
                continue
            # get the max result
            denom = int(denom)
            if denom > results.get(variable, -1):
                if denom > 401:
                    logger.info(f'Denominator too high: "{denom}" in {text}.')
                results[variable] = denom
            else:
                continue

            # number correct
            variable = f'{exam}_numbercorrect_{lat}'
            num_correct = int(num_correct)
            prev_denom[lat] = (denom, num_correct, True)
            results[variable] = num_correct
            if -6 <= num_correct <= 6:
                pass
            else:
                logger.info(f'Invalid number correct "{num_correct}" in {text}.')


def parse_va_test(row, prev_denom, results, *, no_improvement=False):
    """
    Parse visual acuity exam.
    :param no_improvement: specify that no improvement so won't look for test/distanace in 'row'
    :param row:
    :param prev_denom:
    :param results:
    :return:
    """
    exam = row['exam']
    test = row.get('test', None)  # None if no improvement
    distance = row.get('distance', None)  # None if no improvement
    try:
        distance = int(distance)
    except Exception as e:
        logger.info(f'Distance {distance} cannot be converted to int in {row.get("text", "")}.')
    laterality = laterality_from_int(row['laterality'])
    for lat in laterality_iter(laterality_from_int(laterality)):
        if no_improvement:
            test, distance, *_ = prev_denom[lat]
        variable = f'{exam}_letters_{lat}'
        results[variable] = test.upper()
        variable = f'{exam}_distance_{lat}'
        results[variable] = distance
        prev_denom[lat] = (test.upper(), distance, False)


def build_va(data):
    results = {}
    prev_denom = {}
    for row in data:
        if row.get('denominator', None) and row['denominator'].upper() in {'NI', 'NO IMPROVEMENT'}:
            lat = laterality_iter(laterality_from_int(row['laterality']))[0]
            if lat not in prev_denom:
                logger.warning(f'Missing laterality {lat} in {row["text"]}.')
            elif prev_denom[lat][-1] is True:
                parse_va_exam(row, prev_denom, results)
            else:
                parse_va_test(row, prev_denom, results, no_improvement=True)
        elif 'test' in row:
            parse_va_test(row, prev_denom, results)
        elif 'denominator' in row:
            parse_va_exam(row, prev_denom, results)
        else:
            logger.warning(f'Unrecognized visual acuity: {row}')
    return results


def get_manifest(data):
    if data:
        return data[0]
    return {}
