"""
patterns.py

This file contains the regular expression patterns for identifying section in optometry and ophthalmology notes.
"""
import enum
import re


class SectionName(enum.StrEnum):
    ANGLE = 'angle'
    LENS = 'lens'
    MACULA = 'macula'
    ASSESSMENT = 'assessment'
    PLAN = 'plan'
    PERIPHERY = 'periphery'
    VESSELS = 'vessels'
    SUBJECTIVE = 'subjective'
    GLAUCOMA_TYPE = 'glaucoma_type'
    GLAUCOMA = 'glaucoma'
    GLAUCOMA_FLOWSHEET = 'glaucoma_flowsheet'
    GONIOSCOPY = 'gonio'
    LAST_GONIOSCOPY = 'last_gonio'
    PACHYMETRY = 'pachymetry'
    CCT = 'cct'
    OPTIC_NERVE = 'optic_nerve'
    CUP_DISC = 'cup_disc'
    CUP_DISC_OD = 'cup_disc_od'
    CUP_DISC_OS = 'cup_disc_os'
    COMMENT = 'comment'


nonw = r'[^\w\n\-:]'
nonw_s = fr'{nonw}*'
sep = rf'{nonw_s}(?:(?:and|&){nonw_s})?'

applanation = r'(?:app?(?:lanation)?)'
iop = fr'(?:iop|intra[-\s]?ocular{nonw_s}pressure)\'?s?'
tonometry = r'(?:tonometry|t?nct|tag)(?:\s*method)?'

tears = r'(?:lacrim\w+|tears?)'
lids = r'(?:(?:eye)?lids?)'
lashes = r'(?:eye)?lash(?:es)?'
lymph = r'lymph'
conjunctiva = r'conj(?:unc?tiva)?'
sclera = r'sclera'
adnexa = r'ad?nexa'
orbit = r'orbits?'
anterior = r'(?:ant(?:erior)?)'
posterior = r'(?:post?(?:erior)?)'
chamber = r'chambers?'
vitreous = r'vit(?:reous)?'
segment = r'segment'
patient = r'(?:patient|pt)'
meds = r'med(?:ication)?s?'
previous = r'(?:last|prev(?:ious)?|past)'
cup_disc = r'c(?:up)?\W*d(?:is[ck])?'
od = fr'(?:o{nonw_s}d|r{nonw_s}e)'
os = fr'(?:o{nonw_s}s|l{nonw_s}e)'
history = fr'(?:hx|history)'
eye = fr'(?:eye|ocular|ophthalmic)'
visual_acuity = rf'(?:(?:visual{nonw_s})?acuit(?:y|ies)|vas?)'
visual_fields = rf'(?:vf|visual{nonw_s}field\'?s?)'
manifest_rx = rf'(?:(?:manifest{nonw_s})?refraction|mrx)'
bcva = rf'(?:best{nonw_s}corrected{nonw_s}vision|bcva)'
date = r'\d{1,2}/\d{1,2}/\d{2,4}'
dx = r'(?:diagnosis|dx)'

