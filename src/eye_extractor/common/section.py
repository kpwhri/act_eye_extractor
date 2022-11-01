from typing import Callable

from eye_extractor.laterality import build_laterality_table

# section function: text, lateralities, source -> data
SectFunc = Callable[[str, dict, str], list]


def _run_on_section(func, name, text):
    return func(text, build_laterality_table(text), name)


def run_on_section(section_funcs: dict[str, SectFunc], default_func: SectFunc, text: str,
                   *, headers=None, lateralities=None):
    data = []
    if headers:
        for section_names, section_func in section_funcs.items():
            if section_names == 'ALL':
                data += _run_on_section(section_func, section_names, text)
            else:
                if not isinstance(section_names, tuple):
                    section_names = (section_names,)
                for section_name, section_text in headers.iterate(*section_names):
                    data += _run_on_section(section_func, section_name, section_text)
    else:  # this is often just used for testing
        data += default_func(text, lateralities or build_laterality_table(text), 'ALL')
    return data
