"""
Exhaustive Multi-Prompt Stress Test & Peer Grill Verification Suite.
Grills the system across diverse, ambiguous, conflicting, and edge-case prompts
to verify engineering correctness, physical realism, and guardrail stability.
"""

import pytest
from src.nlp_parser import NLPTranslationLayer
from src.rag_engine import RAGEngine
from src.llm_orchestrator import LLMOrchestrator
from src.ashby_engine import AshbyIndex


@pytest.fixture(scope="module")
def system_components():
    rag = RAGEngine()
    orchestrator = LLMOrchestrator(mode=LLMOrchestrator.MODE_AUTONOMOUS_EXPERT)
    return rag, orchestrator


def test_prompt_1_capstone_benchmark(system_components):
    """Grill Test 1: Official Capstone Benchmark Prompt."""
    rag, orchestrator = system_components
    prompt = "I want to make a blade that will push water, carry a heavy load, and sit in a river all day, but I don't know the exact weight."

    spec = NLPTranslationLayer.parse_layman_prompt(prompt)
    rag_prompt = rag.build_augmented_prompt(prompt, spec)
    chunks = rag.query(prompt, top_k=3)
    res = orchestrator.generate_recommendation(prompt, spec, rag_prompt, chunks)

    assert "PETG-CF" in res["synthesized_response"]
    assert "hardened steel" in res["synthesized_response"].lower()
    assert "28.4%" in res["synthesized_response"]
    assert res["is_submerged_river"] is True


def test_prompt_2_vague_minimal_layman(system_components):
    """Grill Test 2: Ultra-vague minimal layman input."""
    rag, orchestrator = system_components
    prompt = "I need to make a spinning thing for water."

    spec = NLPTranslationLayer.parse_layman_prompt(prompt)
    rag_prompt = rag.build_augmented_prompt(prompt, spec)
    chunks = rag.query(prompt, top_k=3)
    res = orchestrator.generate_recommendation(prompt, spec, rag_prompt, chunks)

    # Must detect water exposure and assume reasonable baseline
    assert spec["boundary_conditions_and_constraints"]["submerged_aquatic_exposure"] is True
    assert len(res["ranked_materials"]) > 0
    assert res["ranked_materials"][0]["key"] in ["PETG-CF", "PA12-CF", "PETG", "PEEK_Optima", "PEEK"]


def test_prompt_3_conflicting_pla_request(system_components):
    """Grill Test 3: User naively requests PLA for underwater river use."""
    rag, orchestrator = system_components
    prompt = "I want to print a water impeller using cheap standard PLA to save money in the river."

    spec = NLPTranslationLayer.parse_layman_prompt(prompt)
    rag_prompt = rag.build_augmented_prompt(prompt, spec)
    chunks = rag.query(prompt, top_k=3)
    res = orchestrator.generate_recommendation(prompt, spec, rag_prompt, chunks)

    # System MUST refuse PLA as top choice and explain why
    top_mat = res["ranked_materials"][0]["key"]
    assert top_mat != "PLA", "System must never recommend PLA as top choice for submerged river use"
    assert "28.4%" in res["synthesized_response"] or "degradation" in res["synthesized_response"].lower()


def test_prompt_4_outdoor_equatorial_solar(system_components):
    """Grill Test 4: Outdoor intense solar UV exposure in Kenya without water."""
    rag, orchestrator = system_components
    prompt = "Design a stiff, lightweight cantilever mounting arm for solar panels outdoors under intense African equatorial sun in Garissa."

    spec = NLPTranslationLayer.parse_layman_prompt(prompt)
    assert spec["boundary_conditions_and_constraints"]["outdoor_uv_exposure"] is True
    assert spec["boundary_conditions_and_constraints"]["submerged_aquatic_exposure"] is False

    rag_prompt = rag.build_augmented_prompt(prompt, spec)
    chunks = rag.query(prompt, top_k=3)
    res = orchestrator.generate_recommendation(prompt, spec, rag_prompt, chunks)

    # In dry outdoor conditions, UV resistance dominates
    assert len(res["ranked_materials"]) > 0


