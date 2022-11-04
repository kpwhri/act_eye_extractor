import re
import string

history_pat = r'(?:hx|history)'

POSSIBLE_END_HX_PAT = re.compile(
    r'(?:===|___|:)',
    re.I
)

NEGATIVE_FOR_PAT = re.compile(
    r'(?:negative\W*for)\W*'
    r'(?P<target>(?:[\w-]+\W){1,3})'
)

FAMILY_RELATIONS = [
    'brother', 'sister', 'mother', 'father', 'aunt', 'grandmother', 'grandma',
    'bro', 'sis', 'mom', 'mama', 'dad', 'papa', 'uncle', 'grandfather', 'grandpa',
]
FAMILY_RELATION_PAT = re.compile(rf'(?:{"|".join(FAMILY_RELATIONS)})', re.I)

CONDITION_WORDS = frozenset({
    'amd', 'armd', 'glaucoma', 'cataract', 'cataracts', 'retina', 'issues',
    'eye', 'pvd', 'trauma', 'amblyopia', 'surgery', 'dr', 'retinopathy',
    'diabetes', 'degeneration', 'type', 'onset',
})


def find_previous_letter(text, start_pos):
    for i in range(start_pos, 0, -1):
        if text[i] in string.ascii_letters:
            return i
    return 0


def find_word_start(text, start_pos):
    for i in range(start_pos, 0, -1):
        if text[i] not in string.ascii_letters:
            return i + 1
    return 0


def find_start_of_previous_word(text, start_pos):
    return find_word_start(text, find_previous_letter(text, start_pos))


def find_end(text, start_pos):
    text = text.lower()
    for m in POSSIBLE_END_HX_PAT.finditer(text, pos=start_pos):
        if m.group() == '===':
            return m.start()
        elif m.group() == ':':
            curr_text = text[m.end():].strip().strip('¶')
            prev_word = re.split(r'[\s/\-¶]+', text[start_pos: m.start()].strip())[-1]
            if curr_text.startswith(('yes', 'no')):
                continue
            elif prev_word in CONDITION_WORDS:
                continue
            else:
                return find_start_of_previous_word(text, m.start())


def update_history_from_key(data, pat, key, value, data_key):
    if re.search(pat, key, re.I):
        data[data_key] = 1 if value else 0
        return True
    return False


def update_hx_data(data, key, value=None, exclusive_search=True):
    """

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


def create_history(text, start_pats, is_personal_hx=False):
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
