"""
Build table from jsonl output.
"""
import csv
import datetime
import pathlib

import click
from loguru import logger

from eye_extractor.builders.build_history import build_history
from eye_extractor.clickargs import table_output_opts
from eye_extractor.common.json import loads_json
from eye_extractor.laterality import Laterality
from eye_extractor.output.amd import build_amd_variables
from eye_extractor.output.cataract import build_cataract_variables
from eye_extractor.output.cataract_surgery import build_cataract_surgery_variables
from eye_extractor.output.columns import OUTPUT_COLUMNS
from eye_extractor.output.dr import build_dr_variables
from eye_extractor.output.exam import build_exam
from eye_extractor.output.glaucoma import build_glaucoma
from eye_extractor.output.iop import build_iop
from eye_extractor.output.ro import build_ro_variables
from eye_extractor.output.shared import build_shared_variables
from eye_extractor.output.uveitis import build_uveitis_variables
from eye_extractor.output.va import build_va, get_manifest
from eye_extractor.output.validators import validate_columns_in_row


def process_data(data, *, add_columns=None, date_column='note_date'):
    result = {
        'docid': data['note_id'],
        'studyid': data.get('studyid', None),
        'date': data[date_column],
        'encid': data.get('enc_id', None),
        'is_training': data.get('train', None),
    }
    data['date'] = datetime.datetime.strptime(data[date_column], '%Y-%m-%d %H:%M:%S')
    data['note']['date'] = data['date'].date()
    data['note']['default_lat'] = Laterality(data['note']['default_lat'])
    for col in add_columns or []:
        result[col] = data[col]

    result.update(build_shared_variables(data))
    result.update(build_va(data['va']))
    result.update(build_iop(data['iop']))
    result.update(get_manifest(data['manifestrx']))
    result.update(build_amd_variables(data))
    result.update(build_glaucoma(data))
    result.update(build_uveitis_variables(data))
    result.update(build_ro_variables(data))
    result.update(build_cataract_variables(data))
    result.update(build_cataract_surgery_variables(data))
    result.update(build_history(data['history']))
    result.update(build_exam(data))
    result.update(build_dr_variables(data))
    return result


@click.command()
@click.argument('jsonl_file', type=click.Path(exists=True, path_type=pathlib.Path))
@table_output_opts(True)
def _build_table(jsonl_file: pathlib.Path, outdir: pathlib.Path, date_column='note_date', add_columns=None):
    build_table(jsonl_file, outdir, date_column, add_columns)


def build_table(jsonl_file: pathlib.Path, outdir: pathlib.Path, date_column='note_date', add_columns=None):
    """

    :param date_column: name of date column to use (defaults to 'note_date')
    :param add_columns:
    :param jsonl_file: if file, read that file; if directory, run all
    :param outdir:
    :return:
    """
    start_time = datetime.datetime.now()
    outdir.mkdir(parents=True, exist_ok=True)
    logger.add(outdir / f'build_table_{start_time:%Y%m%d_%H%M%S}.log', level='INFO')
    outpath = outdir / f'variables_{jsonl_file.stem}_{start_time:%Y%m%d_%H%M%S}.csv'
    for col in add_columns or []:
        OUTPUT_COLUMNS[col] = []
    if jsonl_file.is_dir():
        jsonl_files = jsonl_file.glob('*.jsonl')
    else:
        jsonl_files = [jsonl_file]
    with open(outpath, 'w', encoding='utf8', newline='') as out:
        for i, jsonl_file in enumerate(jsonl_files):
            with open(jsonl_file, encoding='utf8') as fh:
                writer = csv.DictWriter(out, fieldnames=OUTPUT_COLUMNS.keys())
                if i == 0:
                    writer.writeheader()
                for line in fh:
                    data = loads_json(line.strip())
                    result = process_data(data, add_columns=add_columns, date_column=date_column)
                    validate_columns_in_row(OUTPUT_COLUMNS, result, id_col='studyid')
                    writer.writerow(result)
    duration = datetime.datetime.now() - start_time
    logger.info(f'Total run time: {duration}')


if __name__ == '__main__':
    _build_table()
