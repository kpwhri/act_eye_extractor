def build_iop(data):
    result = {}
    result.update(iop_measurement(data))
    return result


def iop_measurement(data):
    if not data:
        return {}
    return {
        'iop_measurement_re': data[0].get('iop_measurement_re'),
        'iop_measurement_le': data[0].get('iop_measurement_le'),
        'iop_instrument_type': data[0].get('iop_instrument_type'),
    }