section_pre_pat = rf'^{nonw_s}'
section_post_pat = rf'{nonw_s}[:-](?P<content>.*)$'
targets = [
    (SectionName.CCT, r'ccts?'),
    (SectionName.MACULA, r'mac(?:ula)?'),
    ('impression', r'imp(?:ression)?'),
    ('narrative', r'narrative'),
    ('dilation', fr'(?:pupil(?:l?ary)?{nonw_s})?dilat(?:ed|ion)(?:with{nonw_s}m&n|eye{nonw_s}health{nonw_s}exam\w*)?'),
    ('tonometry', fr'(?:(?:{applanation}|{iop}|{tonometry}|by){nonw_s})+'),
    ('past_iop', fr'{previous}{nonw_s}{iop}'),
    ('oriented',
     rf'(?:{patient}{nonw_s})?(?:alert{nonw_s}and{nonw_s})?orient\w*{nonw_s}(?:to{nonw_s})?(?:p{nonw_s}p{nonw_s}[tp])?'),
    ('cc', rf'(?:(?:cc|chief{nonw_s}complaint|reason{nonw_s}for{nonw_s}visit){nonw_s})+'),
    ('pupils', rf'pupils?'),
    ('eom', rf'eom\'?s?'),
    ('previous_vf', rf'{previous}{nonw_s}{visual_fields}'),
    ('vf', rf'{visual_fields}'),
    ('vf_type', rf'{visual_fields}{nonw_s}type'),
    (
        'cvf', rf'(?:c(?:onf\w*)?{nonw_s}v(?:isual)?{nonw_s}f(?:ield)?\'?s?|visual{nonw_s}fields?{nonw_s}conf\w*)'),
    (('pupils', 'iris'), rf'iris{nonw_s}pupils?'),
    (('lids', 'lashes', 'tears', 'lymph'), rf'{lids}{sep}{lashes}{sep}{tears}{sep}{lymph}'),
    (('lids', 'lashes', 'tears'), rf'{lids}{sep}{lashes}{sep}{tears}'),
    (('lids', 'lashes'), rf'{lids}{sep}{lashes}'),
    (('lids', 'adnexa'), rf'{lids}{sep}{adnexa}'),
    (('lids', 'lashes', 'conjunctiva'), rf'{lids}{sep}{lashes}{sep}{conjunctiva}'),
    (('lashes', 'tears'), rf'{lashes}{sep}{tears}'),
    (('lashes', 'conjunctiva'), rf'{lashes}{sep}{conjunctiva}'),
    ('lids', f'{lids}'),
    (SectionName.LENS, f'lens(?:es)?'),
    ('iol', f'iol'),
    ('adnexa', f'{adnexa}'),
    ('retina', f'retina'),
    ('dry_eye', f'dry{nonw_s}eye'),
    ('trauma', f'trauma'),
    ('orbit', f'{orbit}'),
    (('orbit', 'adnexa'), f'{orbit}{sep}{adnexa}'),
    (('orbit', 'adnexa'), f'{adnexa}{sep}{orbit}'),
    ('lashes', f'{lashes}'),
    ('tears', f'{tears}'),
    ('conjunctiva', f'{conjunctiva}'),
    ('sclera', f'{sclera}'),
    ('cornea', f'cornea\'?s?'),
    ('anterior_chamber', f'{anterior}{nonw_s}{chamber}'),
    ('anterior_vitreous', f'{anterior}{nonw_s}{vitreous}'),
    ('anterior_segment', f'{anterior}{nonw_s}{segment}'),
    ('posterior_chamber', f'{posterior}{nonw_s}{chamber}'),
    ('posterior_vitreous', f'{posterior}{nonw_s}{vitreous}'),
    ('posterior_segment', f'{posterior}{nonw_s}{segment}'),
    ('vitreous', f'{vitreous}'),
    (('conjunctiva', 'sclera'), f'{conjunctiva}{sep}{sclera}'),
    (('conjunctiva', 'sclera'), f'{sclera}{sep}{conjunctiva}'),
    (SectionName.ASSESSMENT, f'assessment(?:{nonw_s}comments?)?'),
    (SectionName.PLAN, f'plan(?:{nonw_s}(?:and{nonw_s}follow{nonw_s}up|comments?))?'),
    ((SectionName.ASSESSMENT, SectionName.PLAN), fr'assessment{nonw_s}plan'),
    ('presents', f'{patient}{nonw_s}presents{nonw_s}with'),
    (SectionName.OPTIC_NERVE, f'optic{nonw_s}nerves?'),
    (SectionName.VESSELS, f'vessels?'),
    (SectionName.ANGLE, f'angles?(?:{nonw_s}v[oa]n{nonw_s}herr?ick)?'),
    ('iris', f'iris'),
    ('disc', f'discs?'),
    ('drawings', f'drawings?'),
    ('iris_rubeosis', rf'iris{nonw_s}rubeosis'),
    ('csn', f'csn'),
    ('signed_by', f'signed(?:{nonw_s}by)?'),
    ('objective', fr'objective'),
    ('subjective', fr'subjective'),
    ('date', f'date'),
    ('time', f'time'),
    ('name', f'name'),
    ('mrn', f'mrn'),
    ('num_children', f'number{nonw_s}of{nonw_s}children'),
    ('education_yrs', f'years{nonw_s}of{nonw_s}education'),
    ('marital_status', f'marital{nonw_s}status'),
    ('occupation', f'(?:occupation|occupational{nonw_s}{history})'),
    ('va', f'(?:today{nonw_s})?{visual_acuity}'),
    ('previous_va', f'{previous}{nonw_s}{visual_acuity}'),
    ('allergies', f'(?:review{nonw_s}of{nonw_s}patient\'?s?{nonw_s})?allerg(?:y|ies)'),
    ('dob', f'(?:date{nonw_s}of{nonw_s}birth|dob)'),
    ('eye_meds', fr'(?:'
                 fr'(?:current|active){nonw_s})?'
                 fr'{eye}{nonw_s}{meds}'
                 fr'(?:{nonw_s}'
                 fr'(?:and{nonw_s}{previous}{nonw_s}dose|as{nonw_s}of{nonw_s}{date})'
                 fr')?'),
    ('eye_meds_ineffective', fr'{meds}\s*ineffective'),
    ('eye_meds_not_tolerated', fr'{meds}\s*not\s*tolerated'),
    ('med_allergies', fr'{meds}{nonw_s}allerg(?:y|ies)'),
    ('meds', fr'(?:active|current){nonw_s}{meds}(?:{nonw_s}as{nonw_s}of{nonw_s}{date})?'),
    ('peripheral_retina', f'periph(?:eral)?{nonw_s}retinal?'),
    (SectionName.PERIPHERY, fr'periphery'),
    ('problem_list', f'(?:{patient}{nonw_s})?(?:(?:active|current){nonw_s})?problem{nonw_s}list'),
    ('hpi',
     fr'(?:(?:ccs?|chief{nonw_s}complaints?|hpi|history{nonw_s}of{nonw_s}present{nonw_s}illness|reason{nonw_s}for{nonw_s}exam\w*){nonw_s})+'),
    (SectionName.LAST_GONIOSCOPY, fr'{previous}{nonw_s}gonio\w*'),
    (SectionName.GONIOSCOPY, fr'gonio\w*'),
    (SectionName.PACHYMETRY, fr'pachymetry'),
    (SectionName.CUP_DISC, fr'{cup_disc}'),
    (SectionName.CUP_DISC_OD, fr'(?:{od}{nonw_s}{cup_disc}|{cup_disc}{nonw_s}{od})'),
    (SectionName.CUP_DISC_OS, fr'(?:{os}{nonw_s}{cup_disc}|{cup_disc}{nonw_s}{os})'),
    ('od', fr'{od}'),
    ('os', fr'{os}'),
    ('oct', fr'(?:(?:mac\w*)?{nonw_s}oct(?:{nonw_s}mac\w*)?)'),
    ('hx', fr'(?:{history}|{previous})'),
    ('eye_hx',
     fr'(?:{previous}{nonw_s})?(?:personal{nonw_s})?(?:medical{nonw_s})?{eye}{nonw_s}{history}(?:{nonw_s}of)?'),
    ('family_eye_hx', fr'(?:family{nonw_s}{eye}{nonw_s}(?:health{nonw_s})?{history}(?:{nonw_s}of)?|fohx)'),
    ('med_hx',
     fr'(?:(?:pertinent{nonw_s})?(?:{previous}{nonw_s})?(?:medical|{patient}){nonw_s}{history}(?:{nonw_s}of)?|pmhx)'),
    ('family_hx', fr'(?:family{nonw_s}{history}(?:{nonw_s}of)?|fhx)'),
    ('manifest_rx', fr'{manifest_rx}'),
    ('last_manifest_rx', fr'(?:{previous}{nonw_s}glasses{nonw_s}rx{nonw_s})?{previous}{nonw_s}{manifest_rx}s?'),
    ('bcva', fr'{bcva}'),
    ('add', fr'add'),
    ('near_add', fr'near{nonw_s}add'),
    ('inter_add', fr'inter{nonw_s}add'),
    ('type', fr'type'),
    ('cover_test', fr'cover{nonw_s}test'),
    ('eye_rx', fr'new{nonw_s}{eye}{nonw_s}(?:rx|prescription)'),
    ('pain_level', fr'pain{nonw_s}level'),
    ('fundus', fr'fund(?:us|i)'),
    ('prism', fr'prism'),
    ('past_eye_surgery', fr'{previous}{nonw_s}{eye}{nonw_s}surgery(?:{nonw_s}or{nonw_s}laser)'),
    ('surgery', fr'surgery'),
    ('current_glasses', fr'(?:current{nonw_s}glasses|glasses{nonw_s}rx)'),
    ('review_of_systems', fr'review{nonw_s}of{nonw_s}systems'),
    (SectionName.GLAUCOMA, fr'glaucoma'),
    (SectionName.GLAUCOMA_FLOWSHEET, fr'glaucoma{nonw_s}flowsheet'),
    (SectionName.GLAUCOMA_TYPE, fr'type{nonw_s}of{nonw_s}glaucoma'),
    ('cataracts', fr'cataracts?'),
    ('diabetes', fr'diabetes'),
    ('diabetic_issues', fr'diabetic{nonw_s}{eye}{nonw_s}issues'),
    ('amd', fr'(?:ar?md|(?:age\W?related{nonw_s})?macular{nonw_s}degeneration)'),
    ('ret_detach', fr'(?:rd|retinal{nonw_s}detachment)'),
    ('blindness', fr'blindness'),
    ('ta', fr'ta'),
    ('hypertension', fr'(?:hypertension|htn)'),
    ('migraine', fr'migraine'),
    ('cancer', fr'cancer'),
    ('thyroid', fr'thyroid'),
    ('cardio', fr'cardio'),
    ('respiratory', fr'resp(?:iratory)?'),
    ('arthritis', fr'(?:rheumatoid{nonw_s})?arthritis'),
    ('other', fr'other'),
    ('corneal_disease', fr'corneal{nonw_s}disease'),
    ('eye_assessment', fr'{eye}{nonw_s}health{nonw_s}assessment'),
    ('best_corrected_vision', fr'best{nonw_s}corrected{nonw_s}vision'),
    # social history
    ('social_hx', fr'(?:social{nonw_s}{history}|shx)'),
    ('drug_use', fr'drug{nonw_s}use'),
    ('alcohol_use', fr'alcohol{nonw_s}use'),
    ('tobacco_use', fr'tobacco{nonw_s}use'),
    ('smoking', fr'smoking'),
    (SectionName.COMMENT, fr'comments?'),
    # surgery
    ('preop_dx', f'pre{nonw_s}operative{nonw_s}{dx}'),
    ('postop_dx', f'post{nonw_s}operative{nonw_s}{dx}'),
    ('op_date', f'date{nonw_s}of{nonw_s}operation'),
    ('procedures', f'procedures(?:{nonw_s}performed)?'),
    ('anesthesia_type', fr'anesthesia{nonw_s}type'),
    ('procedure_duration', fr'estimated{nonw_s}length{nonw_s}of{nonw_s}procedure'),
]

PATTERNS = [
    (cat,  # category
     2,  # default level
     re.compile(f'{section_pre_pat}(?P<name>{pat}){section_post_pat}', re.I | re.MULTILINE),
     ) for cat, pat in targets
]


class PatternGroup:
    MACULA_ASSESSMENT_PLAN = (SectionName.MACULA, SectionName.ASSESSMENT, SectionName.PLAN)
