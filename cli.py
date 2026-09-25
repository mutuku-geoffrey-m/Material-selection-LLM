"""
Command-Line Interface (CLI) for Autonomous Material Selection System.
Supports headless execution, batch query evaluation, and benchmark validation.
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


def run_single_prompt(prompt: str, mode: str = LLMOrchestrator.MODE_LOCAL, verbose: bool = False):
    print("\n" + "=" * 75)
    print("AUTONOMOUS LLM-BASED MATERIAL SELECTION SYSTEM (CLI MODE)")
    print("=" * 75)
    print(f"\n[USER PROMPT]: {prompt}\n")

    # 1. NLP Translation
    print("[1/3] Parsing Layman Intent via NLP Translation Layer...")
    spec = NLPTranslationLayer.parse_layman_prompt(prompt)
    ashby_info = spec["synthesized_engineering_spec"]
    boundary = spec["boundary_conditions_and_constraints"]

    print(f"  -> Component Classification: {ashby_info['component_classification']}")
    print(f"  -> Governing Ashby Index:    {ashby_info['primary_governing_ashby_index']} (M = {ashby_info['ashby_mathematical_formula']})")
    print(f"  -> Submerged River Exposure: {boundary['submerged_aquatic_exposure']}")
    print(f"  -> Manufacturing Route:      {boundary['manufacturing_process']}")

    # 2. Vector DB Retrieval
    print("\n[2/3] Querying ChromaDB Engineering Knowledge Base...")
    rag = RAGEngine()
    rag_prompt = rag.build_augmented_prompt(prompt, spec, top_k=4)
    chunks = rag.query(prompt, top_k=4)
    print(f"  -> Retrieved {len(chunks)} verified engineering document chunks from persistent vector store.")

    # 3. LLM Orchestration
    print(f"\n[3/3] Executing Synthesis via Orchestrator ({mode})...")
    orchestrator = LLMOrchestrator(mode=mode)
    result = orchestrator.generate_recommendation(
        user_prompt=prompt,
        engineering_spec=spec,
        rag_prompt=rag_prompt,
        retrieved_chunks=chunks
    )

    print("\n" + "-" * 75)
    print("SYNTHESIZED ENGINEERING SPECIFICATION & DECISION:")
    print("-" * 75)
    print(result["synthesized_response"])

    if verbose:
        print("\n" + "-" * 75)
        print("TOP 3 MATERIAL RANKINGS (ASHBY METRIC):")
        print("-" * 75)
        for i, m in enumerate(result["ranked_materials"][:3], 1):
            print(f"  {i}. {m['name']} | Metric: {m['final_metric']:.2f} | Density: {m['density_g_cm3']:.2f} g/cm3 | E: {m['youngs_modulus_gpa']} GPa | Yield: {m['yield_strength_mpa']} MPa")

    print("\n" + "=" * 75)
    return result


def main():
    parser = argparse.ArgumentParser(description="Autonomous LLM Material Selection CLI")
    parser.add_argument("--prompt", "-p", type=str, help="Natural language engineering query")
    parser.add_argument("--benchmark", "-b", action="store_true", help="Run the capstone micro-hydro benchmark prompt")
    parser.add_argument("--mode", "-m", choices=[LLMOrchestrator.MODE_LOCAL, LLMOrchestrator.MODE_CLOUD, LLMOrchestrator.MODE_AUTONOMOUS_EXPERT],
                        default=LLMOrchestrator.MODE_AUTONOMOUS_EXPERT, help="Operating mode")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print detailed mechanical metrics")

    args = parser.parse_args()

    if args.benchmark or not args.prompt:
        benchmark_prompt = "I want to make a blade that will push water, carry a heavy load, and sit in a river all day, but I don't know the exact weight."
        run_single_prompt(benchmark_prompt, mode=args.mode, verbose=True)
    else:
        run_single_prompt(args.prompt, mode=args.mode, verbose=args.verbose)


if __name__ == "__main__":
    main()
