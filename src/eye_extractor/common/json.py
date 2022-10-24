import datetime
import json


def load_json(fh):
    """Date safe load json"""
    pass


def dump_json():
    """Date safe dump json"""
    pass


def dumps_json(data):
    return json.dumps(data, default=str)


def loads_json(data):
    return json.loads(data, object_hook=load_date_hook)


def dumps_and_loads_json(data):
    return loads_json(dumps_json(data))


def load_date_hook(d):
    if 'date' in d:
        try:
            d['date'] = datetime.datetime.strptime(d['date'].split(' ')[0], '%Y-%m-%d').date()
        except:
            pass
    return d


def dump_date_hook(obj):
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return '%Y-%m-%d'
    raise TypeError(f'Type {type(obj)} is not serializable.')
