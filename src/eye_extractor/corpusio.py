import json
import pathlib

from loguru import logger

from eye_extractor.headers import Headers, extract_headers_and_text


def _read_json_file(path, *, encoding='utf8'):
    if path.exists():
        with open(path, encoding=encoding) as fh:
            return json.load(fh)


def read_file(file, directory):
    with open(file, encoding='utf8') as fh:
        text = fh.read()
    # read metadata file (if exists)
    if not (data := _read_json_file(directory / f'{file.stem}.meta')):
        data = {'filename': str(file)}
    # read section data file (if exists)
    sections = Headers(_read_json_file(directory / f'{file.stem}.sect'), text=text)
    sections.add(extract_headers_and_text(text))
    return file, text, data, sections


def read_directories(*directories: pathlib.Path):
    for directory in directories:
        logger.info(f'Reading Directory: {directory}')
        for i, file in enumerate(directory.glob('*.txt'), start=1):
            yield read_file(file, directory)
            if i % 10000 == 0:
                logger.info(f'Processed {i} records.')


def read_filelist(filelist):
    with open(filelist) as fh:
        for i, line in enumerate(fh, start=1):
            file = pathlib.Path(line.strip())
            yield read_file(file, file.parent)
            if i % 10000 == 0:
                logger.info(f'Processed {i} records.')


def read_from_params(*directories, filelist=None):
    if filelist is not None:
        yield from read_filelist(filelist)
    else:
        yield from read_directories(*directories)
