import re


def get_standardized_name(term):
    return re.sub(r'[^A-Za-z]+', ' ', term).lower()


def build_regex_from_dict(d):
    """

    :param d: drug to enum
    :return:
    """
    return re.compile('|'.join(d.keys()).replace(' ', r'\W*'), re.I)
