"""
Script to extract and build only those files specified on the command line.
"""
import datetime
import json
from pathlib import Path

import click

from eye_extractor.build_table import process_data
from eye_extractor.clickargs import table_output_opts, files_arg
from eye_extractor.corpusio import read_file
from eye_extractor.extract import extract_variable_from_text
from eye_extractor.utils import get_dt


@click.command()
@files_arg
@table_output_opts(False)
def extract_and_build(files: tuple[Path], outdir=None, date_column='note_date', add_columns=None):
    """Run extract and build on a list of files"""
    if outdir is None:
        outdir = Path('.')
    for file in files:
        _, text, data, sections = read_file(file, file.parent)
        result = extract_variable_from_text(text, data, sections)
        with open(outdir / f'{file.stem}_{get_dt()}.extract.json', 'w') as fh:
            json.dump(result, fh, indent=2)
        result = process_data(result, add_columns=add_columns, date_column=date_column)
        with open(outdir / f'{file.stem}_{get_dt()}.build.json', 'w') as fh:
            json.dump(result, fh, indent=2)


if __name__ == '__main__':
    extract_and_build()
