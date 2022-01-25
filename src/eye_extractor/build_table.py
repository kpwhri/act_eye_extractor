"""
Build table from jsonl output.
"""
import csv
import datetime
import json
import pathlib

import click

OUTPUT_COLUMNS = []


def process_data(data):
    result = {}
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
        print(jsonl_file)
    with (
            open(jsonl_file, encoding='utf8') as fh,
            open(outpath, 'w', encoding='utf8') as out,
    ):
        writer = csv.DictWriter(out, fieldnames=OUTPUT_COLUMNS)
        for line in fh:
            data = json.loads(line.strip())
            result = process_data(data)
            writer.writerow(result)


if __name__ == '__main__':
    build_table()
