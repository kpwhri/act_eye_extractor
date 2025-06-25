def safeget(data, *keys):
    curr = data
    for key in keys:
        curr = data.get(key, None)
        if not curr:
            return None
    return curr
