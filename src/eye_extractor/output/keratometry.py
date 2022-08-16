def build_keratometry(data):
    """
    Current algorithm: just take the first measurement that appears
    :param data:
    :return:
    """
    results = {
        'keratometry_flatcurve_re': -1,
        'keratometry_flatcurve_le': -1,
        'keratometry_steepcurve_re': -1,
        'keratometry_steepcurve_le': -1,
        'keratometry_flataxis_re': -1,
        'keratometry_flataxis_le': -1,
        'keratometry_steepaxis_re': -1,
        'keratometry_steepaxis_le': -1,
        'ax_length_re': -1,
        'ax_length_le': -1,
    }
    outvars = list(results.keys())
    for datum in data:
        for key, result in datum.items():
            for var in outvars:
                if results[var] == -1 and result.get(var, None):
                    results[var] = result[var]
    return results
