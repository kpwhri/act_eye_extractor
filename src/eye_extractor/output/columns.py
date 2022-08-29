from eye_extractor.output.validators import is_int, is_in_range, is_date, contains, is_string, is_upper, \
    is_float_in_range, equals

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
    'vacc_denominator_re': [is_in_range(15, 401)],
    'vacc_denominator_le': [is_in_range(15, 401)],
    'vasc_denominator_re': [is_in_range(15, 401)],
    'vasc_denominator_le': [is_in_range(15, 401)],
    'vaph_denominator_re': [is_in_range(15, 401)],
    'vaph_denominator_le': [is_in_range(15, 401)],
    'varx_denominator_re': [is_in_range(15, 401)],
    'varx_denominator_le': [is_in_range(15, 401)],
    'vacc_numbercorrect_re': [is_in_range(-6, 6)],
    'vacc_numbercorrect_le': [is_in_range(-6, 6)],
    'vasc_numbercorrect_re': [is_in_range(-6, 6)],
    'vasc_numbercorrect_le': [is_in_range(-6, 6)],
    'vaph_numbercorrect_re': [is_in_range(-6, 6)],
    'vaph_numbercorrect_le': [is_in_range(-6, 6)],
    'varx_numbercorrect_re': [is_in_range(-6, 6)],
    'varx_numbercorrect_le': [is_in_range(-6, 6)],
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
    'fluid_amd_re': [is_in_range(-1, 5)],
    'fluid_amd_le': [is_in_range(-1, 5)],
    'fluid_amd_unk': [is_in_range(-1, 5)],
    'amd_subretfluid_re': [is_in_range(-1, 1)],
    'amd_subretfluid_le': [is_in_range(-1, 1)],
    'amd_subretfluid_unk': [is_in_range(-1, 1)],
    'amd_intrarettfluid_re': [is_in_range(-1, 1)],
    'amd_intrarettfluid_le': [is_in_range(-1, 1)],
    'amd_intrarettfluid_unk': [is_in_range(-1, 1)],
    'drusen_size_re': [],
    'drusen_type_re': [],
    'drusen_size_unk': [],
    'drusen_type_unk': [],
    'drusen_size_le': [],
    'drusen_type_le': [],
    'pigmentchanges_le': [is_in_range(-1, 1)],
    'pigmentchanges_re': [is_in_range(-1, 1)],

    ## RO (RVO/RAO)
    # RVO
    'rvo_yesno_re': [is_in_range(-1, 1)],
    'rvo_yesno_le': [is_in_range(-1, 1)],
    'rvo_yesno_unk': [is_in_range(-1, 1)],
    'rvo_type_re': [is_in_range(-1, 3)],
    'rvo_type_le': [is_in_range(-1, 3)],
    'rvo_type_unk': [is_in_range(-1, 3)],
    'rvo_treatment_re': [is_in_range(-1, 6)],
    'rvo_treatment_le': [is_in_range(-1, 6)],
    'rvo_treatment_unk': [is_in_range(-1, 6)],
    'rvo_antivegf_re': [is_in_range(-1, 3)],
    'rvo_antivegf_le': [is_in_range(-1, 3)],
    'rvo_antivegf_unk': [is_in_range(-1, 3)],
    'rvo_subretfluid_re': [is_in_range(-1, 1)],
    'rvo_subretfluid_le': [is_in_range(-1, 1)],
    'rvo_subretfluid_unk': [is_in_range(-1, 1)],
    'rvo_intraretfluid_re': [is_in_range(-1, 1)],
    'rvo_intraretfluid_le': [is_in_range(-1, 1)],
    'rvo_intraretfluid_unk': [is_in_range(-1, 1)],
    'fluid_rvo_re': [is_in_range(-1, 5)],
    'fluid_rvo_le': [is_in_range(-1, 5)],
    'fluid_rvo_unk': [is_in_range(-1, 5)],

    # RAO
    'rao_yesno_le': [is_in_range(-1, 1)],
    'rao_yesno_re': [is_in_range(-1, 1)],
    'rao_yesno_unk': [is_in_range(-1, 1)],

    ## Cataract
    'cataract_yesno_re': [is_in_range(-1, 1)],
    'cataract_yesno_le': [is_in_range(-1, 1)],
    'cataractiol_yesno_re': [is_in_range(-1, 1)],
    'cataractiol_yesno_le': [is_in_range(-1, 1)],
    'cataractiol_yesno_unk': [is_in_range(-1, 1)],
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
    'nscataract_severity_re': [is_float_in_range(-1, 5)],
    'nscataract_severity_le': [is_float_in_range(-1, 5)],
    'cortcataract_severity_re': [is_float_in_range(-1, 5)],
    'cortcataract_severity_le': [is_float_in_range(-1, 5)],
    'pscataract_severity_re': [is_float_in_range(-1, 5)],
    'pscataract_severity_le': [is_float_in_range(-1, 5)],
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
    # gonioscopy
    'gonio_re': [is_upper],
    'gonio_le': [is_upper],
    'gonio_unk': [is_upper],
    # cct
    'centralcornealthickness_re': [is_in_range(450, 750), equals(-1)],
    'centralcornealthickness_le': [is_in_range(450, 750), equals(-1)],
    'centralcornealthickness_unk': [is_in_range(450, 750), equals(-1)],
    # disc hemorrhage: yes/no/unknown
    'disc_hem_re': [is_in_range(-1, 1)],
    'disc_hem_le': [is_in_range(-1, 1)],
    'disc_hem_unk': [is_in_range(-1, 1)],
    # disc notch: yes/no/unknown
    'disc_notch_re': [is_in_range(-1, 1)],
    'disc_notch_le': [is_in_range(-1, 1)],
    'disc_notch_unk': [is_in_range(-1, 1)],
    # tilted disc: yes/no/unknown
    'tilted_disc_re': [is_in_range(-1, 1)],
    'tilted_disc_le': [is_in_range(-1, 1)],
    'tilted_disc_unk': [is_in_range(-1, 1)],
    # peri-papillary atrophy: yes/no/unknown
    'ppa_re': [is_in_range(-1, 1)],
    'ppa_le': [is_in_range(-1, 1)],
    'ppa_unk': [is_in_range(-1, 1)],
    # exfoliation: yes/no/unknown
    'exfoliation_re': [is_in_range(-1, 1)],
    'exfoliation_le': [is_in_range(-1, 1)],
    'exfoliation_unk': [is_in_range(-1, 1)],
    # preglaucoma
    'preglaucoma_re': [is_upper],
    'preglaucoma_le': [is_upper],
    'preglaucoma_unk': [is_upper],
    # glaucoma treatment
    'glaucoma_tx_re': [is_upper],
    'glaucoma_tx_le': [is_upper],
    'glaucoma_tx_unk': [is_upper],
    # glaucoma disc pallor: yes/no/unknown
    'disc_pallor_glaucoma_re': [is_in_range(-1, 1)],
    'disc_pallor_glaucoma_le': [is_in_range(-1, 1)],
    'disc_pallor_glaucoma_unk': [is_in_range(-1, 1)],
    # pigmentary epithelial detachment
    'ped_re': [is_in_range(-1, 1)],
    'ped_le': [is_in_range(-1, 1)],
    'ped_unk': [is_in_range(-1, 1)],
    # choroidal neovascularization
    'choroidalneovasc_re': [is_in_range(-1, 1)],
    'choroidalneovasc_le': [is_in_range(-1, 1)],
    'choroidalneovasc_unk': [is_in_range(-1, 1)],
    # scar: subretinal fibrous
    'subret_fibrous_re': [is_upper],
    'subret_fibrous_le': [is_upper],
    'subret_fibrous_unk': [is_upper],
    # geographic atrophy (yes/no/unknown)
    'geoatrophy_re': [is_in_range(-1, 1)],
    'geoatrophy_le': [is_in_range(-1, 1)],
    'geoatrophy_unk': [is_in_range(-1, 1)],
    # dry severity
    'dryamd_severity_re': [is_upper],
    'dryamd_severity_le': [is_upper],
    'dryamd_severity_unk': [is_upper],
    # wet severity
    'wetamd_severity_re': [is_upper],
    'wetamd_severity_le': [is_upper],
    'wetamd_severity_unk': [is_upper],
    # vitamin (yes/no/unknown)
    'amd_vitamin': [is_in_range(-1, 1)],
    # lasertype
    'amd_lasertype_re': [is_in_range(-1, 5)],
    'amd_lasertype_le': [is_in_range(-1, 5)],
    'amd_lasertype_unk': [is_in_range(-1, 5)],
    # antivegf
    'amd_antivegf_re': [is_in_range(-1, 5)],
    'amd_antivegf_le': [is_in_range(-1, 5)],
    'amd_antivegf_unk': [is_in_range(-1, 5)],
    # intra retinal fluid
    'amd_intraretfluid_re': [is_in_range(-1, 5)],
    'amd_intraretfluid_le': [is_in_range(-1, 5)],
    'amd_intraretfluid_unk': [is_in_range(-1, 5)],

    ## DIABETIC RETINOPATHY
    # diab_retinop_yesno
    'diab_retinop_yesno_re': [is_in_range(-1, 1)],
    'diab_retinop_yesno_le': [is_in_range(-1, 1)],
    'diab_retinop_yesno_unk': [is_in_range(-1, 1)],
    # ret_microaneurysm
    'ret_microaneurysm_re': [is_in_range(-1, 1)],
    'ret_microaneurysm_le': [is_in_range(-1, 1)],
    'ret_microaneurysm_unk': [is_in_range(-1, 1)],
    # hardexudates
    'hardexudates_re': [is_in_range(-1, 1)],
    'hardexudates_le': [is_in_range(-1, 1)],
    'hardexudates_unk': [is_in_range(-1, 1)],
    # disc_edema_dr
    'disc_edema_dr_re': [is_in_range(-1, 1)],
    'disc_edema_dr_le': [is_in_range(-1, 1)],
    'disc_edema_dr_unk': [is_in_range(-1, 1)],
    # hemorrhage_dr
    'hemorrhage_dr_re': [is_in_range(-1, 1)],
    'hemorrhage_dr_le': [is_in_range(-1, 1)],
    'hemorrhage_dr_unk': [is_in_range(-1, 1)],
    # hemorrhage_typ_dr
    'hemorrhage_typ_dr_re': [is_in_range(-1, 6)],
    'hemorrhage_typ_dr_le': [is_in_range(-1, 6)],
    'hemorrhage_typ_dr_unk': [is_in_range(-1, 6)],
    # laser scars
    'dr_laser_scars_re': [is_in_range(-1, 1)],
    'dr_laser_scars_le': [is_in_range(-1, 1)],
    'dr_laser_scars_unk': [is_in_range(-1, 1)],
    # laser panretinal photocoagulation scars
    'laserpanret_photocoag_re': [is_in_range(-1, 1)],
    'laserpanret_photocoag_le': [is_in_range(-1, 1)],
    'laserpanret_photocoag_unk': [is_in_range(-1, 1)],
    # neovascularization
    'neovasc_yesno_re': [is_in_range(-1, 1)],
    'neovasc_yesno_le': [is_in_range(-1, 1)],
    'neovasc_yesno_unk': [is_in_range(-1, 1)],
    # neovascularization of angle
    'nva_yesno_re': [is_in_range(-1, 1)],
    'nva_yesno_le': [is_in_range(-1, 1)],
    'nva_yesno_unk': [is_in_range(-1, 1)],
    # neovascularization of iris
    'nvi_yesno_re': [is_in_range(-1, 1)],
    'nvi_yesno_le': [is_in_range(-1, 1)],
    'nvi_yesno_unk': [is_in_range(-1, 1)],
    # neovascularization of disc
    'nvd_yesno_re': [is_in_range(-1, 1)],
    'nvd_yesno_le': [is_in_range(-1, 1)],
    'nvd_yesno_unk': [is_in_range(-1, 1)],
    # neovascularization elsewhere
    'nve_yesno_re': [is_in_range(-1, 1)],
    'nve_yesno_le': [is_in_range(-1, 1)],
    'nve_yesno_unk': [is_in_range(-1, 1)],
    # diabetic macular edema
    'dmacedema_yesno_re': [is_in_range(-1, 1)],
    'dmacedema_yesno_le': [is_in_range(-1, 1)],
    'dmacedema_yesno_unk': [is_in_range(-1, 1)],
    # clinically significant diabetic macular edema
    'dmacedema_clinsignif_re': [is_in_range(-1, 1)],
    'dmacedema_clinsignif_le': [is_in_range(-1, 1)],
    'dmacedema_clinsignif_unk': [is_in_range(-1, 1)],
    # OCT for central macular thickness
    'oct_centralmac_re': [is_in_range(-1, 1)],
    'oct_centralmac_le': [is_in_range(-1, 1)],
    'oct_centralmac_unk': [is_in_range(-1, 1)],
    # Laser scar types
    'focal_dr_laser_scar_type_re': [is_in_range(-1, 1)],
    'focal_dr_laser_scar_type_le': [is_in_range(-1, 1)],
    'focal_dr_laser_scar_type_unk': [is_in_range(-1, 1)],
    # Diabetic retinopathy type
    'diabretinop_type_re': [is_in_range(-1, 2)],
    'diabretinop_type_le': [is_in_range(-1, 2)],
    'diabretinop_type_unk': [is_in_range(-1, 2)],
    # Presence of fluid
    'fluid_dr_re': [is_in_range(-1, 5)],
    'fluid_dr_le': [is_in_range(-1, 5)],
    'fluid_dr_unk': [is_in_range(-1, 5)],
    # Diabetic macular edema treatment
    'dmacedema_tx_re': [is_in_range(-1, 5)],
    'dmacedema_tx_le': [is_in_range(-1, 5)],
    'dmacedema_tx_unk': [is_in_range(-1, 5)],
    # Anti-VEGF diabetic macular edema
    'dmacedema_antivegf_re': [is_in_range(-1, 4)],
    'dmacedema_antivegf_le': [is_in_range(-1, 4)],
    'dmacedema_antivegf_unk': [is_in_range(-1, 4)],
    # Diabetic retinopathy treatment
    'drtreatment_re': [is_in_range(-1, 6)],
    'drtreatment_le': [is_in_range(-1, 6)],
    'drtreatment_unk': [is_in_range(-1, 6)],
    # Diabetic macular edema CMT value
    'dmacedema_cmt_re': [is_in_range(-1, 1000)],
    'dmacedema_cmt_le': [is_in_range(-1, 1000)],
    'dmacedema_cmt_unk': [is_in_range(-1, 1000)],
}
