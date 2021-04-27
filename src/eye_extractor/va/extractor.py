import math
import re
from collections import Counter
from functools import lru_cache

from loguru import logger

from eye_extractor.laterality import Laterality
from eye_extractor.nlp.tokenizer import tokenize


class VAExtractor:
    PATTERN = re.compile(
        r'(\s|^|~|:)(?P<numerator>20|3E|E)/\s*(?P<score>\d+)\s*(?P<sign>[+|-])*\s*(?P<diopter>\d)*'
        r'|(?P<test>HM|CF|LP|NLP)(\W+(@|at|x)*\s*((\d+)(\s*\'|\s*"|\s*in|\s*ft|\s*feet)*|face)*'
        r'|$)'
    )
    SNELLEN_LEVELS = [10, 15, 20, 25, 30, 40, 50, 60, 70, 80, 100, 125, 150, 200, 250, 300, 400, 600, 800]
    LATERALITY = {'OD': Laterality.OD,
                  'RE': Laterality.OD,
                  'RIGHT': Laterality.OD,
                  'R': Laterality.OD,
                  'L': Laterality.OS,
                  'OS': Laterality.OS,
                  'LE': Laterality.OS,
                  'LEFT': Laterality.OS,
                  'BOTH': Laterality.OU,
                  'BE': Laterality.OU,
                  'OU': Laterality.OU,
                  'BILATERAL': Laterality.OU
                  }

    def __init__(self):
        self.snellen_levels = {x: -math.log(20.0 / x) / math.log(10.0) for x in self.SNELLEN_LEVELS}
        self.visual_acuities = {}

    @lru_cache
    def _get_snellen(self, x):
        return -math.log(20.0 / x) / math.log(10.0)

    def add_visual_acuity(self, lat, match, line, confidence):
        # add results
        if lat == Laterality.OU:
            self.visual_acuities[Laterality.OD].append((match, line, confidence))
            self.visual_acuities[Laterality.OS].append((match, line, confidence))
        else:
            self.visual_acuities[lat].append((match, line, confidence))

    def extract(self, text):
        lines = text.split('\n')
        matches = {i: [m for m in self.PATTERN.finditer(line)] for i, line in enumerate(lines)}
        tokens = {i: tokenize(line) for i, line in enumerate(lines)}
        # retain only laterality terms
        laterality_terms = {i: [
            (self.LATERALITY[tok], s, e) for tok, s, e in tokens[i] if tok in self.LATERALITY.keys()
        ] for i in tokens}
        max_term = Counter(lat for line in laterality_terms.values() for lat, _, _ in line if lat != Laterality.OU
                           ).most_common(n=1)
        self.visual_acuities = {Laterality.OD: [], Laterality.OS: []}
        i = 0
        while i < len(lines):
            for m in matches[i]:
                # found va
                if not m.group('score'):
                    logger.warning(f'Failed to parse score: {m.group()}: {m.groupdict()}')
                    continue
                va_score = int(m.group('score'))
                if va_score < 5:
                    logger.warning(f'Invalid score in: {m.group()}: {m.groupdict()}')
                    continue

                # find laterality
                if laterality_terms[i]:
                    lat = self._find_laterality(m.start(), m.end(), laterality_terms[i], text)
                    self.add_visual_acuity(lat, m, i, 5)
                elif lat := self._find_laterality_prior_lines(
                        [laterality_terms[j] for j in range(i - 3, i) if j in laterality_terms]
                ):
                    self.add_visual_acuity(lat, m, i, 5)
                elif len(matches) > i + 1 and self._find_laterality_next(matches[i + 1]):
                    # treat each row as list of lateralities
                    [self.add_visual_acuity(Laterality.OD, m, i, 0) for m in matches[i]]
                    [self.add_visual_acuity(Laterality.OS, m, i + 1, 0) for m in matches[i + 1]]
                    i += 1  # skip next line
                    break  # no more matches in line
                elif m2 := self._find_laterality_next(matches[i][1:]):
                    self.add_visual_acuity(Laterality.OD, m, i, 0)
                    self.add_visual_acuity(Laterality.OS, m2, i, 0)
                    break  # no more matches current line
                elif max_term:
                    self.add_visual_acuity(max_term[0][0], m, i, 0)
                else:
                    logger.warning(f'Failed to find laterality: {m.group()}: {m.groupdict()}')
            i += 1

        od_match, od_lva = self.get_best_result(Laterality.OD)
        os_match, os_lva = self.get_best_result(Laterality.OS)
        return {
            'RE': od_match.groupdict() if od_match else None,
            'RElogmar': format(od_lva, '.15g') if od_lva else None,
            'LE': os_match.groupdict() if os_match else None,
            'LElogmar': format(os_lva, '.15g') if os_lva else None,
        }

    def logmar(self, match):
        d = match.groupdict()
        if d['numerator'] == '20':
            score = int(d['score'])
            manual = self._get_snellen(score)
            if score not in self.snellen_levels:  # HACK: skip adjustments, otherwise process fails
                return manual
            if d['sign'] == '+':
                denom = self.snellen_levels[self.SNELLEN_LEVELS[self.SNELLEN_LEVELS.index(score) - 1]]
                manual = (int(d['diopter'] or 1) * (denom - manual) / 5.0) + manual
            elif d['sign'] == '-':
                denom = self.snellen_levels[self.SNELLEN_LEVELS[self.SNELLEN_LEVELS.index(score) + 1]]
                manual = (int(d['diopter'] or 1) * (denom - manual) / 5.0) + manual
            return manual
        elif d['numerator'] in {'3E', '3', 'E'}:
            return math.log(3.0 / d['score']) / math.log(10.0)
        elif d['exam'] == 'CF':
            return 2.0
        elif d['exam'] == 'HM':
            return 2.4
        elif d['exam'] == 'LP':
            return 2.7
        elif d['exam'] == 'NLP':
            return 3.0
        return None
    
    def get_best_result(self, lat: Laterality):
        min_priority = 0
        best_lva = None
        best_match = None
        for m, line, priority in self.visual_acuities[lat]:
            if priority < min_priority:
                continue
            lva = self.logmar(m)
            if lva and (not best_lva or lva < best_lva):
                best_lva = lva
                min_priority = priority
                best_match = m
        return best_match, best_lva

    def _find_laterality(self, start_idx, end_idx, laterality_terms, text):
        """Get laterality with lowest score/distance"""
        answers = []  # laterality, score, distance
        pat_10pt = re.compile('[!?.]', re.I)
        pat_5pt = re.compile('(,|and)', re.I)
        for lat, start, end in laterality_terms:
            if start > end_idx:
                target = text[end_idx: start]
                distance = start - end_idx
            else:
                target = text[end: start_idx]
                distance = start_idx - end
            score10 = len(pat_10pt.findall(target)) * 10
            score5 = len(pat_5pt.findall(target)) * 5
            # TODO: why are we keeping all??
            answers.append((lat, score10 + score5, distance))
        return sorted(answers, key=lambda x: (-x[1], -x[2]))[0][0]

    def _find_laterality_prior_lines(self, laterality_lines):
        for line in laterality_lines:
            for lat, start, end in line:
                if lat != Laterality.OU:
                    return lat

    def _find_laterality_next(self, matches_line):
        if not matches_line:
            return False
        for m in matches_line:
            if m.group('score'):
                return m
