#---
params_placeholders = {
    "uses"          :   "<!-- primary uses -->",
    "side_effects"  :   "<!-- common side effects and notable side effects -->",
    "interactions"  :   "<!-- notable interactions -->",
    }
#---
all_params = {}
params_to_add = {}
#---
all_params['first'] = [
    "Verifiedfields",
    "Verifiedrevid",
    "Watchedfields",
    "Watchedrevid",

    "verifiedfields",
    "verifiedrevid",
    "watchedfields",
    "watchedrevid",

    "drug_name",
    "INN",
    "image",
    "width",
    "alt",
    "image2",
    "width2",
    "alt2",
    "caption",
    "caption2",
    "imageL",
    "widthL",
    "altL",
    "imageR",
    "widthR",
    "altR",
    "captionLR",
    ]
#---
all_params['combo'] = {
    "mab" : [
        "type",
        "mab_type",
        "source",
        "target",
    ],
    "vaccine" : [
        "type",
        "target",
        "vaccine_type",
    ],
    "combo" : [
        "type",
        "component1",
        "class1",
        "component2",
        "class2",
        "component3",
        "class3",
        "component4",
        "class4",
        "component5",
        "class5",
    ],
    "all" : []
}
#---
all_params['combo']['all'] = all_params['combo']['mab'] + all_params['combo']['vaccine'] + all_params['combo']['combo']
all_params['combo']['all'] = list(set(all_params['combo']['all']))
#---
all_params['names'] = [
    "pronounce",
    "pronounce_ref",
    "pronounce_comment",
    "tradename",
    "synonyms",
    "INN",
    "AAN",
    "BAN",
    "JAN",
    "USAN",
    "IUPAC_name",
    ]
#---
params_to_add['names'] = ["pronounce", "tradename", "synonyms", "IUPAC_name"]
#---
all_params['gene'] = [
    "gt_target_gene",
    "gt_vector",
    "gt_nucleic_acid_type",
    "gt_editing_method",
    "gt_delivery_method",
    ]
#---
all_params['clinical'] = [
    "class",  
    "uses", 
    "side effects", 
    "side effect", 
    "side_effects", 
    "side_effect", 
    "interactions", 
    "pregnancy_AU", 
    "pregnancy_AU_comment", 
    "pregnancy_US", 
    "pregnancy_US_comment", 
    "pregnancy_category", 
    "breastfeeding", 
    "PLLR", 
    "routes_of_administration", 
    "onset", 
    "duration_of_action", 
    "defined_daily_dose",
    "routes_of_use", 
    "typical_dose",
    "dependency_liability",
    "addiction_liability",
    "duration",
    ]
#---
params_to_add['clinical'] = [
    "class",
    "uses",
    "side_effects", 
    "interactions", 
    "onset", 
    "duration_of_action", 
    "defined_daily_dose", 
    "typical_dose", 
    "breastfeeding"
    ]
#---
all_params['external'] = [
    "Drugs.com",
    "NLM",
    "MedlinePlus",
    ]
#---
params_to_add['external'] = [
    "Drugs.com",
    # "NLM",
    "MedlinePlus",
    ]
#---
all_params['legal'] = [
    "INN_EMA",
    "engvar",
    "legal_AU",
    "legal_AU_comment",
    "legal_BR",
    "legal_BR_comment",
    "legal_CA",
    "legal_CA_comment",
    "legal_DE",
    "legal_DE_comment",
    "legal_EU",
    "legal_EU_comment",
    "legal_NZ",
    "legal_NZ_comment",
    "legal_UN",
    "legal_UN_comment",
    "legal_UK",
    "legal_UK_comment",
    "legal_US",
    "legal_US_comment",
    "legal_status",
    "DailyMedID",
    "licence_US",
    "license_US",
    "licence_CA",
    "license_CA",
    "licence_EU",
    "license_EU",
    ]
#---
all_params['physiological'] = [
    "source_tissues",
    "target_tissues",
    "receptors",
    "agonists",
    "antagonists",
    "precursor",
    "biosynthesis",
    "sources",
    "targets",
    ]
#---
all_params['pharmacokinetic'] = [
    "bioavailability",
    "protein_bound",
    "metabolism",
    "metabolites",
    "elimination_half-life",
    "excretion",
    ]
#---
all_formola_params = [
    "Ac", "Ag", "Al", "Am", "Ar", "As", "At", "Au",
    "B", "Ba", "Be", "Bh", "Bi", "Bk", "Br", "C",
    "Ca", "Cd", "Ce", "Cf", "Cl", "Cm", "Cn", "Co",
    "Cr", "Cs", "Cu", "D", "Db", "Ds", "Dy", "Er",
    "Es", "Eu", "F", "Fe", "Fl", "Fm", "Fr", "Ga",
    "Gd", "Ge", "H", "He", "Hf", "Hg", "Ho", "Hs",
    "I", "In", "Ir", "K", "Kr", "La", "Li", "Lr",
    "Lu", "Lv", "Mc", "Md", "Mg", "Mn", "Mo", "Mt",
    "N", "Na", "Nb", "Nd", "Ne", "Nh", "Ni", "No",
    "Np", "O", "Og", "Os", "P", "Pa", "Pb", "Pd",
    "Pm", "Po", "Pr", "Pt", "Pu", "Ra", "Rb", "Re",
    "Rf", "Rg", "Rh", "Rn", "Ru", "S", "Sb", "Sc",
    "Se", "Sg", "Si", "Sm", "Sn", "Sr", "Ta", "Tb",
    "Tc", "Te", "Th", "Ti", "Tl", "Tm", "Ts", "U",
    "V", "W", "Xe", "Y", "Yb", "Zn", "Zr",
]
#---
all_params['chemical'] = all_formola_params + [
	"charge",
	"chemical_formula",
	"chemical_formula_ref",
	"chemical_formula_comment",

	"SMILES",
	"SMILES2",
	
	"StdInChI",
	"StdInChI_Ref",
	"StdInChI_comment",

	"StdInChIKey",
	"StdInChIKey_Ref",

	"StdInChI2",
	"StdInChI2_Ref",

	"StdInChIKey2",
	"StdInChIKey2_Ref",
	
	"Jmol",
	"Jmol2",

	"molecular_weight",
	"molecular_weight_round",
	"molecular_weight_unit",
	"molecular_weight_ref",
	"molecular_weight_comment",

	"chirality",

	"density",
	"density_notes",

	"melting_point",
	"melting_high",
	"melting_notes",

	"boiling_point",
	"boiling_high",
	"boiling_notes",

	"solubility",
	"sol_units",
	"specific_rotation"
    ]
#---
all_params['last'] = []
#---