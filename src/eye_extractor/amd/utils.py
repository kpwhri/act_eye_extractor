from eye_extractor.common.section import run_on_section, SectFunc
from eye_extractor.sections.document import Document, TextView
from eye_extractor.sections.patterns import PatternGroup


def run_on_macula(macula_func: SectFunc, default_func: SectFunc, doc: Document, all_func: SectFunc = None, *,
                  textview=TextView.NO_HX):
    section_funcs = {
        PatternGroup.MACULA_ASSESSMENT_PLAN: macula_func,
    }
    if all_func is not None:
        section_funcs['ALL'] = all_func
    return run_on_section(
        section_funcs=section_funcs,
        default_func=default_func,
        doc=doc,
        textview=textview,
    )
