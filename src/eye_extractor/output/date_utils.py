import datetime


def parse_date_or_none(data, column, *, dtformat='%Y-%m-%d'):
    val = data.get(column, None)
    if isinstance(val, str):
        val = val.split(' ')[0]
        return datetime.datetime.strptime(val, dtformat)
    return val
