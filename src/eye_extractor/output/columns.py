from eye_extractor.output.validators import is_int, is_in_range, is_date, contains, is_string, is_upper

OUTPUT_COLUMNS = {
    # metadata
    'docid': [],
    'studyid': [is_int],
    'date': [is_date],
    'encid': [is_int],
    'is_training': [is_in_range(0, 1)],
    # visual acuity
    'iop_measurement_re': [],
    'iop_measurement_le': [],
    'iop_instrument_type': [],
    'vacc_denominator_re': [is_int, is_in_range(15, 401)],
    'vacc_denominator_le': [is_int, is_in_range(15, 401)],
    'vasc_denominator_re': [is_int, is_in_range(15, 401)],
    'vasc_denominator_le': [is_int, is_in_range(15, 401)],
    'vaph_denominator_re': [is_int, is_in_range(15, 401)],
    'vaph_denominator_le': [is_int, is_in_range(15, 401)],
    'varx_denominator_re': [is_int, is_in_range(15, 401)],
    'varx_denominator_le': [is_int, is_in_range(15, 401)],
    'vacc_numbercorrect_re': [is_int, is_in_range(-6, 6)],
    'vacc_numbercorrect_le': [is_int, is_in_range(-6, 6)],
    'vasc_numbercorrect_re': [is_int, is_in_range(-6, 6)],
    'vasc_numbercorrect_le': [is_int, is_in_range(-6, 6)],
    'vaph_numbercorrect_re': [is_int, is_in_range(-6, 6)],
    'vaph_numbercorrect_le': [is_int, is_in_range(-6, 6)],
    'varx_numbercorrect_re': [is_int, is_in_range(-6, 6)],
    'varx_numbercorrect_le': [is_int, is_in_range(-6, 6)],
    'vacc_letters_re': [contains('CF', 'HM', 'LP', 'NLP')],
    'vacc_letters_le': [contains('CF', 'HM', 'LP', 'NLP')],
    'vasc_letters_re': [contains('CF', 'HM', 'LP', 'NLP')],
    'vasc_letters_le': [contains('CF', 'HM', 'LP', 'NLP')],
    'vaph_letters_re': [contains('CF', 'HM', 'LP', 'NLP')],
    'vaph_letters_le': [contains('CF', 'HM', 'LP', 'NLP')],
    'varx_letters_re': [contains('CF', 'HM', 'LP', 'NLP')],
    'varx_letters_le': [contains('CF', 'HM', 'LP', 'NLP')],
    'vacc_distance_re': [is_int],
    'vacc_distance_le': [is_int],
    'vasc_distance_re': [is_int],
    'vasc_distance_le': [is_int],
    'vaph_distance_re': [is_int],
    'vaph_distance_le': [is_int],
    'varx_distance_re': [is_int],
    'varx_distance_le': [is_int],
    'etdrs_nc_re': [is_int],
    'etdrs_nc_le': [is_int],
    'etdrs_wc_re': [is_int],
    'etdrs_wc_le': [is_int],
    'etdrs_ph_re': [is_int],
    'etdrs_ph_le': [is_int],
    'varx_type_re': [],
    'varx_type_le': [],
    'manifestrx_sphere_re': [],
    'manifestrx_cylinder_re': [],
    'manifestrx_axis_re': [],
    'manifestrx_add_re': [],
    'manifestrx_denom_re': [],
    'manifestrx_ncorr_re': [],
    'manifestrx_sphere_le': [],
    'manifestrx_cylinder_le': [],
    'manifestrx_axis_le': [],
    'manifestrx_add_le': [],
    'manifestrx_denom_le': [],
    'manifestrx_ncorr_le': [],
    'amd_re': [is_int],
    'amd_le': [is_int],
    'subretinal_hem_re': [],
    'subretinal_hem_le': [],
    'fluid_amd_re': [],
    'fluid_amd_le': [],
    'drusen_size_re': [],
    'drusen_type_re': [],
    'drusen_size_unk': [],
    'drusen_type_unk': [],
    'drusen_size_le': [],
    'drusen_type_le': [],
    'pigmentchanges_le': [is_in_range(-1, 1)],
    'pigmentchanges_re': [is_in_range(-1, 1)],
    'rvo_yesno_le': [is_in_range(-1, 1)],
    'rvo_yesno_re': [is_in_range(-1, 1)],
    'rao_yesno_le': [is_in_range(-1, 1)],
    'rao_yesno_re': [is_in_range(-1, 1)],
    'cataract_yesno_le': [is_in_range(-1, 1)],
    'cataract_yesno_re': [is_in_range(-1, 1)],
    'cataractiol_yesno_le': [is_in_range(-1, 1)],
    'cataractiol_yesno_re': [is_in_range(-1, 1)],
    'cataractsurg_ioltype_re': [],
    'cataractsurg_ioltype_le': [],
    'cataractsurg_iolpower_re': [],
    'cataractsurg_iolpower_le': [],
    'cataractsurg_otherlens_re': [],
    'cataractsurg_otherlens_le': [],
    'cataractsurg_dt_le': [],
    'cataractsurg_dt_re': [],
    'cataractsurg_dt_unk': [],
    'cataractsurg_yesno': [],
    'cataract_type_re': [],
    'cataract_type_le': [],
    'catsurg_comp_yesno_re': [],
    'catsurg_comp_yesno_le': [],
    'catsurg_comp_describe_re': [],
    'catsurg_comp_describe_le': [],
    'nscataract_severity_re': [is_in_range(-1, 5)],
    'nscataract_severity_le': [is_in_range(-1, 5)],
    'cortcataract_severity_re': [is_in_range(-1, 5)],
    'cortcataract_severity_le': [is_in_range(-1, 5)],
    'pscataract_severity_re': [is_in_range(-1, 5)],
    'pscataract_severity_le': [is_in_range(-1, 5)],
    'uveitis_yesno_re': [],
    'uveitis_yesno_le': [],
    'famhx_glaucoma': [is_in_range(-1, 1)],
    'famhx_diabetes': [is_in_range(-1, 1)],
    'famhx_migraine': [is_in_range(-1, 1)],
    'famhx_cataract': [is_in_range(-1, 1)],
    'famhx_dr': [is_in_range(-1, 1)],
    'famhx_dme': [is_in_range(-1, 1)],
    'famhx_retinal_detachment': [is_in_range(-1, 1)],
    'famhx_amblyopia': [is_in_range(-1, 1)],
    'famhx_amd': [is_in_range(-1, 1)],
    'perhx_glaucoma': [is_in_range(-1, 1)],
    'perhx_diabetes': [is_in_range(-1, 1)],
    'perhx_migraine': [is_in_range(-1, 1)],
    'perhx_cataract': [is_in_range(-1, 1)],
    'perhx_dr': [is_in_range(-1, 1)],
    'perhx_dme': [is_in_range(-1, 1)],
    'perhx_retinal_detachment': [is_in_range(-1, 1)],
    'perhx_amblyopia': [is_in_range(-1, 1)],
    'perhx_amd': [is_in_range(-1, 1)],
    # exam section
    'cupdiscratio_rev': [],
    'cupdiscratio_reh': [],
    'cupdiscratio_lev': [],
    'cupdiscratio_leh': [],
    #
    'intraocular_lens_re': [],
    'intraocular_lens_le': [],
    'posterior_cap_opacity_re': [],
    'posterior_cap_opacity_le': [],
    # glaucoma drops
    'glaucoma_rx_none': [is_in_range(-1, 1)],
    'glaucoma_rx_dorzolamide': [is_in_range(-1, 1)],
    'glaucoma_rx_echothiophate_iodide': [is_in_range(-1, 1)],
    'glaucoma_rx_timolol': [is_in_range(-1, 1)],
    'glaucoma_rx_acetylcholine': [is_in_range(-1, 1)],
    'glaucoma_rx_latanoprostene_bunod': [is_in_range(-1, 1)],
    'glaucoma_rx_apraclonidine': [is_in_range(-1, 1)],
    'glaucoma_rx_carbachol': [is_in_range(-1, 1)],
    'glaucoma_rx_netarsudil': [is_in_range(-1, 1)],
    'glaucoma_rx_metipranolol': [is_in_range(-1, 1)],
    'glaucoma_rx_bimatoprost': [is_in_range(-1, 1)],
    'glaucoma_rx_brimonidine': [is_in_range(-1, 1)],
    'glaucoma_rx_carteolol': [is_in_range(-1, 1)],
    'glaucoma_rx_epinephrine': [is_in_range(-1, 1)],
    'glaucoma_rx_latanoprost': [is_in_range(-1, 1)],
    'glaucoma_rx_betaxolol': [is_in_range(-1, 1)],
    'glaucoma_rx_unoprostone': [is_in_range(-1, 1)],
    'glaucoma_rx_travoprost': [is_in_range(-1, 1)],
    'glaucoma_rx_dipivefrin': [is_in_range(-1, 1)],
    'glaucoma_rx_levobunolol': [is_in_range(-1, 1)],
    'glaucoma_rx_pilocarpine': [is_in_range(-1, 1)],
    'glaucoma_rx_physostigmine': [is_in_range(-1, 1)],
    'glaucoma_rx_brinzolamide': [is_in_range(-1, 1)],
    'glaucoma_rx_tafluprost': [is_in_range(-1, 1)],
    # glaucoma dx/type
    'glaucoma_dx_re': [is_upper],
    'glaucoma_dx_le': [is_upper],
    'glaucoma_dx_unk': [is_upper],
    'glaucoma_type_re': [is_upper],
    'glaucoma_type_le': [is_upper],
    'glaucoma_type_unk': [is_upper],

}
