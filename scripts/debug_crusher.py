import sys, os
sys.path.insert(0, os.path.abspath('.'))
from src.ashby_engine import rank_materials

results = rank_materials(
    fdm_only=False,
    prompt_text='Select a material for a stone crusher jaw. Maximize hardness and strength'
)

print('TOP 5 RESULTS:')
for i, m in enumerate(results[:5]):
    name = m.get('name', '?')
    family = m.get('family', '?')
    score = m.get('final_metric', m.get('raw_score', 0))
    cost = m.get('cost_per_kg_usd', m.get('techno_economics', {}).get('raw_cost_usd_per_kg', '?'))
    ys = m.get('yield_strength', '?')
    print(f'{i+1}. {name} | {family} | Score: {score:.3f} | Cost: {cost} | YS: {ys}')

print()
print('Checking if Mg AM100A passes crusher filter...')
from src.ashby_engine import MATERIALS_DATABASE, list_all_materials
mats = list_all_materials()
mg_mats = [m for m in mats if 'AM100A' in m.get('name','') or 'Magnesium' in m.get('family','')]
print(f'Mg mats in db: {len(mg_mats)}')
for m in mg_mats[:3]:
    print(f"  {m['name']} | ys={m.get('yield_strength',0)} | family={m.get('family','')}")
