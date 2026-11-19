import sys, os
sys.path.insert(0, os.path.abspath('.'))
from src.llm_orchestrator import LLMOrchestrator
from src.nlp_parser import NLPTranslationLayer
from src.materials_db import get_material

orch = LLMOrchestrator(mode='deterministic')
parser = NLPTranslationLayer()

user_prompt = 'Select a material for a stone crusher jaw. Maximize hardness and strength'
nlp_spec = parser.parse_layman_prompt(user_prompt)
result = orch.generate_recommendation(
    user_prompt=user_prompt,
    engineering_spec=nlp_spec,
    rag_prompt=user_prompt,
    retrieved_chunks=[],
    annual_demand_kg=100.0
)

ranked = result.get('ranked_materials', [])
top = ranked[0]
print('top key:', repr(top.get('key')))
print('top name:', repr(top.get('name')))
top_data = get_material(top.get('key',''))
print('get_material returned:', top_data is not None)
if top_data:
    print('  cost_per_kg_usd:', top_data.get('cost_per_kg_usd'))
    print('  yield_strength:', top_data.get('yield_strength'))
    print('  youngs_modulus_print_xy:', top_data.get('youngs_modulus_print_xy'))
else:
    print('  FALLBACK to top_mat, keys:', list(top.keys()))
    print('  cost_usd (in top):', top.get('cost_usd'))
    print('  yield_strength_mpa (in top):', top.get('yield_strength_mpa'))
    print('  youngs_modulus_gpa (in top):', top.get('youngs_modulus_gpa'))
