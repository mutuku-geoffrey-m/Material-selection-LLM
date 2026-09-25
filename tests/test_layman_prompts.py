"""
Tests for Non-Technical Layman Everyday Prompts.
Ensures conversational queries from non-technical users receive physically accurate,
domain-tailored material selections instead of defaulting to identical materials.
"""

import pytest
from src.nlp_parser import NLPTranslationLayer
from src.llm_orchestrator import LLMOrchestrator
from src.rag_engine import RAGEngine


@pytest.fixture(scope="module")
def system():
    rag = RAGEngine()
    orchestrator = LLMOrchestrator(mode=LLMOrchestrator.MODE_AUTONOMOUS_EXPERT)
    return rag, orchestrator


def test_layman_knife_selection(system):
    rag, orchestrator = system
    prompt = "i want to make a knife"
    spec = NLPTranslationLayer.parse_layman_prompt(prompt)
    res = orchestrator.generate_recommendation(prompt, spec, prompt, [])
    top = res["ranked_materials"][0]["key"]
    assert top in ["Alloy_Steel_4140", "Stainless_Steel_316L"], f"Expected hardened steel for knife, got {top}"


def test_layman_shoe_sole_and_rubber(system):
    rag, orchestrator = system
    for prompt in ["a shoe sole", "something flexible like rubber"]:
        spec = NLPTranslationLayer.parse_layman_prompt(prompt)
        res = orchestrator.generate_recommendation(prompt, spec, prompt, [])
        top = res["ranked_materials"][0]["key"]
        assert top == "TPU_95A", f"Expected TPU 95A for '{prompt}', got {top}"


def test_layman_cooking_pan_heat_conduction(system):
    rag, orchestrator = system
    prompt = "a cooking pan"
    spec = NLPTranslationLayer.parse_layman_prompt(prompt)
    res = orchestrator.generate_recommendation(prompt, spec, prompt, [])
    top = res["ranked_materials"][0]["key"]
    assert top in ["Copper_C11000", "Aluminium_6061_T6"], f"Expected conductive metal for cookware, got {top}"


def test_layman_toy_and_prototyping_safety(system):
    rag, orchestrator = system
    for prompt in ["a toy car for my kid", "something cheap to test a model"]:
        spec = NLPTranslationLayer.parse_layman_prompt(prompt)
        res = orchestrator.generate_recommendation(prompt, spec, prompt, [])
        top = res["ranked_materials"][0]["key"]
        assert top in ["PLA", "PETG"], f"Expected non-toxic PLA/PETG for '{prompt}', got {top}"


def test_layman_optical_transparency(system):
    rag, orchestrator = system
    prompt = "something that is clear like glass"
    spec = NLPTranslationLayer.parse_layman_prompt(prompt)
    res = orchestrator.generate_recommendation(prompt, spec, prompt, [])
    top = res["ranked_materials"][0]["key"]
    assert top in ["Polycarbonate", "PC"], f"Expected optical-grade Polycarbonate for clear glass, got {top}"


def test_layman_heatsink(system):
    rag, orchestrator = system
    prompt = "a heatsink for my computer"
    spec = NLPTranslationLayer.parse_layman_prompt(prompt)
    res = orchestrator.generate_recommendation(prompt, spec, prompt, [])
    top = res["ranked_materials"][0]["key"]
    assert top in ["Copper_C11000", "Aluminium_6061_T6"], f"Expected copper or aluminium for heatsink, got {top}"


def test_layman_roofing_weatherability(system):
    rag, orchestrator = system
    prompt = "something for my roof"
    spec = NLPTranslationLayer.parse_layman_prompt(prompt)
    res = orchestrator.generate_recommendation(prompt, spec, prompt, [])
    top = res["ranked_materials"][0]["key"]
    assert top in ["Aluminium_6061_T6", "ASA", "Stainless_Steel_316L"], f"Expected weatherable metal/polymer for roof, got {top}"


def test_layman_bicycle_frame(system):
    rag, orchestrator = system
    prompt = "a frame for a bicycle"
    spec = NLPTranslationLayer.parse_layman_prompt(prompt)
    res = orchestrator.generate_recommendation(prompt, spec, prompt, [])
    top = res["ranked_materials"][0]["key"]
    assert top in ["CFRP_Prepreg", "Titanium_Ti6Al4V", "Aluminium_6061_T6"], f"Expected frame material, got {top}"


def test_layman_answers_are_diverse_and_non_identical(system):
    rag, orchestrator = system
    prompts = [
        "i want to make a chair",
        "something for my roof",
        "i want to make a knife",
        "a water bottle",
        "a shoe sole",
        "a cooking pan",
        "a toy car for my kid",
        "something that is clear like glass",
        "a heatsink for my computer"
    ]
    top_picks = set()
    for p in prompts:
        spec = NLPTranslationLayer.parse_layman_prompt(p)
        res = orchestrator.generate_recommendation(p, spec, p, [])
        top_mat = res["ranked_materials"][0]["name"]
        top_picks.add(top_mat)

    assert len(top_picks) >= 5, f"Expected diverse material answers, but got only {len(top_picks)}: {top_picks}"
