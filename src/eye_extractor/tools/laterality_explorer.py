"""
Prints out visualisations of notes and the lateralities contained.
"""
import datetime
import pathlib

import click

from eye_extractor.laterality import build_laterality_table, Laterality
from eye_extractor.nlp.character_groups import LINE_START_CHARS

LAT_TO_COLOR = {
    Laterality.UNKNOWN: '',
    Laterality.OD: 'background: magenta;',
    Laterality.OS: 'background: cyan;',
    Laterality.OU: 'background: yellow;',
}


def get_file_text(docid, *corpus_paths):
    if docid is None:
        return
    if isinstance(docid, pathlib.Path):
        with open(docid, encoding='utf8') as fh:
            return fh.read()
    for path in corpus_paths:
        curr = path / f'{docid}.txt'
        if curr.exists():
            with open(curr, encoding='utf8') as fh:
                return fh.read()


def write_span(outfh, lat, text):
    outfh.write(f'\n<span style="{LAT_TO_COLOR[lat]}">{text}</span>')


def write_laterality_html(outfh, text):
    """Write laterality output for a given bit of text."""
    latloc = build_laterality_table(text)
    curr_lat = Laterality.UNKNOWN
    curr_idx = 0
    outfh.write('<p>')
    for i, letter in enumerate(text):
        new_lat = latloc.get_by_index(i, text)
        if letter in LINE_START_CHARS:
            if curr_lat is None:
                continue
            write_span(outfh, curr_lat, text[curr_idx:i])  # not including newline
            outfh.write('</p><p>')
            curr_idx = i + 1  # start from next character
            curr_lat = Laterality.UNKNOWN
            continue  # ignore if changed
        if curr_lat is None or new_lat == curr_lat:
            continue
        write_span(outfh, curr_lat, text[curr_idx:i])
        curr_idx = i
        curr_lat = new_lat
    write_span(outfh, curr_lat, text[curr_idx:])
    outfh.write('</p>')


def write_key(outfh, *, header_level=3):
    outfh.write(f'<h{header_level}>Laterality Color Key</h{header_level}>\n')
    outfh.write('<ul>\n')
    for lat, bgvalue in LAT_TO_COLOR.items():
        outfh.write(f'<li><span style="{bgvalue}">{lat.name}: {lat.value}</span></li>\n')
    outfh.write('</ul>\n')


def build_laterality_html_file_from_docid(docid, *corpus_paths, outpath=None):
    if not outpath:
        outpath = pathlib.Path('.') / '.laterality'
    outpath.mkdir(exist_ok=True)

    curr_dt = datetime.datetime.now()

    if text := get_file_text(docid, *corpus_paths):
        outfile = outpath / f'{docid.stem if isinstance(docid, pathlib.Path) else docid}.html'
        if outfile.exists():
            with open(outfile, encoding='utf8') as fh:
                prev = fh.read()
        else:
            prev = ''
        with open(outfile, 'w', encoding='utf8') as out:
            out.write(f'<h1>Run: {curr_dt}</h1>')
            write_key(out)
            write_laterality_html(out, text)
            out.write(prev)


def build_laterality_html_files(docids, *corpus_paths, outpath=None):
    if not outpath:
        outpath = pathlib.Path('.') / '.laterality'
    outpath.mkdir(exist_ok=True)
    for docid in docids:
        build_laterality_html_file_from_docid(docid, *corpus_paths, outpath=outpath)


@click.command()
@click.argument('corpus_paths', nargs=-1, type=click.Path(exists=True, file_okay=False, path_type=pathlib.Path))
@click.option('--docid', default=None, required=False, multiple=True)
@click.option('--outpath', type=click.Path(file_okay=False, path_type=pathlib.Path))
@click.option('--filelist', type=click.Path(exists=True, dir_okay=False, path_type=pathlib.Path))
def main(corpus_paths, docid=None, outpath=None, filelist=None):
    """
    Get laterality for requested docid.
    :return:
    """
    if not outpath:
        outpath = pathlib.Path('.') / '.laterality'
    outpath.mkdir(exist_ok=True)

    if filelist:
        with open(filelist) as fh:
            docids = [pathlib.Path(line.strip()) for line in fh]
        build_laterality_html_files(docids, *corpus_paths, outpath=outpath)
    elif docid:
        build_laterality_html_files(docid, *corpus_paths, outpath=outpath)
    else:
        while True:
            print('Type `q` or `exit` to quit.')
            docid = input('docid>> ').strip().lower()
            if docid in {'q', 'exit', 'quit'}:
                break
            build_laterality_html_file_from_docid(docid, *corpus_paths, outpath=outpath)


if __name__ == '__main__':
    main()
