"""
Runs the 100 benchmark scenarios through the SAME path the Streamlit app uses
(parser -> LLMOrchestrator in deterministic mode -> Ashby filters -> techno-economics),
without needing Ollama. Writes benchmark_100_full_pipeline.csv for supervisor/peer review.

Usage:  python scripts/run_benchmark_full_pipeline.py
"""
import os, sys, csv, time, collections
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)
from tests.test_100_benchmarks import SCENARIOS
from src.nlp_parser import NLPTranslationLayer
from src.llm_orchestrator import LLMOrchestrator

orch = LLMOrchestrator(mode=LLMOrchestrator.MODE_AUTONOMOUS_EXPERT)
rows, lat = [], []
for i, prompt in enumerate(SCENARIOS, 1):
    t0 = time.perf_counter()
    spec = NLPTranslationLayer.parse_engineering_prompt(prompt)
    res = orch.generate_recommendation(prompt, spec, "", [], 1500.0)
    dt = (time.perf_counter() - t0) * 1000.0
    lat.append(dt)
    ranked = res.get("ranked_materials") or []
    syn = spec["synthesized_engineering_spec"]
    rows.append([i, prompt, syn.get("component_classification"), res.get("ashby_index_used"),
                 " | ".join(m["name"] for m in ranked[:3]), round(dt, 1), "", ""])

out = os.path.join(ROOT, "benchmark_100_full_pipeline.csv")
with open(out, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["#", "Prompt", "Parsed component class", "Ashby index used", "Top-3 materials",
                "Latency ms", "Expected index (reviewer)", "Correct? Y/N (reviewer)"])
    w.writerows(rows)

top1 = collections.Counter(r[4].split(" | ")[0] for r in rows if r[4])
lat.sort()
print(f"Scenarios: {len(rows)}   mean {sum(lat)/len(lat):.0f} ms   p95 {lat[int(0.95*len(lat))-1]:.0f} ms")
print("Most frequent #1 picks:")
for k, v in top1.most_common(6):
    print(f"  {v:3d}  {k}")
print("Wrote", out)
