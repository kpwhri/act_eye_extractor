from typing import Callable

from eye_extractor.laterality import build_laterality_table

# section function: text, lateralities, source -> data
SectFunc = Callable[[str, dict, str], list]


def run_on_section(section_funcs: dict[str, SectFunc], default_func: SectFunc, text: str,
                   *, headers=None, lateralities=None):
    data = []
    if headers:
        for section_name, section_func in section_funcs.items():
            if section_text := (
                    text if section_name == 'ALL' else
                    headers.get(section_name, None)
            ):
                lateralities = build_laterality_table(section_text)
                data += section_func(section_text, lateralities, section_name)
    else:  # this is often just used for testing
        if not lateralities:
            lateralities = build_laterality_table(text)
        data += default_func(text, lateralities, 'ALL')
    return data
