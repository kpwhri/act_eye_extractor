from datetime import datetime

_CURR_DT = None

def get_dt(prev=True):
    """

    :param prev: use the previously-specified datetime (if available)
    :return:
    """
    global _CURR_DT
    if _CURR_DT is None or not prev:
        _CURR_DT = datetime.now().strftime('%Y%m%d_%H%M%S')
    return _CURR_DT
