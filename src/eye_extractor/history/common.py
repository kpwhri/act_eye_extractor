"""
Shared functions related to finding and extracting information related to historical conditions,
    both personal history and family history.

Some of these (e.g., `find_end`) may have broader uses in locating the beginning of the next section.
"""
import re
import string

from eye_extractor.nlp.negate.other_subject import FAMILY_RELATION_PAT
from eye_extractor.sections.document import Document
from eye_extractor.sections.patterns import SectionName
from eye_extractor.sections.section_builder import Section

history_pat = r'(?:hx|history)'

POSSIBLE_END_HX_PAT = re.compile(
    r'(?:===|___|:)',
    re.I
)

NEGATIVE_FOR_PAT = re.compile(
    r'(?:negative\W*for)\W*'
    r'(?P<target>(?:[\w-]+\W){1,3})'
)

CONDITION_WORDS = frozenset({
    'amd', 'armd', 'glaucoma', 'cataract', 'cataracts', 'retina', 'issues',
    'eye', 'pvd', 'trauma', 'amblyopia', 'surgery', 'dr', 'retinopathy',
    'diabetes', 'degeneration', 'type', 'onset',
})


def find_previous_letter(text, start_pos):
    """Look backwards to identify the first letter in text from `start_pos`"""
    for i in range(start_pos, 0, -1):
        if text[i] in string.ascii_letters:
            return i
    return 0


def find_word_start(text, start_pos):
    """From a `start_pos` in a word, look backwards to identify the start index of a word"""
    for i in range(start_pos, 0, -1):
        if text[i] not in string.ascii_letters:
            return i + 1
    return 0


def find_start_of_previous_word(text, start_pos):
    """Find the index of the previous word's start"""
    return find_word_start(text, find_previous_letter(text, start_pos))


def find_end(text, start_pos):
    """
    Identify the end of a section, particular a historical section.
    These are challenging as they tend to contain 'subheaders' with yes/no answers.
    They also tend to have the same 'subheaders'.
    Here, we try to identify subheaders using the 'yes'/'no' values or a set of known
        subheaders.
    The index of the start of the next header is returned. If the next header has mulitple
        words, only the last term will be identified.
    Line endings, etc., are not considered

    :param text: text to search for the end of the current section
    :param start_pos:
    :return:
    """
    text = text.lower()  # will check membership in lowercase sets
    for m in POSSIBLE_END_HX_PAT.finditer(text, pos=start_pos):
        if m.group() == '===':
            return m.start()
        elif m.group() == ':':
            curr_text = text[m.end():].strip().strip('¶')
            prev_word = re.split(r'[\s/\-¶]+', text[start_pos: m.start()].strip())[-1]
            if curr_text.startswith(('yes', 'no')):
                continue  # is a subheader
            elif prev_word in CONDITION_WORDS:
                continue  # is a subheader
            else:  # found the next section
                return find_start_of_previous_word(text, m.start())
    return len(text)  # this is the last section


def update_history_from_key(data, pat, key, value, data_key):
    """Update history dict `data` with identified key"""
    if re.search(pat, key, re.I):
        data[data_key] = 1 if value else 0
        return True
    return False


def update_hx_data(data, key, value=None, exclusive_search=True):
    """
    Search the history section for particular patterns/keywords to identify historical conditions.

    :param data:
    :param key:
    :param value:
    :param exclusive_search: if True, return first value only
    :return:
    """
    found = False
    for data_key, pattern in [
        ('diabetes', 'diabete'),
        ('glaucoma', 'glaucoma'),
        ('migraine', 'migraine'),
        ('cataracts', 'cataract'),
        ('dr', 'diabetic retinopathy'),
        ('retinal_detachment', '(retinal detachment)'),
        ('amblyopia', '(amblyopia|strabismus|lazy eye)'),
        ('amd', r'(age\Wrelated|macular degenera|ar?md)'),
    ]:
        found_ = update_history_from_key(data, pattern, key, 1 if value else 0, data_key)
        found |= found_
        if found_ and exclusive_search:
            return


def create_history_from_doc(doc: Document, *section_names: SectionName, is_personal_hx=False):
    """
    Extract specific historical information and conditions from a history section.

    :param doc: document with history text to look in
    :param section_names: list of sections to search for
    :param is_personal_hx: personal history section if true, else family history
    :return:
    """

    data = {}
    for section in doc.iter_sections(*section_names):
        curr_text = section.text
        yes_no_list = [x.strip() for x in re.split(r'\b(yes|no(?:ne)?)\b', curr_text.strip()) if x.strip()]
        if len(yes_no_list) > 1:
            it = iter(yes_no_list)
            for key, val in zip(it, it):
                if key in {'yes', 'no', 'none'}:
                    key, val = val, key
                if is_personal_hx and FAMILY_RELATION_PAT.search(key):
                    continue
                update_hx_data(data, key, 1 if val == 'yes' else 0)
        else:
            # update with all keywords
            update_hx_data(data, curr_text, value=1, exclusive_search=False)
            # then negate those which have a negation keyword preceding them
            for m2 in NEGATIVE_FOR_PAT.finditer(curr_text):
                update_hx_data(data, m2.group('target'), 0, exclusive_search=False)
    return data


def create_history(text, start_pats, is_personal_hx=False):
    """
    Extract specific historical information and conditions from a history section.

    :param text: text to look in
    :param start_pats: history patterns (compiled)
    :param is_personal_hx: personal history section if true, else family history
    :return:
    """
    data = {}
    for start_pat in start_pats:
        for m in start_pat.finditer(text):
            start = m.end()
            end = find_end(text, start)
            curr_text = text[start:end]
            yes_no_list = [x.strip() for x in re.split(r'\b(yes|no(?:ne)?)\b', curr_text.strip()) if x.strip()]
            if len(yes_no_list) > 1:
                it = iter(yes_no_list)
                for key, val in zip(it, it):
                    if key in {'yes', 'no', 'none'}:
                        key, val = val, key
                    if is_personal_hx and FAMILY_RELATION_PAT.search(key):
                        continue
                    update_hx_data(data, key, 1 if val == 'yes' else 0)
            else:
                # update with all keywords
                update_hx_data(data, curr_text, value=1, exclusive_search=False)
                # then negate those which have a negation keyword preceding them
                for m2 in NEGATIVE_FOR_PAT.finditer(curr_text):
                    update_hx_data(data, m2.group('target'), 0, exclusive_search=False)
    return data
