import sys, os
sys.path.insert(0, os.path.abspath("."))
from src.ashby_engine import rank_materials

ranked = rank_materials(fdm_only=False, prompt_text="Select a material for a stone crusher jaw. Maximize hardness and strength")
print("Ranked materials with fdm_only=False:", len(ranked))
for i, m in enumerate(ranked[:10]):
    print(f"{i+1}. {m['name']} | Metric: {m['final_metric']:.2f} | Cost: ${m.get('cost_usd', 0):.2f}/kg")
