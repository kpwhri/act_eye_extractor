"""
For debugging, run a given function on text to see if it works/fails.
"""
import json
from pathlib import Path

import click

from eye_extractor.clickargs import files_arg, outdir_opt
from eye_extractor.corpusio import read_file
from eye_extractor.history.famhx import create_family_history
from eye_extractor.utils import get_dt

FUNCTIONS = {  # must accept 3 args: text, metadata, sections
    'famhx': create_family_history,
}


@click.command()
@files_arg
@outdir_opt
@click.option('--function', 'functions', multiple=True, type=click.Choice(FUNCTIONS),
              help=f'Specify functions to test. Available: {", ".join(FUNCTIONS)}.')
def run_function_on_file(files: tuple[Path], outdir: Path, functions: tuple[str]):
    if outdir is None:
        outdir = Path('.')
    for file in files:
        _, text, data, sections = read_file(file, file.parent)
        for function in functions:
            result = FUNCTIONS[function](text, data, sections)
            with open(outdir / f'{file.stem}_{get_dt()}.{function}.json', 'w') as fh:
                json.dump(result, fh, indent=2)


if __name__ == '__main__':
    run_function_on_file()
