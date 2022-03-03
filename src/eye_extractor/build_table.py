"""
Build table from jsonl output.
"""
import csv
import datetime
import json
import pathlib

import click
from loguru import logger

from eye_extractor.output.amd import build_amd_variables
from eye_extractor.output.columns import OUTPUT_COLUMNS
from eye_extractor.output.laterality import laterality_from_int, laterality_iter
from eye_extractor.output.uveitis import build_uveitis_variables
from eye_extractor.output.validators import validate_columns_in_row


def parse_va_exam(row, prev_denom, results):
    exam = row['exam']
    denom = row['denominator']
    num_correct = row['correct']
    text = row.get('text', '')
    laterality = laterality_from_int(row['laterality'])
    if not denom:
        return
    for lat in laterality_iter(laterality):
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


def get_va(data):
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


def process_data(data):
    result = {
        'docid': data['ft_id'],
        'studyid': data['studyid'],
        'date': data['event_date'],
        'encid': data['enc_id']
    }
    result.update(get_va(data['va']))
    result.update(get_manifest(data['manifestrx']))
    result.update(build_amd_variables(data))
    result.update(build_uveitis_variables(data))
    return result


@click.command()
@click.argument('jsonl_file', type=click.Path(exists=True, path_type=pathlib.Path))
@click.argument('outdir', type=click.Path(file_okay=False, path_type=pathlib.Path))
def build_table(jsonl_file: pathlib.Path, outdir: pathlib.Path):
    """

    :param jsonl_file: if file, read that file; if directory, get most recent jsonl file
    :param outdir:
    :return:
    """
    now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    outdir.mkdir(parents=True, exist_ok=True)
    outpath = outdir / f'variables_{now}.csv'
    if jsonl_file.is_dir():
        list_of_paths = jsonl_file.glob('*.jsonl')
        jsonl_file = max(list_of_paths, key=lambda p: p.stat().st_ctime)
    with (
            open(jsonl_file, encoding='utf8') as fh,
            open(outpath, 'w', encoding='utf8', newline='') as out,
    ):
        writer = csv.DictWriter(out, fieldnames=OUTPUT_COLUMNS.keys())
        writer.writeheader()
        for line in fh:
            data = json.loads(line.strip())
            result = process_data(data)
            validate_columns_in_row(OUTPUT_COLUMNS, result, id_col='studyid')
            writer.writerow(result)


if __name__ == '__main__':
    build_table()
