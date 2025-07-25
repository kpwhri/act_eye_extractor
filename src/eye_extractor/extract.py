"""
Primary entry point for extracting eye-related variables from a corpus of notes.

The `extract` function will take text notes as input (supplied by filelists, directories, etc.)
    and write NLP-extracted information to a jsonlines file.

Once completing this step, use the `build_table` to compile this information to a CSV file.
"""
import datetime
import json
import pathlib
import sys

import click
from loguru import logger

from eye_extractor.amd.algorithm import extract_amd_variables
from eye_extractor.cataract.algorithm import extract_cataract_variables
from eye_extractor.cataract.cataract_surgery import get_cataract_surgery
from eye_extractor.clickargs import outdir_opt
from eye_extractor.common.algo.extract import extract_common_algorithms
from eye_extractor.common.noteinfo import extract_note_level_info
from eye_extractor.corpusio import read_from_params
from eye_extractor.ro.algorithm import extract_ro_variables
from eye_extractor.sections.document import Document
from eye_extractor.dr.diabetic_retinopathy import extract_dr_variables
from eye_extractor.exam.algorithm import get_exam
from eye_extractor.glaucoma.algorithm import extract_glaucoma
from eye_extractor.history.famhx import create_family_history
from eye_extractor.history.perhx import create_personal_history
from eye_extractor.iop import get_iop
from eye_extractor.nlp.negate.boilerplate import remove_boilerplate
from eye_extractor.uveitis.algorithm import extract_uveitis
from eye_extractor.va.extractor2 import extract_va
from eye_extractor.va.rx import get_manifest_rx

ALGORITHMS = [
    'va',
    'iop',
    'amd',
    'cataractsurg',
    'cataract',
    'glaucoma',
    'ro',
    'uveitis',
    'history',
    'exam',
    'dr',
]


def extract_all(text: str, *, data: dict = None, sections: dict = None, targets: list[str] = None):
    """

    Args:
        text:
        data:
        sections:
        targets (list[str]): list of algorithms to run; defaults to None := all

    Returns:

    """
    doc = Document(text, newline_chars='¶')
    # TODO: for treatment-related, may need to look at non-boilerplate removed text
    # text = remove_boilerplate(text)
    if data is None:
        data = {}
    data['note'] = extract_note_level_info(doc)
    doc.lateralities.default_laterality = data['note']['default_lat']
    data['common'] = extract_common_algorithms(doc)

    # main algorithms
    if not targets:
        targets = ALGORITHMS
    if 'va' in targets:
        data['va'] = list(extract_va(doc.get_text()))
        data['manifestrx'] = list(get_manifest_rx(doc.get_text()))
    if 'iop' in targets:
        data['iop'] = list(get_iop(doc.get_text()))
    if 'amd' in targets:
        data['amd'] = extract_amd_variables(doc)
    if 'cataractsurg' in targets:
        data['cataractsurg'] = get_cataract_surgery(doc)
    if 'cataract' in targets:
        data['cataract'] = extract_cataract_variables(doc)
    if 'glaucoma' in targets:
        data['glaucoma'] = extract_glaucoma(doc)
    if 'ro' in targets:
        data['ro'] = extract_ro_variables(doc)
    if 'uveitis' in targets:
        data['uveitis'] = extract_uveitis(doc)
    if 'history' in targets:
        data['history'] = {
            'family': create_family_history(doc),
            'personal': create_personal_history(doc),
        }
    if 'exam' in targets:
        data['exam'] = get_exam(doc)
    if 'dr' in targets:
        data['dr'] = extract_dr_variables(doc)

    return data


@click.command()
@click.argument('directories', nargs=-1, type=click.Path(exists=True, file_okay=False, path_type=pathlib.Path))
@outdir_opt
@click.option('--filelist', type=click.Path(dir_okay=False, path_type=pathlib.Path), default=None)
@click.option('--search-missing-headers', is_flag=True, default=False,
              help='If a requested header is not found, attempt to find it in the text.')
@click.option('--targets', multiple=True, default=None,
              help='Target algorithms to run')
def _extract_variables(directories: tuple[pathlib.Path], outdir: pathlib.Path = None, filelist: pathlib.Path = None,
                       *, search_missing_headers=False, targets=None):
    extract_variables(directories, outdir, filelist, search_missing_headers=search_missing_headers, targets=targets)


def extract_variables(directories: tuple[pathlib.Path] = None, outdir: pathlib.Path = None,
                      filelist: pathlib.Path = None,
                      *,
                      search_missing_headers=False,
                      targets=None):
    """
    Iterate through all '*.txt' files in directory for processing by eye extractor.
        Optionally, will include relevant metadata from associated *.meta json files
    :return:
    """
    if outdir is None:
        outdir = pathlib.Path('out')
    outdir.mkdir(parents=True, exist_ok=True)
    start_time = datetime.datetime.now()
    logger.remove()
    logger.add(outdir / f'eye_extractor_{start_time:%Y%m%d_%H%M%S}.log', level='DEBUG')
    logger.add(sys.stderr, level='INFO')
    outfile = outdir / f'eye_extractor_{start_time:%Y%m%d_%H%M%S}.jsonl'
    with open(outfile, 'w', encoding='utf8') as out:
        for file, text, data, sections in read_from_params(*directories or tuple(), filelist=filelist,
                                                           search_missing_headers=search_missing_headers):
            line = extract_variable_from_text(text, data, sections, targets)
            out.write(json.dumps(line, default=str) + '\n')
    duration = datetime.datetime.now() - start_time
    logger.info(f'Total run time: {duration}')
    return outfile


def extract_variable_from_text(text, data, sections, targets):
    """extract eye info from text, data, and section info"""
    data = extract_all(text, data=data, sections=sections, targets=targets)
    return data


if __name__ == '__main__':
    _extract_variables()
