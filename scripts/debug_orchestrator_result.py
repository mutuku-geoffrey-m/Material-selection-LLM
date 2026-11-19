import sys, os
sys.path.insert(0, os.path.abspath('.'))
from src.llm_orchestrator import LLMOrchestrator
from src.nlp_parser import NLPTranslationLayer

orch = LLMOrchestrator(mode='deterministic')
parser = NLPTranslationLayer()

user_prompt = 'Select a material for a stone crusher jaw. Maximize hardness and strength'
nlp_spec = parser.parse_layman_prompt(user_prompt)

print('=== NLP SPEC BOUNDARY CONDITIONS ===')
bc = nlp_spec.get('boundary_conditions_and_constraints', {})
print('fdm_only_preference:', bc.get('fdm_only_preference'))
print('manufacturing_process:', bc.get('manufacturing_process'))

result = orch.generate_recommendation(
    user_prompt=user_prompt,
    engineering_spec=nlp_spec,
    rag_prompt=user_prompt,
    retrieved_chunks=[],
    annual_demand_kg=100.0
)

print('\n=== RESULT KEYS ===')
print(list(result.keys()))
ranked = result.get('ranked_materials', [])
print(f'\nTotal ranked: {len(ranked)}')
print('\nTOP 3:')
for i, m in enumerate(ranked[:3]):
    print(f'{i+1}. {m.get("name","?")}')
    print(f'   keys: {list(m.keys())}')
    print(f'   final_metric: {m.get("final_metric","MISSING")}')
    print(f'   raw_score: {m.get("raw_score","MISSING")}')
    print(f'   score: {m.get("score","MISSING")}')
    print(f'   cost_per_kg_usd: {m.get("cost_per_kg_usd","MISSING")}')
    print()
