"""
Search a corpus for patterns (e.g., related to a particular sections, etc.).

Keep track of text that did not have the pattern matched.

"""
import datetime
import pathlib

import click
from loguru import logger

from eye_extractor.corpusio import read_from_params
from eye_extractor.sections.history import retrieve_history_sections
from eye_extractor.sections.oct_macula import find_oct_macula_sections


def _prep_text(text):
    return text.replace('\n', r'\n').replace('\t', r'\t')


@click.command()
@click.argument('directories', nargs=-1, type=click.Path(exists=True, file_okay=False, path_type=pathlib.Path))
@click.option('--outdir', type=click.Path(file_okay=False, path_type=pathlib.Path), default=None)
@click.option('--filelist', type=click.Path(dir_okay=False, path_type=pathlib.Path), default=None)
@click.option('--pattern', 'patterns', multiple=True)
def find_patterns_in_corpus(
        directories: tuple[pathlib.Path], outdir: pathlib.Path = None,
        filelist: pathlib.Path = None, patterns: list[str] = None,
):
    if not patterns:
        raise ValueError(r'No patterns selected for review.')
    if outdir is None:
        outdir = pathlib.Path('out')
    outdir.mkdir(parents=True, exist_ok=True)
    start_time = datetime.datetime.now()
    with (open(outdir / f'patterns_{start_time:%Y%m%d_%H%M%S}.txt', 'w', encoding='utf8') as out,
          open(outdir / f'patterns_missing_{start_time:%Y%m%d_%H%M%S}.txt', 'w', encoding='utf8') as miss):
        for file, text, data, sections in read_from_params(*directories, filelist):
            if 'HISTORY' in patterns:
                _sections = retrieve_history_sections(text)
                if not _sections:
                    miss.write(f'{file.name}\tHISTORY\t{file}\n')
                for section in _sections:
                    out.write(f'{file.name}\tHISTORY\t{_prep_text(section["name"])}\t{_prep_text(section["text"])}\n')
            if 'OCT' in patterns:
                _sections = find_oct_macula_sections(text)
                if not _sections:
                    miss.write(f'{file.name}\tOCT\t{file}\n')
                for mac_sections in _sections:
                    for lat, values in mac_sections.items():
                        out.write(f'{file.name}\tOCT\t{lat.name}\t{_prep_text(values["text"])}\n')
    duration = datetime.datetime.now() - start_time
    logger.info(f'Total run time: {duration}')


if __name__ == '__main__':
    find_patterns_in_corpus()
