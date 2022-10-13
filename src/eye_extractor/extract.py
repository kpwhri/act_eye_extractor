import datetime
import json
import pathlib

import click
from loguru import logger

from eye_extractor.amd.algorithm import extract_amd_variables
from eye_extractor.cataract.algorithm import extract_cataract
from eye_extractor.cataract.cataract_surgery import get_cataract_surgery
from eye_extractor.common.noteinfo import extract_note_level_info
from eye_extractor.dr.diabetic_retinopathy import extract_dr_variables
from eye_extractor.common.algo.extract import extract_common_algorithms
from eye_extractor.exam.algorithm import get_exam
from eye_extractor.glaucoma.algorithm import extract_glaucoma
from eye_extractor.headers import extract_headers_and_text, Headers
from eye_extractor.history.famhx import create_family_history
from eye_extractor.history.perhx import create_personal_history
from eye_extractor.iop import get_iop
from eye_extractor.laterality import build_laterality_table
from eye_extractor.ro.algorithm import extract_ro_variables
from eye_extractor.uveitis.uveitis import get_uveitis
from eye_extractor.va.extractor2 import extract_va
from eye_extractor.va.rx import get_manifest_rx


def extract_all(text: str, *, data: dict = None, sections: dict = None):
    if not sections:
        sections = extract_headers_and_text(text)
    lateralities = build_laterality_table(text)
    if data is None:
        data = {}
    data['note'] = extract_note_level_info(text, headers=sections, lateralities=lateralities)
    lateralities.default_laterality = data['note']['default_lat']
    data['va'] = list(extract_va(text))
    data['iop'] = list(get_iop(text))
    data['amd'] = extract_amd_variables(text, headers=sections, lateralities=lateralities)
    data['cataractsurg'] = get_cataract_surgery(text)
    data['cataract'] = extract_cataract(text, headers=sections, lateralities=lateralities)
    data['glaucoma'] = extract_glaucoma(text, headers=sections, lateralities=lateralities)
    data['manifestrx'] = list(get_manifest_rx(text))
    data['ro'] = extract_ro_variables(text, headers=sections, lateralities=lateralities)
    data['uveitis'] = get_uveitis(text, headers=sections, lateralities=lateralities)
    data['history'] = {
        'family': create_family_history(text, headers=sections, lateralities=lateralities),
        'personal': create_personal_history(text, headers=sections, lateralities=lateralities),
    }
    data['exam'] = get_exam(text, headers=sections, lateralities=lateralities)
    data['dr'] = extract_dr_variables(text, headers=sections, lateralities=lateralities)
    data['common'] = extract_common_algorithms(text, headers=sections, lateralities=lateralities)

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


def _read_json_file(path, *, encoding='utf8'):
    if path.exists():
        with open(path, encoding=encoding) as fh:
            return json.load(fh)


def extract_variable_from_file(file, directory):
    with open(file, encoding='utf8') as fh:
        text = fh.read()
    # read metadata file (if exists)
    if not (data := _read_json_file(directory / f'{file.stem}.meta')):
        data = {'filename': str(file)}
    # read section data file (if exists)
    if not (sections := Headers(_read_json_file(directory / f'{file.stem}.sect'))):
        sections = extract_headers_and_text(text)
    # extract eye info from file
    data = extract_all(text, data=data, sections=sections)
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
