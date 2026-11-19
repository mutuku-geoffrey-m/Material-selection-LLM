import sys, os
sys.path.insert(0, os.path.abspath("."))
from src.nlp_parser import NLPTranslationLayer
from src.llm_orchestrator import LLMOrchestrator
from src.rag_engine import RAGEngine

rag = RAGEngine()
orchestrator = LLMOrchestrator()

prompt = "Select a material for a stone crusher jaw. Maximize hardness and strength"
nlp_spec = NLPTranslationLayer.parse_engineering_prompt(prompt)

retrieved = rag.query(prompt, top_k=4)
rag_prompt = rag.build_augmented_prompt(prompt, nlp_spec, retrieved)

result = orchestrator.generate_recommendation(
    user_prompt=prompt,
    engineering_spec=nlp_spec,
    rag_prompt=rag_prompt,
    retrieved_chunks=retrieved,
    annual_demand_kg=1500.0
)

top_mats = result.get("ranked_materials", [])
print(f"Total ranked candidates returned: {len(top_mats)}")
if top_mats:
    top = top_mats[0]
    print(f"Top Candidate: {top.get('name')}")
    print(f"Raw Score: {top.get('raw_score')}")
    print(f"Final Metric: {top.get('final_metric')}")
    print(f"Cost USD: {top.get('cost_usd')}")
    print(f"Yield Strength: {top.get('yield_strength_mpa')}")
print("\nRecommendation Mode Used:", result.get("mode_used"))
print("Arbitrated:", (result.get("arbitration_result") or {}).get("arbitrated"))
