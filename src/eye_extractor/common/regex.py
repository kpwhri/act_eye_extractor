def coalesce_match(m, *groups):
    """Take first matching pattern from groups"""
    d = m.groupdict()
    for group in groups:
        if value := d.get(group, None):
            return value
    return None