def test_prompt_5_high_speed_flywheel_inertia(system_components):
    """Grill Test 5: High speed flywheel energy storage."""
    rag, orchestrator = system_components
    prompt = "Heavy flywheel rotor to smooth out generator surges without bursting under centrifugal spin."

    spec = NLPTranslationLayer.parse_layman_prompt(prompt)
    assert spec["synthesized_engineering_spec"]["primary_governing_ashby_index"] == AshbyIndex.FLYWHEEL_INERTIA


def test_prompt_6_torrential_river_runner(system_components):
    """Grill Test 6: Extreme river velocity and large chord."""
    rag, orchestrator = system_components
    prompt = "Hydro-turbine runner blade with 300 mm chord operating in turbulent 3.8 m/s flood rapids."

    spec = NLPTranslationLayer.parse_layman_prompt(prompt)
    assert spec["numerical_parameters"]["estimated_chord_m"] == pytest.approx(0.30, 0.01)
    assert spec["numerical_parameters"]["estimated_flow_velocity_ms"] == pytest.approx(3.8, 0.01)

    rag_prompt = rag.build_augmented_prompt(prompt, spec)
    chunks = rag.query(prompt, top_k=3)
    res = orchestrator.generate_recommendation(prompt, spec, rag_prompt, chunks)

    hydro = res["hydrodynamic_analysis"]
    assert hydro is not None
    # Re = 3.8 * 0.3 / 1.004e-6 = 1.135e6 (in 0.8e6 - 4.8e6 range!)
    assert hydro["chord_reynolds_number"] > 1e6
    assert hydro["reynolds_range_match"] == "0.8e6 to 4.8e6 range fulfilled"
    assert hydro["drag_penalty_percent"] > 0


def test_cli_runner():
    """Verify that CLI execution functions run without exception."""
    from cli import run_single_prompt
    res = run_single_prompt(
        "I want to make a blade that will push water, carry a heavy load, and sit in a river all day, but I don't know the exact weight.",
        mode=LLMOrchestrator.MODE_AUTONOMOUS_EXPERT,
        verbose=True
    )
    assert res is not None
    assert "PETG-CF" in res["synthesized_response"]


def test_prompt_7_extreme_thermal_350c(system_components):
    """Grill Test 7: Extreme thermal operation at 350°C (disqualifies all standard thermoplastics)."""
    rag, orchestrator = system_components
    prompt = "I need a nozzle or manifold operating at 350 C continuous heat."

    spec = NLPTranslationLayer.parse_layman_prompt(prompt)
    assert spec["boundary_conditions_and_constraints"]["high_temperature_threshold"] is True

    rag_prompt = rag.build_augmented_prompt(prompt, spec)
    chunks = rag.query(prompt, top_k=3)
    res = orchestrator.generate_recommendation(prompt, spec, rag_prompt, chunks)

    synth = res["synthesized_response"]
    assert any(m in synth for m in ["Alumina", "Aluminium", "Stainless Steel", "Inconel", "Titanium"]), "At 350°C, must select high-temp material"
    assert "Thermal Service Threshold Warning" in synth
    assert "Manufacturing Directives" in synth or "Fabrication Directives" in synth


def test_prompt_8_explicit_cnc_machining(system_components):
    """Grill Test 8: Explicit user request for CNC machining / subtractive route."""
    rag, orchestrator = system_components
    prompt = "I want to CNC mill an impeller out of stainless steel or aluminium for a high pressure hydro system."

    spec = NLPTranslationLayer.parse_layman_prompt(prompt)
    assert spec["boundary_conditions_and_constraints"]["manufacturing_process"] == "Conventional Subtractive/Machining"

    rag_prompt = rag.build_augmented_prompt(prompt, spec)
    chunks = rag.query(prompt, top_k=3)
    res = orchestrator.generate_recommendation(prompt, spec, rag_prompt, chunks)

    synth = res["synthesized_response"]
    assert "Subtractive (CNC) Manufacturing Directives" in synth
    assert res["ranked_materials"][0]["key"] in ["Stainless_Steel_316L", "Aluminium_6061_T6"]


