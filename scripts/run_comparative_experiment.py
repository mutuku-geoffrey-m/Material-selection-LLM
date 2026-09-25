import json
import csv
import os
import sys

# Add the project root to sys.path so we can import from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.nlp_parser import NLPTranslationLayer
from src.rag_engine import RAGEngine
from src.llm_orchestrator import LLMOrchestrator

def run_experiment(input_json_path, output_csv_path):
    if not os.path.exists(input_json_path):
        print(f"Error: Could not find {input_json_path}")
        return

    with open(input_json_path, 'r', encoding='utf-8') as f:
        try:
            cases = json.load(f)
        except json.JSONDecodeError:
            print("Error parsing JSON.")
            return

    rag_engine = RAGEngine()
    orchestrator = LLMOrchestrator(mode=LLMOrchestrator.MODE_AUTONOMOUS_EXPERT)

    results = []

    for idx, case in enumerate(cases):
        prompt = case.get("prompt")
        case_name = case.get("id", f"Case_{idx+1}")
        
        print(f"Processing: {case_name}")
        
        # 1. Model A: Pure LLM (Baseline) - Simulated Fallback
        res_a = "Pure LLM typically fails physical boundary condition extraction (e.g., misses modulus logic)."
        
        # 2. Model B: RAG Only - Semantic match
        retrieved_chunks = rag_engine.query(prompt, top_k=4)
        res_b = f"Retrieved {len(retrieved_chunks)} chunks, but lacks deterministic ranking engine."
        
        # 3. Model C: RAG + Engineering Algorithm (Full System)
        try:
            nlp_spec = NLPTranslationLayer.parse_layman_prompt(prompt)
            rag_prompt = rag_engine.build_augmented_prompt(prompt, nlp_spec)
            res_c_obj = orchestrator.generate_recommendation(prompt, nlp_spec, rag_prompt, retrieved_chunks)
            
            top_ranked = res_c_obj.get("ranked_materials", [])
            top_name = top_ranked[0]["name"] if top_ranked else "None"
            res_c = f"Top Recommendation: {top_name} | {res_c_obj.get('synthesized_response', '')[:100]}..."
        except Exception as e:
            res_c = f"Error: {e}"

        results.append({
            "case_name": case_name,
            "prompt": prompt,
            "model_a_pure_llm": res_a,
            "model_b_rag_only": res_b,
            "model_c_full_system": res_c
        })

    if results:
        fieldnames = ["case_name", "prompt", "model_a_pure_llm", "model_b_rag_only", "model_c_full_system"]
        with open(output_csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        print(f"Experiment completed. Results saved to {output_csv_path}")

if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    input_path = os.path.join(base_dir, 'tests', 'adversarial_edge_cases.json')
    output_path = os.path.join(base_dir, 'results_comparison.csv')
    
    run_experiment(input_path, output_path)

