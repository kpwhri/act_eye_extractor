import datetime


def parse_date_or_none(data, column, *, dtformat='%Y-%m-%d'):
    val = data.get(column, None)
    if val:
        return datetime.datetime.strptime(val, dtformat)
    return val
