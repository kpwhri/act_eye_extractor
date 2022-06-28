from eye_extractor.output.variable import column_from_variable, column_from_variable_binary


def build_dr_variables(data):
    curr = data['dr']
    results = {}
    results.update(build_dr(curr))
    results.update(build_ret_micro(curr))
    return results


def build_dr(data):
    return column_from_variable_binary(data, 'diab_retinop_yesno')


def build_ret_micro(data):
    return column_from_variable_binary(data, 'ret_microaneurysm')


def build_cotton_wspot(data):
    return column_from_variable_binary(data, 'cottonwspot')


def build_hard_exudates(data):
    return column_from_variable_binary(data, 'hardexudates')


# Categorical variable
# def build_ven_beading(data):
#     return column_from_variable(
#         {
#             f'venbeading_re': -1,
#             f'venbeading_le': -1,
#         },
#         data,
#         transformer_func=lambda n: n['severity'],
#         filter_func=lambda n: n['value'] in {ctype.value for ctype in cataracttypes},
#         convert_func=lambda n: f'cataract_type_{n[-2:]}',
#     )

def build_disc_edema(data):
    return column_from_variable_binary(data, 'disc_edema_DR')


def build_hemorrhage(data):
    return column_from_variable_binary(data, 'hemorrhage_dr')


# def build_hemorrhage_type(data):
#     return column_from_variable({
#             f'venbeading_re': -1,
#             f'venbeading_le': -1,
#         },
#         data)


# def build_irma(data):
#     return column_from_variable({
#             f'venbeading_re': -1,
#             f'venbeading_le': -1,
#         },
#         data)


# def build_fuild(data):
#     return column_from_variable({
#             f'venbeading_re': -1,
#             f'venbeading_le': -1,
#         },
#         data)


def build_laser_scars(data):
    return column_from_variable_binary(data, 'dr_laser_scars')


# def build_laser_scar_type(data):
#     return column_from_variable({
#             f'venbeading_re': -1,
#             f'venbeading_le': -1,
#         },
#         data)


def build_laser_panrentinal(data):
    return column_from_variable_binary(data, 'laserpanret_photocoag')


def build_neovasc(data):
    return column_from_variable_binary(data, 'neovasc_yesno')


def build_nva(data):
    return column_from_variable_binary(data, 'nva_yesno')
