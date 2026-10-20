"""
Capstone Academic Test Suite: Autonomous Material Selection RAG-LLM
Candidate: Mutuku Geoffrey Mulu (Admission No. F18/144332/2022)

Verifies:
1. Automotive aerodynamic spoiler material selection & strict Titanium elimination.
2. Wind turbine blade aerodynamic selection & PLA/metal elimination.
3. Machine learning intent classification accuracy & zero hardcoding verification.
4. Capstone river turbine benchmark inviolability (PETG-CF #1, PLA 28.4% water loss, epoxy smoothing).
5. Cross-domain recommendation diversity and non-repetition.
"""

import pytest
from src.nlp_parser import NLPTranslationLayer
from src.ashby_engine import rank_materials, AshbyIndex
from src.llm_orchestrator import LLMOrchestrator
from src.rag_engine import RAGEngine


@pytest.fixture(scope="module")
def shared_rag_and_orch():
    rag = RAGEngine()
    orch = LLMOrchestrator(mode=LLMOrchestrator.MODE_AUTONOMOUS_EXPERT)
    return rag, orch


def test_spoiler_material_selection(shared_rag_and_orch):
    """Verify car spoiler prompt selects lightweight composites/ASA and strictly rejects Titanium."""
    rag, orch = shared_rag_and_orch
    prompt = "I want to create a spoiler for a car that can withstand aerodynamic drag and sunlight"

    spec = NLPTranslationLayer.parse_layman_prompt(prompt)
    comp = spec["synthesized_engineering_spec"]["component_classification"]
    assert comp == "automotive_aerodynamic_wing_or_spoiler"

    rag_prompt = rag.build_augmented_prompt(prompt, spec)
    retrieved = rag.query(prompt, top_k=3)
    res = orch.generate_recommendation(prompt, spec, rag_prompt, retrieved)

    ranked = res["ranked_materials"]
    top_mat = ranked[0]["name"]

    # Top material must be a lightweight structural composite or weatherable polymer
    assert any(valid in top_mat for valid in ["CFRP", "Continuous", "PA12-CF", "PETG-CF", "ASA", "ABS"])

    # Titanium must be heavily penalized and not in the top 3
    top_3_names = [m["name"] for m in ranked[:3]]
    assert not any("Titanium" in name for name in top_3_names)

    # Synthesis must articulate polar moment of inertia and rejection of dense metals
    synth = res["synthesized_response"]
    assert "polar moment of inertia" in synth.lower() or "downforce" in synth.lower()
    assert "Titanium" in synth
    assert "g/cm³" in synth or "g/cm" in synth


def test_wind_turbine_blade_selection(shared_rag_and_orch):
    """Verify wind turbine blade prompt selects composites and rejects virgin PLA and monolithic heavy metals."""
    rag, orch = shared_rag_and_orch
    prompt = "I need to make blades for a wind turbine"

    spec = NLPTranslationLayer.parse_layman_prompt(prompt)
    comp = spec["synthesized_engineering_spec"]["component_classification"]
    assert comp == "wind_turbine_blade"

    rag_prompt = rag.build_augmented_prompt(prompt, spec)
    retrieved = rag.query(prompt, top_k=3)
    res = orch.generate_recommendation(prompt, spec, rag_prompt, retrieved)

    ranked = res["ranked_materials"]
    top_mat = ranked[0]["name"]

    # Top material must be a high-stiffness composite
    assert any(valid in top_mat for valid in ["PA12-CF", "PETG-CF", "Carbon Fiber", "ASA"])

    # Virgin PLA and heavy metals must not be #1
    assert "Polylactic Acid" not in top_mat
    assert "Titanium" not in top_mat
    assert "Steel" not in top_mat

    synth = res["synthesized_response"]
    assert "wind turbine" in synth.lower()
    assert "fatigue" in synth.lower()


def test_machine_learning_intent_model():
    """Verify trained ML intent model executes and predicts correct component categories."""
    model = NLPTranslationLayer.get_ml_intent_model()
    assert model is not None
    assert hasattr(model, "vectorizer")
    assert hasattr(model, "comp_model")
    assert hasattr(model, "ashby_model")
    assert len(model.vectorizer.vocabulary) > 100

    test_queries = [
        ("aerodynamic rear spoiler for sports car", "automotive_aerodynamic_wing_or_spoiler"),
        ("blades for a wind turbine generator", "wind_turbine_blade"),
        ("submerged river hydrokinetic turbine runner", "turbine_blade_or_impeller"),
        ("chef knife for cutting meat", "cutting_tool_or_blade"),
        ("heat sink for computer cpu", "thermal_heat_sink"),
        ("lightweight bicycle frame", "bicycle_frame_or_chassis"),
        ("biocompatible hip implant joint", "biocompatible_orthopedic_implant"),
        ("frying pan base for cooking", "culinary_cookware")
    ]

    for q, expected in test_queries:
        pred_dict = NLPTranslationLayer.predict_ml_intent(q)
        pred_comp = pred_dict["component_classification"]
        assert pred_comp == expected, f"Query '{q}' predicted '{pred_comp}', expected '{expected}'"


def test_river_turbine_capstone_benchmark_inviolability(shared_rag_and_orch):
    """Verify that the primary 5th-year river turbine benchmark remains 100% intact."""
    rag, orch = shared_rag_and_orch
    prompt = "I need to 3D print a hydrokinetic river turbine blade submerged in flowing river water"

    spec = NLPTranslationLayer.parse_layman_prompt(prompt)
    rag_prompt = rag.build_augmented_prompt(prompt, spec)
    retrieved = rag.query(prompt, top_k=3)
    res = orch.generate_recommendation(prompt, spec, rag_prompt, retrieved)

    ranked = res["ranked_materials"]
    assert "PETG-CF" in ranked[0]["name"], "PETG-CF must be #1 for submerged river turbine"

    synth = res["synthesized_response"]
    assert "28.4%" in synth, "Must cite 28.4% PLA water saturation strength loss"
    assert "XTC-3D" in synth, "Must specify XTC-3D epoxy surface smoothing"
    assert "hardened steel" in synth.lower() or "ruby nozzle" in synth.lower(), "Must specify hardened steel or ruby nozzle for abrasive CF"


def test_diversity_and_non_repetition(shared_rag_and_orch):
    """Verify that different physical domains generate diverse, distinct materials and rationales."""
    rag, orch = shared_rag_and_orch

    prompts = [
        "car spoiler for downforce",
        "wind turbine blade",
        "butcher knife for meat",
        "soft protective phone case",
        "aluminum heat sink for cpu",
        "lightweight racing bicycle frame",
        "titanium hip replacement implant",
        "thermal cooking pan base",
        "cheap prototype toy figurine",
        "heavy duty crane hoist hook"
    ]

    top_materials = []
    top_indices = []

    for p in prompts:
        spec = NLPTranslationLayer.parse_layman_prompt(p)
        top_indices.append(spec["synthesized_engineering_spec"]["primary_governing_ashby_index"])
        rag_prompt = rag.build_augmented_prompt(p, spec)
        retrieved = rag.query(p, top_k=3)
        res = orch.generate_recommendation(p, spec, rag_prompt, retrieved)
        top_materials.append(res["ranked_materials"][0]["name"])

    # Across 10 diverse mechanical applications, there must be at least 5 different top materials
    unique_materials = set(top_materials)
    assert len(unique_materials) >= 5, f"Too many repeated materials: {unique_materials}"

    # There must be at least 4 different Ashby indices used
    unique_indices = set(top_indices)
    assert len(unique_indices) >= 4, f"Insufficient Ashby index diversity: {unique_indices}"
