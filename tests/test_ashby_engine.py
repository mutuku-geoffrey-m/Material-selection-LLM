"""
Unit tests for Ashby optimization methodology, performance index mathematics, and material ranking.
"""

import pytest
import math
from src.ashby_engine import (
    AshbyIndex,
    calculate_ashby_index,
    rank_materials,
    derive_selection_guide,
    INDEX_DESCRIPTIONS
)
from src.materials_db import get_material


def test_ashby_beam_stiffness_calculation():
    """Verify analytical formula M = E^(1/2) / rho."""
    petg_cf = get_material("PETG-CF")
    e_gpa = petg_cf["youngs_modulus_print_xy"]
    rho_kg_m3 = petg_cf["density"]
    expected_m = math.sqrt(e_gpa) / (rho_kg_m3 / 1000.0)

    computed_m = calculate_ashby_index(petg_cf, AshbyIndex.BEAM_STIFFNESS)
    assert computed_m == pytest.approx(expected_m, rel=1e-4)


def test_ashby_beam_strength_calculation():
    """Verify analytical formula M = sigma_y^(2/3) / rho."""
    petg_cf = get_material("PETG-CF")
    sigma_y = petg_cf["yield_strength"]
    rho_kg_m3 = petg_cf["density"]
    expected_m = (sigma_y ** (2.0 / 3.0)) / (rho_kg_m3 / 1000.0)

    computed_m = calculate_ashby_index(petg_cf, AshbyIndex.BEAM_STRENGTH)
    assert computed_m == pytest.approx(expected_m, rel=1e-4)


def test_ashby_flywheel_inertia_calculation():
    """Verify flywheel kinetic energy index M = sigma_y / rho."""
    abs_mat = get_material("ABS")
    expected_m = abs_mat["yield_strength"] / (abs_mat["density"] / 1000.0)
    computed_m = calculate_ashby_index(abs_mat, AshbyIndex.FLYWHEEL_INERTIA)
    assert computed_m == pytest.approx(expected_m, rel=1e-4)


def test_ranking_petg_cf_outperforms_in_water():
    """Verify that in water-saturated conditions, PETG-CF dominates PLA due to PLA degradation."""
    # Rank materials for beam strength with water degradation active
    ranked = rank_materials(
        index_key=AshbyIndex.BEAM_STRENGTH,
        fdm_only=True,
        water_degradation_adjusted=True
    )

    # Top candidate should be high-performance composite or engineering polymer (PETG-CF, PA12-CF, PEEK)
    top_keys = [r["key"] for r in ranked[:4]]
    assert any(k in top_keys for k in ["PETG-CF", "PA12-CF", "PEEK", "PEEK_Optima"])

    # Find PLA and PETG-CF scores
    pla_score = [r["final_metric"] for r in ranked if r["key"] == "PLA"][0]
    petg_cf_score = [r["final_metric"] for r in ranked if r["key"] == "PETG-CF"][0]

    assert petg_cf_score > pla_score, "PETG-CF must rank higher than degraded PLA under river conditions"


def test_derive_selection_guide():
    """Verify natural language intent mapping to correct Ashby indices."""
    guide_blade = derive_selection_guide("I want to design a turbine blade carrying a heavy hydrodynamic load in a river")
    assert guide_blade["index_key"] == AshbyIndex.BEAM_STRENGTH

    guide_spar = derive_selection_guide("We need a stiff beam with minimum bending deflection")
    assert guide_spar["index_key"] == AshbyIndex.BEAM_STIFFNESS

    guide_flywheel = derive_selection_guide("A high speed flywheel to store rotational kinetic energy without bursting")
    assert guide_flywheel["index_key"] == AshbyIndex.FLYWHEEL_INERTIA

    guide_skin = derive_selection_guide("Thin outer plate shell skin to resist water pressure")
    assert guide_skin["index_key"] == AshbyIndex.PLATE_STIFFNESS

    # Verify no shadowing when 'blade' is mentioned alongside 'shell' or 'skin'
    guide_blade_skin = derive_selection_guide("Thin outer blade shell skin to resist water pressure")
    assert guide_blade_skin["index_key"] == AshbyIndex.PLATE_STIFFNESS


def test_rank_materials_high_temperature_disqualification():
    """Verify that operating temperatures > 150°C disqualify thermoplastics and prioritize metals."""
    ranked = rank_materials(
        index_key=AshbyIndex.BEAM_STIFFNESS,
        fdm_only=False,
        max_service_temp_c=350.0
    )

    top_mat = ranked[0]
    high_temp_keys = ["Alumina_Al2O3", "Alumina_Ceramic", "Aluminium_6061_T6", "Stainless_Steel_316L", "Titanium_Ti6Al4V", "Inconel_718", "Alloy_Steel_4140"]
    assert top_mat["key"] in high_temp_keys, f"At 350°C, high-temp material must be recommended, got {top_mat['key']}"
    # Verify thermoplastics are flagged as thermally inviable
    pla = [r for r in ranked if r["key"] == "PLA"][0]
    assert pla["thermally_inviable"] is True


def test_rank_materials_uv_exposure_weighting():
    """Verify that outdoor UV exposure penalizes PLA/ABS and prioritizes ASA / PETG-CF."""
    ranked = rank_materials(
        index_key=AshbyIndex.BEAM_STIFFNESS,
        fdm_only=True,
        water_degradation_adjusted=False,
        uv_exposure_adjusted=True
    )

    asa_score = [r["final_metric"] for r in ranked if r["key"] == "ASA"][0]
    abs_score = [r["final_metric"] for r in ranked if r["key"] == "ABS"][0]
    assert asa_score > abs_score, "ASA must rank higher than ABS under outdoor UV exposure"


def test_rank_materials_water_fatigue_degradation():
    """Verify that fatigue limit is degraded in water-saturated conditions."""
    ranked_dry = rank_materials(
        index_key=AshbyIndex.FATIGUE_EFFICIENCY,
        fdm_only=True,
        water_degradation_adjusted=False
    )
    ranked_wet = rank_materials(
        index_key=AshbyIndex.FATIGUE_EFFICIENCY,
        fdm_only=True,
        water_degradation_adjusted=True
    )

    pla_dry = [r["raw_score"] for r in ranked_dry if r["key"] == "PLA"][0]
    pla_wet = [r["raw_score"] for r in ranked_wet if r["key"] == "PLA"][0]
    assert pla_wet < pla_dry, "PLA fatigue metric must degrade when water-saturated"

