import re
from typing import Pattern


def coalesce_match(m, *groups):
    """Take first matching pattern from groups"""
    d = m.groupdict()
    for group in groups:
        if value := d.get(group, None):
            return value
    return None


def expand_pattern(pat: Pattern, expansion: str, insert_index=None):
    pattern = pat.pattern.strip()
    if insert_index is None:
        insert_index = 0
        if pattern.endswith(r'\b'):
            insert_index -= 2  # '\' and 'b'
        if pattern.endswith(r')'):
            insert_index -= 1
        if insert_index == 0:
            insert_index = None
    return re.compile(pattern[:insert_index] + expansion + pattern[insert_index:], pat.flags)
