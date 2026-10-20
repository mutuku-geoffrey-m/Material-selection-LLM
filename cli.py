"""
Command-Line Interface (CLI) for Engineering Material Selection & Optimization System (EMS-OS).
Supports headless execution, batch query evaluation, and benchmark validation for qualified engineers.
"""

import argparse
import json
import sys
import os

# Ensure UTF-8 output encoding in Windows console to avoid charmap UnicodeEncodeError on Greek symbols
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass

# Add root directory to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.nlp_parser import NLPTranslationLayer
from src.rag_engine import RAGEngine
from src.llm_orchestrator import LLMOrchestrator
from src.report_generator import EngineeringReportGenerator
from src.ashby_engine import AshbyIndex


def run_single_prompt(prompt: str, mode: str = LLMOrchestrator.MODE_LOCAL, verbose: bool = False, demand_kg: float = 1000.0):
    print("\n" + "=" * 80)
    print("ENGINEERING MATERIAL SELECTION & OPTIMIZATION SYSTEM (EMS-OS CLI)")
    print("=" * 80)
    print(f"\n[ENGINEERING SPECIFICATION]: {prompt}\n")

    # 1. Scientific Specification Translation
    print("[1/3] Parsing Engineering Specification via NLP Translation Layer...")
    spec = NLPTranslationLayer.parse_engineering_prompt(prompt)
    ashby_info = spec["synthesized_engineering_spec"]
    boundary = spec["boundary_conditions_and_constraints"]

    print(f"  -> Component Classification: {ashby_info['component_classification']}")
    print(f"  -> Governing Ashby Index:    {ashby_info['primary_governing_ashby_index']} (M = {ashby_info['ashby_mathematical_formula']})")
    print(f"  -> Governing Standards:      {ashby_info.get('governing_standards') or 'Standard Engineering Good Practice'}")
    print(f"  -> Submerged Aquatic:        {boundary['submerged_aquatic_exposure']}")
    print(f"  -> Manufacturing Process:    {boundary['manufacturing_process']}")

    # 2. Vector DB Retrieval
    print("\n[2/3] Querying ChromaDB Engineering Knowledge Base...")
    rag = RAGEngine()
    rag_prompt = rag.build_augmented_prompt(prompt, spec, top_k=4)
    chunks = rag.query(prompt, top_k=4)
    print(f"  -> Retrieved {len(chunks)} verified engineering document chunks from persistent vector store.")

    # 3. LLM Orchestration
    print(f"\n[3/3] Executing Multi-Engine Synthesis & Optimization ({mode})...")
    orchestrator = LLMOrchestrator(mode=mode)
    result = orchestrator.generate_recommendation(
        user_prompt=prompt,
        engineering_spec=spec,
        rag_prompt=rag_prompt,
        retrieved_chunks=chunks,
        annual_demand_kg=demand_kg
    )

    print("\n" + "-" * 80)
    print("SYNTHESIZED ENGINEERING SPECIFICATION & DECISION:")
    print("-" * 80)
    print(result["synthesized_response"])

    if verbose and result.get("techno_economic_leaderboard"):
        print("\n" + "-" * 80)
        print("TECHNO-ECONOMIC & SUPPLY CHAIN LEADERBOARD (EOQ & MOQ):")
        print("-" * 80)
        for r in result["techno_economic_leaderboard"][:5]:
            econ = r["economics"]
            eoq = econ["eoq"]
            print(f"  Rank {r['overall_rank']}: {r['name']} ({r['family']})")
            print(f"    - Ashby Score: {r['technical_ashby_score']:.2f} | Composite Score: {r['composite_score']:.1f}/100")
            print(f"    - Raw Cost: ${econ['raw_cost_usd_per_kg']:.2f}/kg | Sourcing: {econ['sourcing_category']} ({econ['lead_time_days']} days)")
            print(f"    - MOQ: {econ['minimum_order_quantity_kg']:.0f} kg | Optimal EOQ Batch: {eoq['eoq_batch_size_kg']:.0f} kg")

    print("\n" + "=" * 80)
    return result


def main():
    parser = argparse.ArgumentParser(description="Engineering Material Selection & Optimization System (EMS-OS CLI)")
    parser.add_argument("--prompt", "-p", type=str, help="Engineering design specification query")
    parser.add_argument("--benchmark", "-b", action="store_true", help="Run the benchmark engineering test prompt")
    parser.add_argument("--mode", "-m", choices=[LLMOrchestrator.MODE_LOCAL, LLMOrchestrator.MODE_CLOUD, LLMOrchestrator.MODE_AUTONOMOUS_EXPERT],
                        default=LLMOrchestrator.MODE_LOCAL, help="Inference pipeline mode")
    parser.add_argument("--demand", "-d", type=float, default=1500.0, help="Annual project demand in kg")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print detailed mechanical and economic metrics")

    args = parser.parse_args()

    if args.benchmark or not args.prompt:
        benchmark_prompt = "I want to make a blade that will push water, carry a heavy load, and sit in a river all day, but I don't know the exact weight."
        run_single_prompt(benchmark_prompt, mode=args.mode, verbose=True, demand_kg=args.demand)
    else:
        run_single_prompt(args.prompt, mode=args.mode, verbose=args.verbose, demand_kg=args.demand)


if __name__ == "__main__":
    main()
