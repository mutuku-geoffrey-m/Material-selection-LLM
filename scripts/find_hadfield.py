import sys, os
sys.path.insert(0, os.path.abspath("."))
from src.ashby_engine import rank_materials, AshbyIndex
from src.nlp_parser import NLPTranslationLayer

prompt = "Select a material for a stone crusher jaw. Maximize hardness and strength"
nlp_spec = NLPTranslationLayer.parse_engineering_prompt(prompt)
ranked = rank_materials(index_key=nlp_spec["synthesized_engineering_spec"]["primary_governing_ashby_index"], prompt_text=prompt)

for i, m in enumerate(ranked):
    if "Hadfield" in m.get("name", "") or "A128" in m.get("name", ""):
        print(f"Rank {i+1}: {m.get('name')} | Metric: {m.get('final_metric')} | Cost: {m.get('cost_per_kg_usd')}")
