import re

from loguru import logger

history_pat = r'(?:hx|history)'

POSSIBLE_END_HX_PAT = re.compile(
    r'(?:===|:)',
    re.I
)

NEGATIVE_FOR_PAT = re.compile(
    r'(?:negative\W*for)\W*'
    r'(?P<target>(?:[\w-]+\W){1,3})'
)


def find_end(text, start_pos):
    for m in POSSIBLE_END_HX_PAT.finditer(text, pos=start_pos):
        if m.group() == '===':
            return m.start()
        elif m.group() == ':':
            curr_text = text[m.start():].strip()
            if curr_text.startswith(('yes', 'no')):
                continue
            else:
                return m.start()


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
    if not found:
        logger.warning(f'Unidentified history category: {key} ({value})')


def create_history(text, start_pats):
    data = {}
    for start_pat in start_pats:
        for m in start_pat.finditer(text):
            start = m.end()
            end = find_end(text, start)
            curr_text = text[start:end]
            yes_no_list = [x.strip() for x in re.split(r'\b(yes|no)\b', curr_text.strip()) if x.strip()]
            if len(yes_no_list) > 1:
                it = iter(yes_no_list)
                for key, val in zip(it, it):
                    if key in {'yes', 'no'}:
                        key, val = val, key
                    update_hx_data(data, key, 1 if val == 'yes' else 0)
            else:
                # update with all keywords
                update_hx_data(data, curr_text, value=1, exclusive_search=False)
                # then negate those which have a negation keyword preceding them
                for m2 in NEGATIVE_FOR_PAT.finditer(curr_text):
                    update_hx_data(data, m2.group('target'), 0, exclusive_search=False)
    return data
