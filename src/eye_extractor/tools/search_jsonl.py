"""
Search jsonl files to retrieve intermediate representations for an document/note id.

On the first run, `search_jsonl.py` will build the appropriate indexes which will take some time.

Usage:
    python src/tools/search_jsonl.py /path/to/dir/with/jsonl/files/ docid
"""

import datetime
import json
import pathlib
import sqlite3

import click


def load_date_hook(d):
    if 'date' in d:
        try:
            d['date'] = datetime.datetime.strptime(d['date'].split(' ')[0], '%Y-%m-%d').date()
        except:
            pass
    return d


class JsonlSearcher:
    def __init__(self, path, build_new_index_files=False):
        self.path = path
        self.dest_path = self.path / '.index'
        self.idx_path = self.dest_path / 'jsonl.idx'
        self.conn = None
        self.kind = 1 if build_new_index_files else 0
        if self.dest_path.exists():
            self.reconnect()
        else:
            self.dest_path.mkdir()
            self.reconnect()
            self.populate()

    def __del__(self):
        if self.conn is not None:
            self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn is not None:
            self.conn.close()

    def reconnect(self):
        self.conn = sqlite3.connect(self.idx_path)
        self.cur.execute('create table if not exists LOOKUP (docid TEXT, jsonl_file TEXT, line_number INT, kind INT);')

    @property
    def cur(self):
        return self.conn.cursor()

    def populate(self):
        if self.kind == 1:
            self._populate_new_index_files()
        else:
            self._populate()
        self.conn.commit()

    def _insert(self, cur, docid, filestem, line, kind):
        cur.execute(
            f'insert into LOOKUP (docid, jsonl_file, line_number, kind)'
            f' values ("{docid}", "{filestem}.jsonl", {line}, {kind})'
        )

    def _populate(self):
        cur = self.cur
        kind = 0
        for file in self.path.glob('*.jsonl'):
            with open(file, encoding='utf8') as fh:
                for i, line in enumerate(fh):
                    data = json.loads(line, object_hook=load_date_hook)
                    docid = data['note_id']
                    self._insert(cur, docid, file.stem, i, kind)

    def _populate_new_index_files(self):
        cur = self.cur
        kind = 1
        count = 0
        curr_json_file = 0
        out = open(self.dest_path / f'{curr_json_file}.jsonl', 'w', encoding='utf8')
        for file in self.path.glob('*.jsonl'):
            with open(file, encoding='utf8') as fh:
                for i, line in enumerate(fh):
                    data = json.loads(line, object_hook=load_date_hook)
                    docid = data['note_id']
                    self._insert(cur, docid, curr_json_file, count, kind)
                    count += 1
                    out.write(line)
                    if count % 10000 == 0:
                        curr_json_file += 1
                        out = open(self.dest_path / f'{curr_json_file}.jsonl', 'w', encoding='utf8')

    # retrieve
    def lookup(self, docid):
        i = -1
        for i, (jsonl_file, line_num, kind) in enumerate(self.cur.execute(
                f'select jsonl_file, line_number, kind from LOOKUP where docid = "{docid}"'
        )):
            path = self.path if kind == 0 else self.dest_path
            with open(path / jsonl_file, encoding='utf8') as fh:
                for i, line in enumerate(fh):
                    if i != line_num:
                        continue
                    data = json.dumps(json.loads(line, object_hook=load_date_hook), default=str, indent=2)
                    with open(f'{docid}.json', 'w', encoding='utf8') as out:
                        out.write(data)
                    return data
        print(f'Processed {i+1} records with note id: {docid}.')


@click.command()
@click.argument('path', type=click.Path(file_okay=False, path_type=pathlib.Path))
@click.argument('docid')
def main(path, docid):
    """
    Identify json line related to `docid`.

    :param path: path to directory with jsonl files
    :param docid: docid to identify
    :return:
    """
    with JsonlSearcher(path) as searcher:
        print(searcher.lookup(docid))


if __name__ == '__main__':
    main()
