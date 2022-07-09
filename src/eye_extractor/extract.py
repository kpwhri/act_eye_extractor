import datetime
import json
import pathlib

import click
from loguru import logger

from eye_extractor.amd.algorithm import extract_amd_variables
from eye_extractor.cataract.algorithm import extract_cataract
from eye_extractor.cataract.cataract_surgery import get_cataract_surgery
from eye_extractor.exam.algorithm import get_exam
from eye_extractor.headers import extract_headers_and_text
from eye_extractor.history.famhx import create_family_history
from eye_extractor.history.perhx import create_personal_history
from eye_extractor.iop import get_iop
from eye_extractor.laterality import build_laterality_table
from eye_extractor.ro.algorithm import extract_ro_variables
from eye_extractor.uveitis.uveitis import get_uveitis
from eye_extractor.va.extractor2 import extract_va
from eye_extractor.va.rx import get_manifest_rx


def extract_all(text: str, data: dict = None):
    headers = extract_headers_and_text(text)
    lateralities = build_laterality_table(text)
    if data is None:
        data = {}
    data['va'] = list(extract_va(text))
    data['iop'] = list(get_iop(text))
    data['amd'] = extract_amd_variables(text, headers=headers, lateralities=lateralities)
    data['cataractsurg'] = get_cataract_surgery(text)
    data['cataract'] = extract_cataract(text, headers=headers, lateralities=lateralities)
    data['manifestrx'] = list(get_manifest_rx(text))
    data['ro'] = extract_ro_variables(text, headers=headers, lateralities=lateralities)
    data['uveitis'] = get_uveitis(text, headers=headers, lateralities=lateralities)
    data['history'] = {
        'family': create_family_history(text, headers=headers, lateralities=lateralities),
        'personal': create_personal_history(text, headers=headers, lateralities=lateralities),
    }
    data['exam'] = get_exam(text, headers=headers, lateralities=lateralities)
    return data


@click.command()
@click.argument('directories', nargs=-1, type=click.Path(exists=True, file_okay=False, path_type=pathlib.Path))
@click.option('--outdir', type=click.Path(file_okay=False, path_type=pathlib.Path), default=None)
@click.option('--filelist', type=click.Path(dir_okay=False, path_type=pathlib.Path), default=None)
def extract_variables(directories: tuple[pathlib.Path], outdir: pathlib.Path = None, filelist: pathlib.Path = None):
    """
    Iterate through all '*.txt' files in directory for processing by eye extractor.
        Optionally, will include relevant metadata from associated *.meta json files
    :return:
    """
    if outdir is None:
        outdir = pathlib.Path('out')
    outdir.mkdir(parents=True, exist_ok=True)
    now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    with open(outdir / f'eye_extractor_{now}.jsonl', 'w', encoding='utf8') as out:
        if filelist is not None:
            for line in extract_variables_from_filelist(filelist):
                out.write(json.dumps(line, default=str) + '\n')
        else:
            for line in extract_variables_from_directories(*directories):
                out.write(json.dumps(line, default=str) + '\n')


def extract_variable_from_file(file, directory):
    with open(file, encoding='utf8') as fh:
        text = fh.read()
    metadata = directory / f'{file.stem}.meta'
    if metadata.exists():
        with open(metadata, encoding='utf8') as fh:
            data = json.load(fh)
    else:
        data = {'filename': str(file)}
    data = extract_all(text, data)
    return data


def extract_variables_from_filelist(filelist):
    with open(filelist) as fh:
        for i, line in enumerate(fh, start=1):
            file = pathlib.Path(line.strip())
            yield extract_variable_from_file(file, file.parent)
            if i % 10000 == 0:
                logger.info(f'Processed {i} records.')


def extract_variables_from_directories(*directories: pathlib.Path):
    for directory in directories:
        logger.info(f'Reading Directory: {directory}')
        for i, file in enumerate(directory.glob('*.txt'), start=1):
            yield extract_variable_from_file(file, directory)
            if i % 10000 == 0:
                logger.info(f'Processed {i} records.')


if __name__ == '__main__':
    extract_variables()
