import sys, os
sys.path.insert(0, os.path.abspath("."))
from src.ashby_engine import rank_materials, AshbyIndex
from src.nlp_parser import NLPTranslationLayer

prompt = "Select a material for a stone crusher jaw. Maximize hardness and strength"
nlp_spec = NLPTranslationLayer.parse_engineering_prompt(prompt)
synthesized = nlp_spec["synthesized_engineering_spec"]
bnd = nlp_spec["boundary_conditions_and_constraints"]

ranked = rank_materials(
    index_key=synthesized["primary_governing_ashby_index"],
    fdm_only=bnd.get("fdm_only_preference", False),
    prompt_text=prompt
)

print("Component classification:", synthesized.get("component_classification"))
print("Primary governing index:", synthesized.get("primary_governing_ashby_index"))
print("Total ranked:", len(ranked))
print("\nTop 5 Candidates:")
for i, m in enumerate(ranked[:5]):
    ys = m.get("yield_strength_mpa") or m.get("yield_strength") or 0
    hb = m.get("brinell_hardness") or m.get("hardness_hb") or 0
    cost = m.get("cost_per_kg_usd") or 0.0
    metric = m.get("final_metric") or 0.0
    print(f"{i+1}. {m.get('name')} | Metric: {metric:.3f} | Yield: {ys} MPa | Hardness: {hb} HB | Cost: ${cost:.2f}/kg")
