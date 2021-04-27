"""
Find and Use Past Ocular History
"""
import re
from collections import namedtuple

from eye_extractor.headers import add_laterality_to_variable
from eye_extractor.laterality import LATERALITY_PATTERN, LATERALITY, Laterality
from eye_extractor.patterns import PATTERN_BATTERY, PATTERN_RESPONSE

SECTION_PATTERN = re.compile(
    '(PAST OCULAR HISTORY(?: OF)?|PATIENT HISTORY|SOCIAL HISTORY|PATIENT HAS A HISTORY OF'
    '|PATIENT HX|PERSONAL EYE HISTORY|HISTORY OF PRESENT ILLNESS|ASSESSMENT COMMENTS'
    '|IMPRESSION|PEHX|ASSESSMENT'
    '|FAMILY HISTORY(?: OF)?|FAMILY HX|FAMILY EYE HISTORY'
    '|VISUAL ACUITY|ENTRANCE EXAM|TESTING|PROBLEM LIST|EYE MEDICATIONS'
    '|OLD RX|OBJECTIVE EXAM|COMMENTS):?',
    re.I
)

Item = namedtuple('Item', 'label term start end is_label')


def get_value_from_item(item: Item, term: str, section: str):
    if item.label in ('yes', 'no'):
        return {
            'value': 1 if item.label == 'yes' else 0,
            'label': item.label,
            'term': term,
            'section': section,
        }
    return {
        'laterality': item.label,
        'term': term,
        'section': section,
        'value': 1,
    }


def add_pair_to_data(term1: Item, term2: Item, section):
    if term1.is_label:
        return {term1.label: get_value_from_item(term2, term1.term, section)}
    else:
        return {term2.label: get_value_from_item(term1, term2.term, section)}


def extract_from_sections(text):
    data = {}
    section_data = parse_sections(text)
    for row in section_data['PERSONAL']:
        if val := row.get('amd', None):
            if lat := val.get('laterality', None):
                add_laterality_to_variable(data, lat, 'amd', val)
            elif val['value'] == 0:
                add_laterality_to_variable(data, Laterality.OU, 'amd', val)
    return data


def parse_sections(text):
    data = {'PERSONAL': [], 'FAMILY': []}
    for line in text.split('\n\n'):
        sections = iter(SECTION_PATTERN.split(line)[1:])
        for section_label, section_text in zip(sections, sections):
            if section_label.upper() in {
                'PAST OCULAR HISTORY', 'PAST OCULAR HISTORY OF',
                'PATIENT HISTORY', 'SOCIAL HISTORY',
                'PATIENT HAS A HISTORY OF', 'PATIENT HX',
                'PERSONAL EYE HISTORY', 'ASSESSMENT', 'ASSESSMENT COMMENTS',
                'HISTORY OF PRESENT ILLNESS', 'PEHX', 'IMPRESSION',
            }:
                curr = 'PERSONAL'
            elif section_label.upper() in {
                'FAMILY HISTORY', 'FAMILY HISTORY OF', 'FAMILY HX',
                'FAMILY EYE HISTORY',
            }:
                curr = 'FAMILY'
            else:
                continue
            for section in re.split(r'[\W]\d+[).-]', section_text):
                terms = []
                for label, pattern in PATTERN_BATTERY:
                    for m2 in pattern.finditer(section):
                        terms.append(Item(label, m2.group(), m2.start(), m2.end(), True))
                for label, pattern in PATTERN_RESPONSE:
                    for m2 in pattern.finditer(section):
                        terms.append(Item(label, m2.group(), m2.start(), m2.end(), False))
                for m2 in LATERALITY_PATTERN.finditer(section):
                    terms.append(Item(LATERALITY[m2.group().upper()], m2.group(), m2.start(), m2.end(), False))
                terms = sorted(terms, key=lambda x: x[2])  # sort by start index
                if len(terms) == 1:  # handle where only one element
                    term = terms[0]
                    if term.is_label:
                        data[curr].append({term.label: {'value': 1, 'term': term.term, 'label': None}})
                    continue
                i = 0
                did_next = False
                while i < len(terms):
                    term = terms[i]
                    next_term = terms[i + 1] if i + 1 < len(terms) else None
                    prev_term = terms[i - 1] if i > 0 and not did_next else None
                    if not term.is_label:
                        did_next = False
                        i += 1
                    if next_term and section[term.end:next_term.start].strip() in {':', '-'}:
                        data[curr].append(add_pair_to_data(term, next_term, section_label))
                        did_next = True
                        i += 2
                    elif prev_term and section[prev_term.end:term.start].strip() in {':', '-', ''}:
                        data[curr].append(add_pair_to_data(prev_term, term, section_label))
                        did_next = True
                        i += 2
                    elif next_term and not next_term.is_label and section[term.end:next_term.start].strip() in {',',
                                                                                                                ''}:
                        data[curr].append(add_pair_to_data(term, next_term, section_label))
                        did_next = True
                        i += 2
                    elif next_term and next_term.is_label:
                        data[curr].append({term.label: {'value': 1, 'term': term.term, 'label': None}})
                        did_next = False
                        i += 1
                    elif not prev_term and next_term:
                        data[curr].append(add_pair_to_data(term, next_term, section_label))
                        did_next = True
                        i += 2
                    else:
                        did_next = False
                        print(term, next_term)
                        i += 1
    return data
