from eye_extractor.common.section import run_on_section, SectFunc


def run_on_macula(macula_func: SectFunc, default_func: SectFunc, text: str,
                  *, headers=None, lateralities=None, all_func: SectFunc = None):
    section_funcs = {
        ('MACULA', 'ARMD', 'MAC', 'AMD', 'ASSESSMENT'): macula_func,
    }
    if all_func is not None:
        section_funcs['ALL'] = all_func
    return run_on_section(
        section_funcs=section_funcs,
        default_func=default_func,
        text=text,
        headers=headers,
        lateralities=lateralities
    )
