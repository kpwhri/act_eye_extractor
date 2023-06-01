import datetime

from loguru import logger


def parse_date_or_none(data, column, *, dtformat='%Y-%m-%d'):
    val = data.get(column, None)
    if isinstance(val, str):
        val = val.split(' ')[0]
        # TODO: Investigate why line 12 causes an error.
        try:
            return datetime.datetime.strptime(val, dtformat)
        except ValueError as e:
            logger.warning(f"Error while parsing datetime str: {val} - Error: {e}")
    return val
