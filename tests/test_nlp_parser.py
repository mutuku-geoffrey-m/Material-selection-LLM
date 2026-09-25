"""
Unit tests for the Natural Language Translation Layer, intent parsing, and guardrail safeguards.
"""

import pytest
from src.nlp_parser import NLPTranslationLayer
from src.ashby_engine import AshbyIndex


def test_benchmark_capstone_prompt_parsing():
    """Verify parsing of the benchmark capstone prompt from the project specification."""
    prompt = "I want to make a blade that will push water, carry a heavy load, and sit in a river all day, but I don't know the exact weight."
    spec = NLPTranslationLayer.parse_layman_prompt(prompt)

    # 1. Structural intent
    assert spec["synthesized_engineering_spec"]["component_classification"] == "turbine_blade_or_impeller"
    assert spec["synthesized_engineering_spec"]["primary_governing_ashby_index"] == AshbyIndex.BEAM_STRENGTH

    # 2. Environmental translation
    boundary = spec["boundary_conditions_and_constraints"]
    assert boundary["submerged_aquatic_exposure"] is True
    assert boundary["hydrolysis_resistance_required"] is True
    assert boundary["water_saturation_penalty_active"] is True
    assert boundary["cyclical_fatigue_resistance_required"] is True

    # 3. Guardrails & ambiguity handling
    guardrails = spec["guardrail_flags"]
    assert guardrails["has_ambiguity"] is True
    assert any("Exact hydrodynamic load magnitude is unquantified" in a for a in guardrails["ambiguities_noted"])
    assert any("Reject PLA" in s for s in guardrails["hallucination_safeguards"])


def test_outdoor_solar_prompt_parsing():
    """Verify outdoor UV and solar mounting bracket intent parsing."""
    prompt = "I need a stiff mounting bracket for solar panels outside under strong sun in Kenya."
    spec = NLPTranslationLayer.parse_layman_prompt(prompt)

    boundary = spec["boundary_conditions_and_constraints"]
    assert boundary["outdoor_uv_exposure"] is True
    assert boundary["submerged_aquatic_exposure"] is False
    assert spec["synthesized_engineering_spec"]["component_classification"] == "structural_cantilever_beam"


def test_flywheel_prompt_parsing():
    """Verify rotational kinetic energy storage intent parsing."""
    prompt = "Designing a flywheel rotor to store rotational energy without bursting at high speeds."
    spec = NLPTranslationLayer.parse_layman_prompt(prompt)

    assert spec["synthesized_engineering_spec"]["primary_governing_ashby_index"] == AshbyIndex.FLYWHEEL_INERTIA


def test_numerical_extraction_from_prompt():
    """Verify extraction of numerical engineering values if specified by user."""
    prompt = "Turbine blade chord 220 mm operating in river flow of 3.2 m/s."
    spec = NLPTranslationLayer.parse_layman_prompt(prompt)

    assert spec["numerical_parameters"]["estimated_chord_m"] == pytest.approx(0.22, 0.01)
    assert spec["numerical_parameters"]["estimated_flow_velocity_ms"] == pytest.approx(3.2, 0.01)


def test_impeller_benchmark_prompt_fatigue_parsing():
    """Verify that 'impeller' triggers cyclical fatigue resistance even without explicit 'push water' phrase."""
    prompt = "I want to make an impeller that will carry a heavy load in a river, but I do not know the exact weight."
    spec = NLPTranslationLayer.parse_layman_prompt(prompt)

    boundary = spec["boundary_conditions_and_constraints"]
    assert boundary["cyclical_fatigue_resistance_required"] is True, "Rotating impellers must trigger cyclic fatigue"
    assert boundary["submerged_aquatic_exposure"] is True
    assert boundary["water_saturation_penalty_active"] is True


def test_temperature_and_cryogenic_parsing():
    """Verify numerical temperature extraction and cryogenic flag detection."""
    prompt_hot = "I need a manifold nozzle operating at 350 C continuous heat."
    spec_hot = NLPTranslationLayer.parse_layman_prompt(prompt_hot)
    assert spec_hot["boundary_conditions_and_constraints"]["high_temperature_threshold"] is True
    assert spec_hot["numerical_parameters"]["target_service_temperature_c"] == pytest.approx(350.0, 0.1)

    prompt_cryo = "Cryogenic pump casing operating at -196 C in liquid nitrogen."
    spec_cryo = NLPTranslationLayer.parse_layman_prompt(prompt_cryo)
    assert spec_cryo["boundary_conditions_and_constraints"]["is_cryogenic"] is True


def test_explicit_subtractive_cnc_parsing():
    """Verify that requests for CNC milling select Conventional Subtractive machining route."""
    prompt = "I want to CNC mill a heavy duty steel impeller for high pressure water."
    spec = NLPTranslationLayer.parse_layman_prompt(prompt)
    assert spec["boundary_conditions_and_constraints"]["manufacturing_process"] == "Conventional Subtractive/Machining"


def test_dynamic_formula_accuracy():
    """Verify mathematical formula string reflects actual governing index without false E^(1/2)/rho defaults."""
    spec_flywheel = NLPTranslationLayer.parse_layman_prompt("Flywheel kinetic energy rotor spinning at high RPM")
    assert spec_flywheel["synthesized_engineering_spec"]["ashby_mathematical_formula"] == "σ_y / ρ"

    spec_skin = NLPTranslationLayer.parse_layman_prompt("Blade exterior skin panel deflection")
    assert spec_skin["synthesized_engineering_spec"]["ashby_mathematical_formula"] == "E^(1/3) / ρ"


def test_no_river_assumptions_for_solar_bracket():
    """Verify guardrails do NOT inject micro-hydro river assumptions into non-submerged components."""
    prompt = "Design an outdoor solar tracker mounting bracket for equatorial sun in Garissa Kenya."
    spec = NLPTranslationLayer.parse_layman_prompt(prompt)
    ambiguities = spec["guardrail_flags"]["ambiguities_noted"]
    assert not any("Kenyan river flow" in a for a in ambiguities), "Solar bracket must not assume river flow"
    assert not any("micro-hydro baseline" in a for a in ambiguities), "Solar bracket must not assume turbine chord"

