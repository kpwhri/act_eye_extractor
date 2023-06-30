from pathlib import Path

import click

outdir_opt = click.option('--outdir', type=click.Path(exists=True, file_okay=False, path_type=Path), default=None,
                          help='Output directory; defaults to current directory.')
date_column_opt = click.option('--date-column', default='note_date')
add_column_opt = click.option('--add-column', 'add_columns', multiple=True,
                              help='Additional columns to include in output.')
outdir_arg = click.argument('outdir', type=click.Path(file_okay=False, path_type=Path))
files_arg = click.argument('files', nargs=-1, type=click.Path(exists=True, dir_okay=False, path_type=Path))


def table_output_opts(use_arg=False):
    def _table_output_opts(func):
        if use_arg:
            return outdir_arg(date_column_opt(add_column_opt(func)))
        else:
            return outdir_opt(date_column_opt(add_column_opt(func)))
    return _table_output_opts

