import json
import pathlib

from loguru import logger

from eye_extractor.sections.headers import Headers, extract_headers_and_text


def _read_json_file(path, *, encoding='utf8'):
    if path.exists():
        with open(path, encoding=encoding) as fh:
            return json.load(fh)


def read_file(file, directory, *, search_missing_headers=False):
    with open(file, encoding='utf8') as fh:
        text = fh.read()
    # read metadata file (if exists)
    if not (data := _read_json_file(directory / f'{file.stem}.meta')):
        data = {'filename': str(file)}
    # read section data file (if exists)
    sections = Headers(_read_json_file(directory / f'{file.stem}.sect'))
    sections.add(extract_headers_and_text(text))
    if search_missing_headers:
        sections.set_text(text)
    return file, text, data, sections


def read_directories(*directories: pathlib.Path, search_missing_headers=False):
    for directory in directories:
        if not directory:
            continue
        logger.info(f'Reading Directory: {directory}')
        for i, file in enumerate(directory.glob('*.txt'), start=1):
            yield read_file(file, directory, search_missing_headers=search_missing_headers)
            if i % 10000 == 0:
                logger.info(f'Processed {i:,} records.')


def read_filelist(filelist, search_missing_headers=False):
    with open(filelist) as fh:
        for i, line in enumerate(fh, start=1):
            file = pathlib.Path(line.strip())
            yield read_file(file, file.parent, search_missing_headers=search_missing_headers)
            if i % 10000 == 0:
                logger.info(f'Processed {i:,} records.')


def read_from_params(*directories, filelist=None, search_missing_headers=False):
    if filelist is not None:
        yield from read_filelist(filelist, search_missing_headers=search_missing_headers)
    else:
        yield from read_directories(*directories, search_missing_headers=search_missing_headers)
