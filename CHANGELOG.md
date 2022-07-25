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

### Added
- Additional cup disc ratio patterns
- peripapillary atrophy variables (yes=1/no=0/unknown=-1) for `ppa_re`, `ppa_le`, `ppa_unk`
- Headers API to improve access to multiple header types
- Glaucoma treatment variable for `glaucoma_dx_re`, `glaucoma_dx_le`, `glaucoma_dx_unk`: 
  - UNKNOWN
  - NONE
  - OBSERVE
  - CONTINUE_RX
  - NEW_MEDICATION
  - ALT
  - SLT
  - SURGERY
  - TRABECULOPLASTY
- Exfoliation variable (yes=1/no=0/unknown=-1) for `exfoliation_re`, `exfoliation_le`, `exfoliation_unk`

### Fixed
- Typo in determining type of glaucoma drops

## v20220725

### Added
- Tilted disc variable (yes=1/no=0/unknown=-1) for `tilted_disc_re`, `tilted_disc_le`, `tilted_disc_unk`
- Disc notch variable (yes=1/no=0/unknown=-1) for `disc_notch_re`, `disc_notch_le`, `disc_notch_unk`
- Disc hemorrhage variable (yes=1/no=0/unknown=-1) for `disc_hemo_re`, `disc_hemo_le`, `disc_hemo_unk`
- Central corneal thickness variable (cct value as integer) for `centralcornealthickness_re`, `centralcornealthickness_le`, `centralcornealthickness_unk`
- Gonioscopy variable (OPEN/CLOSED/UNKNOWN) for `gonio_re`, `gonio_le`, `gonio_unk`