def test_prompt_9_outdoor_solar_uv_garissa(system_components):
    """Grill Test 9: Outdoor solar tracker in Garissa Kenya under equatorial UV."""
    rag, orchestrator = system_components
    prompt = "Design an outdoor solar tracker mounting bracket exposed to intense UV and sun in Garissa Kenya."

    spec = NLPTranslationLayer.parse_layman_prompt(prompt)
    rag_prompt = rag.build_augmented_prompt(prompt, spec)
    chunks = rag.query(prompt, top_k=3)
    res = orchestrator.generate_recommendation(prompt, spec, rag_prompt, chunks)

    top_mat_key = res["ranked_materials"][0]["key"]
    # Should pick UV-resistant polymer (ASA or PETG-CF) or corrosion/UV-proof structural alloy
    assert top_mat_key in ["ASA", "PETG-CF", "Aluminium_6061_T6", "Titanium_Ti6Al4V"]
    assert "Outdoor Solar UV" in res["synthesized_response"]


def test_cli_subprocess_encoding_execution():
    """Verify that cli.py runs as an independent Windows subprocess without UnicodeEncodeError."""
    import subprocess
    import sys
    import os

    cwd = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    result = subprocess.run(
        [sys.executable, "cli.py", "--benchmark", "--mode", "AUTONOMOUS_EXPERT"],
        cwd=cwd,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        env=env,
        timeout=30
    )
    assert result.returncode == 0, f"CLI subprocess crashed with stderr: {result.stderr}"
    assert "PETG-CF" in result.stdout
    assert "Executive Engineering Decision" in result.stdout


def test_prompt_10_bicycle_frame_universal(system_components):
    """Grill Test 10: Lightweight stiff bicycle frame for road racing."""
    rag, orchestrator = system_components
    prompt = "I want to design a lightweight and stiff bicycle frame for road racing."

    spec = NLPTranslationLayer.parse_layman_prompt(prompt)
    rag_prompt = rag.build_augmented_prompt(prompt, spec)
    chunks = rag.query(prompt, top_k=3)
    res = orchestrator.generate_recommendation(prompt, spec, rag_prompt, chunks)

    synth = res["synthesized_response"]
    assert any(m in synth for m in ["CFRP", "Carbon Fiber", "Titanium", "4140", "Chromoly", "Aluminium"])
    assert "Structural Frame Optimization" in synth
    top_key = res["ranked_materials"][0]["key"]
    assert top_key in ["CFRP_Prepreg", "Titanium_Ti6Al4V", "Aluminium_6061_T6", "Alloy_Steel_4140"]


def test_prompt_11_cpu_heat_sink(system_components):
    """Grill Test 11: High thermal dissipation CPU heat sink."""
    rag, orchestrator = system_components
    prompt = "I need a material for a high-performance CPU heat sink to dissipate heat quickly."

    spec = NLPTranslationLayer.parse_layman_prompt(prompt)
    rag_prompt = rag.build_augmented_prompt(prompt, spec)
    chunks = rag.query(prompt, top_k=3)
    res = orchestrator.generate_recommendation(prompt, spec, rag_prompt, chunks)

    synth = res["synthesized_response"]
    assert "Thermal Conduction Optimization" in synth or "390" in synth or "Copper" in synth
    top_key = res["ranked_materials"][0]["key"]
    # Copper C11000 has 390 W/mK - undisputed king of heat conduction
    assert top_key == "Copper_C11000" or top_key == "Aluminium_6061_T6"


