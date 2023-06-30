"""
For debugging, run a given function on text to see if it works/fails.
"""
import json
from pathlib import Path

import click
from eye_extractor.sections.history import get_history_sections_to_be_removed, remove_history_sections, \
    retrieve_history_sections, get_problem_list_for_json

from eye_extractor.history.perhx import create_personal_history

from eye_extractor.clickargs import files_arg, outdir_opt
from eye_extractor.corpusio import read_file
from eye_extractor.history.famhx import create_family_history
from eye_extractor.utils import get_dt

FUNCTIONS = {  # must accept 2 args: text, sections
    'famhx': create_family_history,
    'perhx': create_personal_history,
    'hxtext': lambda x, y: get_history_sections_to_be_removed(x),
    'hxsects': lambda x, y: list(retrieve_history_sections(x)),
    'removehx': lambda x, y: remove_history_sections(x),
    'problist': lambda x, y: get_problem_list_for_json(x),
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
        _, text, metadata, sections = read_file(file, file.parent)
        for function in functions:
            result = FUNCTIONS[function](text, sections)
            with open(outdir / f'{file.stem}_{get_dt()}.{function}.json', 'w') as fh:
                json.dump(result, fh, indent=2, default=str)


if __name__ == '__main__':
    run_function_on_file()
