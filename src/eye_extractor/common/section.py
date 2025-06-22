from typing import Callable

from eye_extractor.sections.document import Document, TextView

# section function: text, lateralities, source -> data
SectFunc = Callable[[str, dict, str], list]


def _run_on_section(func, name, text, lat):
    return func(text, lat, name)


def run_on_section(section_funcs: dict[str, SectFunc], default_func: SectFunc, doc: Document, *,
                   textview=TextView.NO_HX):
    data = []
    if doc.sections:
        for section_names, section_func in section_funcs.items():
            if section_names == 'ALL':
                data += _run_on_section(section_func, 'ALL', doc.get_text(view=textview),
                                        doc.get_lateralities(view=textview))
            else:
                if not isinstance(section_names, tuple):
                    section_names = (section_names,)
                for section in doc.iter_sections(*section_names):
                    data += _run_on_section(section_func, section.name, section.text, section.lateralities)
    else:  # this is often just used for testing
        data += default_func(doc.get_text(view=textview), doc.get_lateralities(view=textview), 'ALL')
    return data