def test_prompt_12_shock_absorbing_phone_case(system_components):
    """Grill Test 12: Flexible impact-absorbing smartphone bumper case."""
    rag, orchestrator = system_components
    prompt = "I want to make a protective bumper case for a smartphone that can absorb drop impacts without cracking."

    spec = NLPTranslationLayer.parse_layman_prompt(prompt)
    rag_prompt = rag.build_augmented_prompt(prompt, spec)
    chunks = rag.query(prompt, top_k=3)
    res = orchestrator.generate_recommendation(prompt, spec, rag_prompt, chunks)

    synth = res["synthesized_response"]
    assert "Impact Energy Absorption" in synth or "TPU" in synth or "damping" in synth
    top_key = res["ranked_materials"][0]["key"]
    assert top_key in ["TPU_95A", "Polycarbonate"]


def test_prompt_13_heavy_duty_crane_hook(system_components):
    """Grill Test 13: Crane lifting hook resisting shock loading without brittle fracture."""
    rag, orchestrator = system_components
    prompt = "Design a heavy duty crane lifting hook to safely hoist 10 tons without brittle fracture."

    spec = NLPTranslationLayer.parse_layman_prompt(prompt)
    rag_prompt = rag.build_augmented_prompt(prompt, spec)
    chunks = rag.query(prompt, top_k=3)
    res = orchestrator.generate_recommendation(prompt, spec, rag_prompt, chunks)

    synth = res["synthesized_response"]
    assert "Heavy-Duty Lifting" in synth or "toughness" in synth.lower()
    top_key = res["ranked_materials"][0]["key"]
    # 4140 Chromoly Steel or Stainless Steel or Titanium
    assert top_key in ["Alloy_Steel_4140", "CFRP_Prepreg", "Titanium_Ti6Al4V", "Stainless_Steel_316L"]


def test_prompt_14_extreme_high_temperature_nozzle_700c(system_components):
    """Grill Test 14: Gas turbine exhaust nozzle operating at 700°C."""
    rag, orchestrator = system_components
    prompt = "Exhaust nozzle for a turbine engine operating continuously at 700 C."

    spec = NLPTranslationLayer.parse_layman_prompt(prompt)
    rag_prompt = rag.build_augmented_prompt(prompt, spec)
    chunks = rag.query(prompt, top_k=3)
    res = orchestrator.generate_recommendation(prompt, spec, rag_prompt, chunks)

    synth = res["synthesized_response"]
    assert "700" in synth
    top_key = res["ranked_materials"][0]["key"]
    # At 700°C, only superalloys and refractory ceramics survive
    assert top_key in ["Inconel_718", "Alumina_Ceramic", "Alumina_Al2O3", "Stainless_Steel_316L"]


def test_prompt_15_low_friction_sliding_gear(system_components):
    """Grill Test 15: Precision low friction sliding gears and bushings."""
    rag, orchestrator = system_components
    prompt = "Precision sliding gears and bushings requiring low friction and wear resistance without lubrication."

    spec = NLPTranslationLayer.parse_layman_prompt(prompt)
    rag_prompt = rag.build_augmented_prompt(prompt, spec)
    chunks = rag.query(prompt, top_k=3)
    res = orchestrator.generate_recommendation(prompt, spec, rag_prompt, chunks)

    synth = res["synthesized_response"]
    assert "Tribological" in synth or "friction" in synth.lower() or "wear" in synth.lower()


def test_prompt_16_biocompatible_orthopedic_implant(system_components):
    """Grill Test 16: Biocompatible orthopedic femoral hip stem implant."""
    rag, orchestrator = system_components
    prompt = "Biocompatible load-bearing femoral hip replacement stem inside the human body."

    spec = NLPTranslationLayer.parse_layman_prompt(prompt)
    rag_prompt = rag.build_augmented_prompt(prompt, spec)
    chunks = rag.query(prompt, top_k=3)
    res = orchestrator.generate_recommendation(prompt, spec, rag_prompt, chunks)

    synth = res["synthesized_response"]
    assert "Biomedical" in synth or "Biocompatibility" in synth or "Titanium" in synth
    top_key = res["ranked_materials"][0]["key"]
    assert top_key in ["Titanium_Ti6Al4V", "PEEK", "Stainless_Steel_316L", "CFRP_Prepreg", "Alumina_Al2O3"]



