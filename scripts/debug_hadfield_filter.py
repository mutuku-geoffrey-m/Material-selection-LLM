import sys, os
sys.path.insert(0, os.path.abspath("."))
from src.ashby_engine import list_all_materials, AshbyIndex
from src.nlp_parser import NLPTranslationLayer

prompt = "Select a material for a stone crusher jaw. Maximize hardness and strength"
nlp_spec = NLPTranslationLayer.parse_engineering_prompt(prompt)
index_key = nlp_spec["synthesized_engineering_spec"]["primary_governing_ashby_index"]
prompt_lower = prompt.lower()

m = [x for x in list_all_materials() if "Hadfield" in x.get("name", "")][0]
print("Testing material:", m["name"])
print("family:", m.get("family"))
print("yield_strength:", m.get("yield_strength"))
print("fdm_printability:", m.get("fdm_printability"))

# Now let's trace every filter:
fdm_only = False
cnc_only = False
flexible_cushion_required = False

# check filters:
is_fdm = (m.get("fdm_printability") or {}).get("ease_of_printing", "Not FDM Printable") != "Not FDM Printable"
print("is_fdm:", is_fdm)

is_heavy_spring = any(w in prompt_lower for w in ["coil spring", "suspension spring"])
print("is_heavy_spring:", is_heavy_spring)

is_ceramic = m.get("family") == "Technical Ceramic" or "Ceramic" in m.get("name", "")
print("is_ceramic:", is_ceramic)

is_rock_crushing = any(w in prompt_lower for w in ["crusher", "stone crusher", "jaw crusher", "crusher jaw", "crushing jaw", "rock crusher", "jaw plate", "crushing plate", "hammer mill"])
print("is_rock_crushing:", is_rock_crushing)

if is_rock_crushing:
    fam = m.get("family", "")
    is_soft = any(w in fam for w in ["Magnesium", "Aluminum", "Copper", "Brass", "Thermoplastic", "Polymer", "Elastomer"])
    print("is_soft:", is_soft)
    print("yield_strength < 300:", m.get("yield_strength", 0) < 300.0)

# check other filters in rank_materials:
from src.ashby_engine import calculate_ashby_index
base_score = calculate_ashby_index(m, index_key)
print("base_score:", base_score)
