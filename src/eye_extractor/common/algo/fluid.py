import enum
import re

from eye_extractor.amd.utils import run_on_macula
from eye_extractor.nlp.negate.negation import is_negated, is_post_negated
from eye_extractor.laterality import create_new_variable
from eye_extractor.sections.oct_macula import find_oct_macula_sections, remove_macula_oct


class Fluid(enum.IntEnum):
    UNKNOWN = -1
    NO = 0
    FLUID = 1
    SUBRETINAL_FLUID = 11  # 1
    NO_SUBRETINAL_FLUID = 10
    INTRARETINAL_FLUID = 21
    NO_INTRARETINAL_FLUID = 20
    SUB_AND_INTRARETINAL_FLUID = 31
    NO_SUB_AND_INTRARETINAL_FLUID = 30


def rename_fluid(var: Fluid):
    match var:
        case Fluid.SUBRETINAL_FLUID:
            return 2
        case Fluid.INTRARETINAL_FLUID:
            return 3
        case Fluid.SUB_AND_INTRARETINAL_FLUID:
            return 4
        case Fluid.FLUID:
            return 5
        case Fluid.NO | Fluid.NO_INTRARETINAL_FLUID | Fluid.NO_SUBRETINAL_FLUID:
            return 0
        case _:
            return -1


def rename_intraretfluid(var: Fluid):
    match var:
        case Fluid.INTRARETINAL_FLUID | Fluid.SUB_AND_INTRARETINAL_FLUID:
            return 1
        case Fluid.NO_INTRARETINAL_FLUID | Fluid.NO_SUB_AND_INTRARETINAL_FLUID:
            return 0
        case _:
            return -1


def rename_subretfluid(var: Fluid):
    match var:
        case Fluid.SUBRETINAL_FLUID | Fluid.SUB_AND_INTRARETINAL_FLUID:
            return 1
        case Fluid.NO_SUBRETINAL_FLUID | Fluid.NO_SUB_AND_INTRARETINAL_FLUID:
            return 0
        case _:
            return -1


def fluid_prioritization(new_value: Fluid, curr_value: Fluid | None):
    """
    Defines how to reconcile/harmonise multiple fluid values in same note and laterality.
    """
    if curr_value is None:  # may start as None, so accept the new value
        return new_value
    elif curr_value == new_value:  # if both are the same, no need for further processing
        return curr_value
    elif {curr_value, new_value} == {Fluid.SUBRETINAL_FLUID, Fluid.INTRARETINAL_FLUID}:
        # merge subret and intraret
        return Fluid.SUB_AND_INTRARETINAL_FLUID
    elif curr_value == Fluid.SUB_AND_INTRARETINAL_FLUID and new_value in {
        Fluid.SUBRETINAL_FLUID, Fluid.INTRARETINAL_FLUID, Fluid.SUB_AND_INTRARETINAL_FLUID,
    }:
        # keep merged if any existing sub-item is being added
        return curr_value
    elif {curr_value, new_value} == {Fluid.NO_SUBRETINAL_FLUID, Fluid.NO_INTRARETINAL_FLUID}:
        # merge no subret and no intraret
        return Fluid.NO_SUB_AND_INTRARETINAL_FLUID
    elif curr_value == Fluid.NO_SUB_AND_INTRARETINAL_FLUID and new_value in {
        Fluid.NO_SUBRETINAL_FLUID, Fluid.NO_INTRARETINAL_FLUID, Fluid.NO_SUB_AND_INTRARETINAL_FLUID,
    }:
        # keep merged if any existing sub-item is being added
        return curr_value
    elif curr_value.value in {0, 10, 20, 30, -1} and new_value in {1, 11, 21, 31}:
        # group negatives/positives
        # -1=Unknown fluid is the lowest of the 'no' so it will override negatives in next line
        return new_value
    elif new_value.value > curr_value.value:
        # take the highest positive or negative in the group (this is the most specific)
        return new_value
    return curr_value  # default to current value


srf = r'sr\s*h?f(?:luids?)?'
irf = r'ir\s*f(?:luids?)?'

MACULAR_EDEMA_PAT = re.compile(
    rf'\b(?:'
    rf'mac(ular?)?\s*edema'
    rf'|csme'
    rf'|cme'
    rf'|scme'  # popular typo
    rf')\b',
    re.IGNORECASE
)

FLUID_NOS_PAT = re.compile(
    rf'\b(?:'
    rf'fluid'
    rf'|edema'
    rf')\b',
    re.IGNORECASE
)

SUBRETINAL_FLUID_PAT = re.compile(
    rf'(?:'
    rf'sub\W?ret\w*\W*fluid'
    rf'|\b{srf}\b'
    rf')',
    re.IGNORECASE
)

