"""
Build table from jsonl output.
"""
import csv
import datetime
import json
import pathlib

import click
from loguru import logger

from eye_extractor.laterality import Laterality
from eye_extractor.output.columns import OUTPUT_COLUMNS
from eye_extractor.output.validators import validate_columns_in_row


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
            results[variable] = denom
        else:
            continue

        # number correct
        variable = f'{exam}_numbercorrect_{lat}'
        num_correct = int(num_correct)
        prev_denom[lat] = (denom, num_correct)
        results[variable] = num_correct


def parse_va_test(row, prev_denom, results):
    """
    Parse visual acuity exam.
    :param row:
    :param prev_denom:
    :param results:
    :return:
    """
    exam = row['exam']
    test = row['test']
    distance = row['distance']
    try:
        distance = int(distance)
    except Exception as e:
        logger.info(f'Distance {distance} cannot be converted to int in {row.get("text", "")}.')
    laterality = laterality_from_int(row['laterality'])
    for lat in laterality_iter(laterality_from_int(laterality)):
        variable = f'{exam}_letters_{lat}'
        results[variable] = test.upper()
        variable = f'{exam}_distance_{lat}'
        results[variable] = distance


def get_va(data):
    results = {}
    prev_denom = {}
    for row in data:
        if 'denominator' in row:
            parse_va_exam(row, prev_denom, results)
        elif 'test' in row:
            parse_va_test(row, prev_denom, results)
        else:
            logger.warning(f'Unrecognized visual acuity: {row}')
    return results


def process_data(data):
    result = {
        'docid': data['ft_id'],
        'studyid': data['studyid'],
        'date': data['event_date'],
        'encid': data['enc_id']
    }
    result.update(get_va(data['va']))
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
            open(outpath, 'w', encoding='utf8') as out,
    ):
        writer = csv.DictWriter(out, fieldnames=OUTPUT_COLUMNS.keys())
        for line in fh:
            data = json.loads(line.strip())
            result = process_data(data)
            validate_columns_in_row(OUTPUT_COLUMNS, result, id_col='studyid')
            writer.writerow(result)


if __name__ == '__main__':
    build_table()
