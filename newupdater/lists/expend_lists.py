#---
main_temps_list = [
    "drugbox",
    "Infobox anatomy",
    "Infobox birth control",
    "Infobox diagnostic",
    "Infobox diagnostic",
    "Infobox drug (new)",
    "Infobox drug class",
    "Infobox drug mechanism",
    "infobox drug",
    "infobox medical condition (new)", 
    "infobox medical condition",
    "Infobox medical intervention",
    "Infobox nonhuman protein",
    "Infobox nutritional value",
    "Infobox organization",
    "Infobox project",
    "Infobox protein family",
    "Infobox sanitation technology",
    "Infobox vein",
]
#---
main_temps_list = [ x.lower() for x in main_temps_list]
#---
IMC_params = {}
#---
IMC_params["infobox medical condition"] = [
    "name",
    "synonym",
    "image",
    "alt",
    "caption",
    "pronounce",
    "field",
    # "specialty",
    "symptoms",
    "complications",
    "onset",
    "duration",
    "types",
    "causes",
    "risks",
    "diagnosis",
    "differential",
    "prevention",
    "treatment",
    "medication",
    "prognosis",
    "frequency",
    "deaths",
]
IMC_params["infobox medical condition (new)"] = IMC_params["infobox medical condition"]
# ---
dup_params = {}
#---
dup_params["infobox medical condition"] = {
    "synonyms": "synonym",
    "speciality": "field",
    "specialty": "field",
}
#---
dup_params["infobox medical condition (new)"] = dup_params["infobox medical condition"]
# ---