INTRARETINAL_FLUID_PAT = re.compile(
    rf'(?:'
    rf'intra\W?ret\w*\W*fluid'
    rf'|\b{irf}\b'
    rf')',
    re.IGNORECASE
)

SUB_AND_INTRARETINAL_FLUID_PAT = re.compile(
    rf'(?:'
    rf'sub(\W?ret\w*)?(?:\W*fluid)?\W*(?:\w+\W+){{0,2}}intra\W?ret\w*\W*fluid'
    rf'|{srf}\W+(?:and\W+)?{irf}'
    rf'|{irf}\W+(?:and\W+)?{srf}'
    rf')',
    re.IGNORECASE
)


def extract_fluid(text, *, headers=None, lateralities=None):
    data = []
    # prioritize OCT results
    data += _extract_fluid_from_oct(text)
    data += run_on_macula(
        macula_func=_get_fluid_in_macula,
        default_func=_get_fluid_in_macula,  # for testing
        text=remove_macula_oct(text),
        headers=headers,
        lateralities=lateralities,
        all_func=_get_fluid,
    )
    return data


non_macular = {'corneal', 'stromal'}


def _extract_fluid_from_oct(text):
    result = []
    for section_dict in find_oct_macula_sections(text):
        for lat, values in section_dict.items():
            result += _get_fluid_in_macula(values['text'], None, 'OCT MACULA',
                                           known_laterality=lat, known_date=values['date'], priority=2)
    return result


# TODO: Add documentation for this function.
def _get_fluid(text, lateralities, source, *, known_laterality=None, known_date=None, priority=0):
    data = []
    for label, pat, positive_value, negative_value, positive_word in [
        ('MACULAR_EDEMA', MACULAR_EDEMA_PAT, Fluid.INTRARETINAL_FLUID, Fluid.NO_INTRARETINAL_FLUID, 'macular edema'),
        ('SUBRETINAL_FLUID_PAT', SUBRETINAL_FLUID_PAT,
         Fluid.SUBRETINAL_FLUID, Fluid.NO_SUBRETINAL_FLUID, 'subretinal fluid'
         ),
        ('INTRARETINAL_FLUID_PAT', INTRARETINAL_FLUID_PAT,
         Fluid.INTRARETINAL_FLUID, Fluid.NO_INTRARETINAL_FLUID, 'intraretinal fluid'
         ),
        ('SUB_AND_INTRARETINAL_FLUID_PAT', SUB_AND_INTRARETINAL_FLUID_PAT,
         Fluid.SUB_AND_INTRARETINAL_FLUID, Fluid.NO_SUB_AND_INTRARETINAL_FLUID, 'sub and intraretinal fluid'
         ),
    ]:
        for m in pat.finditer(text):
            if is_negated(m, text, non_macular):  # non-macular
                continue
            negword = (
                    is_negated(m, text, word_window=4)
                    or is_post_negated(m, text, {'not', 'resolved'}, word_window=4)
            )
            data.append(
                create_new_variable(text, m, lateralities, 'fluid', {
                    'value': negative_value if negword else positive_value,
                    'term': m.group(),
                    'label': 'no' if negword else positive_word,
                    'negated': negword,
                    'regex': label,
                    'priority': priority,
                    'source': source,
                    'date': known_date,
                }, known_laterality=known_laterality)
            )

    return data


def _get_fluid_in_macula(text, lateralities, source, *,
                         known_laterality=None, priority=1, known_date=None):
    data = []
    for m in FLUID_NOS_PAT.finditer(text):  # in MACULA section, this is IRF
        if is_negated(m, text, non_macular):
            continue
        negword = (
                is_negated(m, text, word_window=4)
                or is_post_negated(m, text, {'not', 'resolved'}, word_window=4)
        )
        if is_negated(m, text, {'subretinal', 'sr', 'sub'}):  # is sub retinal
            value = Fluid.NO_SUBRETINAL_FLUID if negword else Fluid.SUBRETINAL_FLUID
        else:
            value = Fluid.NO_INTRARETINAL_FLUID if negword else Fluid.INTRARETINAL_FLUID
        data.append(
            create_new_variable(text, m, lateralities, 'fluid', {
                'value': value,
                'term': m.group(),
                'label': 'no' if negword else 'yes',
                'negated': negword,
                'regex': 'FLUID_NOS_PAT',
                'source': source,
                'priority': priority,
                'date': known_date,
            }, known_laterality=known_laterality)
        )
    # What is the point of calling `_get_fluid`? It introduces redundancy / duplicated code.
    # TODO: Remove `_get_fluid`, a general fluid search, out of function that searches the macula specifically.
    data += _get_fluid(text, lateralities, source, priority=priority,
                       known_date=known_date, known_laterality=known_laterality)
    return data
