import enum
import re

from eye_extractor.amd.utils import run_on_macula
from eye_extractor.common.negation import is_negated, is_post_negated
from eye_extractor.laterality import create_new_variable


class FluidAMD(enum.IntEnum):
    UNKNOWN = -1
    NO = 0
    FLUID = 1
    SUBRETINAL_FLUID = 11  # 1
    NO_SUBRETINAL_FLUID = 10
    INTRARETINAL_FLUID = 21
    NO_INTRARETINAL_FLUID = 20
    SUB_AND_INTRARETINAL_FLUID = 31
    NO_SUB_AND_INTRARETINAL_FLUID = 30


def fluid_prioritization(new_value: FluidAMD, curr_value: FluidAMD | None):
    if curr_value is None:  # may start as None
        return new_value
    elif curr_value == new_value:
        return curr_value
    elif {curr_value, new_value} == {FluidAMD.SUBRETINAL_FLUID, FluidAMD.INTRARETINAL_FLUID}:
        return FluidAMD.SUB_AND_INTRARETINAL_FLUID
    elif {curr_value, new_value} == {FluidAMD.NO_SUBRETINAL_FLUID, FluidAMD.NO_INTRARETINAL_FLUID}:
        return FluidAMD.NO_SUB_AND_INTRARETINAL_FLUID
    elif curr_value.value in {0, 10, 20, 30, -1} and new_value in {1, 11, 21, 31}:
        # group negatives/positives
        # -1=Unknown fluid is the lowest of the 'no' so it will override negatives in next line
        return new_value
    elif new_value.value > curr_value.value:
        # take the highest positive or negative in the group (this is the most specific)
        return new_value
    return curr_value  # default to current value


srf = r'sr\s*f(?:luids?)?'
irf = r'ir\s*f(?:luids?)?'

FLUID_NOS_PAT = re.compile(
    rf'(?:'
    rf'fluid'
    rf')',
    re.IGNORECASE
)

SUBRETINAL_FLUID_PAT = re.compile(
    rf'(?:'
    rf'sub\W?retinal\W*fluid'
    rf'|\b{srf}\b'
    rf')',
    re.IGNORECASE
)

INTRARETINAL_FLUID_PAT = re.compile(
    rf'(?:'
    rf'intra\W?retinal\W*fluid'
    rf'|\b{irf}\b'
    rf')',
    re.IGNORECASE
)

SUB_AND_INTRARETINAL_FLUID_PAT = re.compile(
    rf'(?:'
    rf'sub(\W?retinal)?(?:\W*fluid)?\W*(?:\w+\W+){{0,2}}intra\W?retinal\W*fluid'
    rf'|{srf}\W+(?:and\W+)?{irf}'
    rf'|{irf}\W+(?:and\W+)?{srf}'
    rf')',
    re.IGNORECASE
)


def get_fluid(text, *, headers=None, lateralities=None):
    return run_on_macula(
        macula_func=_get_fluid_in_macula,
        default_func=_get_fluid_in_macula,  # for testing
        text=text,
        headers=headers,
        lateralities=lateralities,
        all_func=_get_fluid,
    )


def _get_fluid(text, lateralities, source):
    data = []
    for label, pat, positive_value, negative_value, positive_word in [
        ('SUBRETINAL_FLUID_PAT', SUBRETINAL_FLUID_PAT,
         FluidAMD.SUBRETINAL_FLUID, FluidAMD.NO_SUBRETINAL_FLUID, 'subretinal fluid'
         ),
        ('INTRARETINAL_FLUID_PAT', INTRARETINAL_FLUID_PAT,
         FluidAMD.INTRARETINAL_FLUID, FluidAMD.NO_INTRARETINAL_FLUID, 'intraretinal fluid'
         ),
        ('SUB_AND_INTRARETINAL_FLUID_PAT', SUB_AND_INTRARETINAL_FLUID_PAT,
         FluidAMD.SUB_AND_INTRARETINAL_FLUID, FluidAMD.NO_SUB_AND_INTRARETINAL_FLUID, 'sub and intraretinal fluid'
         ),
    ]:
        for m in pat.finditer(text):
            negword = (
                    is_negated(m, text, {'no', 'or', 'without'}, word_window=4)
                    or is_post_negated(m, text, {'not'}, word_window=3)
            )
            data.append(
                create_new_variable(text, m, lateralities, 'fluid_amd', {
                    'value': negative_value if negword else positive_value,
                    'term': m.group(),
                    'label': 'no' if negword else positive_word,
                    'negated': negword,
                    'regex': label,
                    'source': source,
                })
            )

    return data


def _get_fluid_in_macula(text, lateralities, source):
    data = []
    for m in FLUID_NOS_PAT.finditer(text):
        negword = (
                is_negated(m, text, {'no', 'or', 'without'}, word_window=4)
                or is_post_negated(m, text, {'not'}, word_window=3)
        )
        data.append(
            create_new_variable(text, m, lateralities, 'fluid_amd', {
                'value': FluidAMD.NO if negword else FluidAMD.FLUID,
                'term': m.group(),
                'label': 'no' if negword else 'yes',
                'negated': negword,
                'regex': 'FLUID_NOS_PAT',
                'source': source,
            })
        )
    data += _get_fluid(text, lateralities, source)
    return data
