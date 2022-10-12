# Changelog
All notable changes to this project should be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Reference

Types of changes:

* `Added`: for new features.
* `Changed`: for changes in existing functionality.
* `Deprecated`: for soon-to-be removed features.
* `Removed`: for now removed features.
* `Fixed`: for any bug fixes.
* `Security`: in case of vulnerabilities.

## [Unreleased]

### Changed
- Wet/dry AMD variable 'UNSPECIFIED' to 'YES'
- Wet/dry AMD variables use other relevant variables to update final results
- Expanded fluid to include macular edema

## v20220921

### Fixed
- Fixed DR variables in output
- Added `_unk` laterality to subretinal heme and pigment
- Renamed `UNKNOWN`/`YES`/`blank` for `drusen_type` and `drusen_size`

## v20220829

### Added
- Additional DR variables, including severity

## v20220822

### Added
- RNFL values (from text, not scans)
- Keratometry
- CMT from Macula OCT
- Diabetic retinopathy variables

## v20220815

### Added
- Glaucoma disc pallor for `disc_pallor_glaucoma_re`, `disc_pallor_glaucoma_le`, `disc_pallor_glaucoma_unk`
  - YES/NO/UNKNOWN
- RVO type
- RVO treatment
- RVO antivegf
- Fluid for AMD and RVO

## v20220808

### Added
- AMD lasertype for `amd_lasertype_re`, `amd_lasertype_le`, `amd_lasertype_unk`
  - -1 (UNKNOWN)
  - 0 (NONE/NEGATED)
  - 1 (LASER)
  - 2 (PHOTODYNAMIC)
  - 3 (THERMAL)
  - 4 (OTHER) -> not implemented: NLP requires target
  - 5 (UNSPECIFIED) -> not implemented: unclear
- AMD antivegf for `amd_antivegf_re`, `amd_antivegf_le`, `amd_antivegf_unk`
  - -1 (UNKNOWN)
  - 0 (NONE/NEGATED)
  - 1 (BEVACIZUMAB)
  - 2 (AFLIBERCEPT)
  - 3 (RANIBIZUMAB)
  - 4 (OTHER)
  - 5 (UNSPECIFIED) -> not implemented: unclear
- Diabetic retinopathy (yes/no)
- DR Microaneurysm (yes/no)
- DR Hard Exudates (yes/no)
- DR Disc Edema (yes/no)
- DR Hemorrhage (yes/no)
- DR Hemorrhage Type (yes/no)
  - 0 (UNKNOWN)
  - 1 (NONE)
  - 2 (INTRARETINAL)
  - 3 (DOT_BLOT)
  - 4 (PRERETINAL)
  - 5 (VITREOUS)
  - 6 (SUBRETINAL)

### Changed
- Merged treatment options across diseases

## v20220801

### Added
- Additional cup disc ratio patterns
- peripapillary atrophy variables (yes=1/no=0/unknown=-1) for `ppa_re`, `ppa_le`, `ppa_unk`
- Headers API to improve access to multiple header types
- Glaucoma treatment variable for `glaucoma_dx_re`, `glaucoma_dx_le`, `glaucoma_dx_unk`: 
  - UNKNOWN
  - NONE
  - OBSERVE
  - CONTINUE RX
  - NEW MEDICATION
  - ALT
  - SLT
  - SURGERY
  - TRABECULOPLASTY
- Exfoliation variable (yes=1/no=0/unknown=-1) for `exfoliation_re`, `exfoliation_le`, `exfoliation_unk`
- Preglaucoma variable for `preglaucoma_re`, `preglaucoma_le`, `preglaucoma_unk`:
  - UNKNOWN
  - NONE
  - SUSPECT
  - PPG
  - INCREASED CD
  - OHTN (ocular hypertension)
- Validator takes logical `or` rather than `and`
- Pigmentary epithelial detachment (yes=1/no=0/unknown=-1) for `ped_re`, `ped_le`, `ped_unk`
- Unknown laterality to amd fluid: `amd_fluid_unk`
- Choroidal neovascularization (CNV) (yes=1/no=0/unknown=-1) for `choroidalneovasc_re`, `choroidalneovasc_le`, `choroidalneovasc_unk`
- Subretinal scar variable for `subret_fibrous_re`, `subret_fibrous_le`, `subret_fibrous_unk`:
  - UNKNOWN
  - NO
  - YES
  - MACULAR
  - SUBRETINAL
  - DISCIFORM
- geographic atrophy (GA) (yes=1/no=0/unknown=-1) for `geoatrophy_re`, `geoatrophy_le`, `geoatrophy_unk`
- dry severity variable for `dryamd_severity_re`, `dryamd_severity_le`, `dryamd_severity_unk`
  - NB: severity does not seem to appear, so 'UNSPECIFIED' ~= 'YES' (1)
- wet severity variable for `wetamd_severity_re`, `wetamd_severity_le`, `wetamd_severity_unk`
  - NB: severity does not seem to appear, so 'UNSPECIFIED' ~= 'YES' (1)
- amd vitamin variable `amd_vitamin` (yes=1/no=0/unknown=-1)

### Changed
- Output format of `amd_fluid_` to uppercase string

### Fixed
- Typo in determining type of glaucoma drops

## v20220725

### Added
- Tilted disc variable (yes=1/no=0/unknown=-1) for `tilted_disc_re`, `tilted_disc_le`, `tilted_disc_unk`
- Disc notch variable (yes=1/no=0/unknown=-1) for `disc_notch_re`, `disc_notch_le`, `disc_notch_unk`
- Disc hemorrhage variable (yes=1/no=0/unknown=-1) for `disc_hemo_re`, `disc_hemo_le`, `disc_hemo_unk`
- Central corneal thickness variable (cct value as integer) for `centralcornealthickness_re`, `centralcornealthickness_le`, `centralcornealthickness_unk`
- Gonioscopy variable (OPEN/CLOSED/UNKNOWN) for `gonio_re`, `gonio_le`, `gonio_unk`
