"""
Lookup note by document id.
"""

import csv
import json
import pathlib
import re

import click

from eye_extractor.nlp.character_groups import LINE_START_CHARS_RX
from eye_extractor.tools.laterality_explorer import write_laterality_html
from eye_extractor.tools.search_jsonl import JsonlSearcher


class CorpusLookup:

    def __init__(self, *paths):
        self.paths = list(paths)

    def lookup(self, docid):
        text = None
        sect = None
        meta = None
        for path in self.paths:
            try:
                with open(path / f'{docid}.txt', encoding='utf8') as fh:
                    text = fh.read()
                with open(path / f'{docid}.meta', encoding='utf8') as fh:
                    meta = json.load(fh)
                with open(path / f'{docid}.sect', encoding='utf8') as fh:
                    sect = json.load(fh)
            except Exception as e:
                continue
            if text is not None:
                break
        return text, meta, sect


class ResultLookup:

    def __init__(self, path):
        self.data = self._load_csv(path)

    def _load_csv(self, path):
        res = {}
        with open(path, encoding='utf8', newline='') as fh:
            for row in csv.DictReader(fh):
                res[row['docid']] = row
        return res

    def get(self, docid):
        return self.data.get(docid, list())


class ReportBuilder:

    def __init__(self, *corpus_paths, intermediate_path=None, result_path=None):
        self.intermed_lookup = JsonlSearcher(intermediate_path)
        self.corpus_lookup = CorpusLookup(*corpus_paths)
        self.result_lookup = ResultLookup(result_path)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.intermed_lookup.close()

    def lookup(self, docid):
        with open(f'{docid}.html', 'w', encoding='utf8') as out:
            out.write('<html><body>\n')
            out.write(f'<h1>{docid}</h1>\n')

            out.write(f'<h2 id="intermediate">Intermediate</h2>')
            res = self.intermed_lookup.lookup(docid)
            out.write('<ul>\n')
            if res:
                for k, v in json.loads(res).items():
                    out.write(f'<li><b>{k}</b>: {v}</li>')
            out.write('</ul>\n')

            out.write(f'<h2 id="raw">Source Text</h2>')
            text, meta, sect = self.corpus_lookup.lookup(docid)
            out.write(f'<h3 id="text">Text</h3>\n')
            if text:
                write_laterality_html(out, text)
                # for line in re.split(LINE_START_CHARS_RX, text):
                #     out.write(f'<p>{line}</p>\n')
            out.write(f'<h3 id="meta">Metadata</h3>\n')
            if meta:
                out.write('<ul>\n')
                for k, v in meta.items():
                    out.write(f'<li><b>{k}</b>: {v}</li>')
                out.write('</ul>\n')
            out.write(f'<h3 id="sect">Section Info</h3>\n')
            if sect:
                out.write('<ul>\n')
                for k, v in meta.items():
                    out.write(f'<li><b>{k}</b>: {v}</li>')
                out.write('</ul>\n')

            out.write(f'<h2 id="result">Results</h2>')
            res = self.result_lookup.get(docid) or dict()
            out.write('<ul>\n')
            if res:
                print(res)
                for k, v in res.items():
                    out.write(f'<li><b>{k}</b>: {v}</li>')
            out.write('</ul>\n')
            out.write('</body></html>')


@click.command()
@click.argument('corpus_paths', nargs=-1, type=click.Path(exists=True, file_okay=False, path_type=pathlib.Path))
@click.option('--intermediate-path', type=click.Path(exists=True, file_okay=False, path_type=pathlib.Path))
@click.option('--result-path', type=click.Path(exists=True, dir_okay=False, path_type=pathlib.Path))
def main(corpus_paths, intermediate_path=None, result_path=None):
    docid = None
    with ReportBuilder(*corpus_paths, intermediate_path=intermediate_path, result_path=result_path) as rb:
        while True:
            if docid is not None:
                try:
                    rb.lookup(docid)
                except Exception as e:
                    print(f'Failed: {e}')
            print('Type `q` or `exit` to quit.')
            docid = input('docid>> ').strip().lower()
            if docid in {'q', 'exit', 'quit'}:
                break


if __name__ == '__main__':
    main()
