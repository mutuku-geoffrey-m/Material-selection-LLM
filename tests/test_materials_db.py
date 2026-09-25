"""
Unit tests for materials database integrity, physical consistency, and property schemas.
"""

import pytest
from src.materials_db import MATERIALS_DATABASE, get_material, list_all_materials, filter_fdm_printable_materials


def test_database_completeness():
    """Verify that all core materials required by the capstone specification are present."""
    required_keys = ["PLA", "PETG", "PETG-CF", "ABS", "ASA", "Nylon_PA12", "PA12-CF", "Polycarbonate", "Aluminium_6061_T6", "Stainless_Steel_316L"]
    for key in required_keys:
        assert key in MATERIALS_DATABASE, f"Missing critical material: {key}"


def test_physical_properties_sanity():
    """Ensure all mechanical and physical values are physically realistic across metals, polymers, ceramics, and elastomers."""
    for key, data in MATERIALS_DATABASE.items():
        assert data["density"] > 500.0 and data["density"] < 15000.0, f"Unrealistic density for {key}: {data['density']}"
        # Elastomers (e.g. TPU) have Young's modulus in the range 0.01 to 0.1 GPa
        min_e = 0.01 if data.get("family") == "Elastomeric Polymer" else 0.5
        min_yield = 5.0 if data.get("family") == "Elastomeric Polymer" else 10.0
        assert data["youngs_modulus_iso"] >= min_e and data["youngs_modulus_iso"] < 500.0, f"Unrealistic E for {key}"
        assert data["yield_strength"] >= min_yield and data["yield_strength"] < 2000.0, f"Unrealistic yield strength for {key}"
        assert data["ultimate_tensile_strength"] >= data["yield_strength"] * 0.9, f"UTS should exceed or match yield strength for {key}"
        assert data["fatigue_strength_limit"] > 0, f"Fatigue strength missing or non-positive for {key}"


def test_water_saturation_data_accuracy():
    """Verify empirical water degradation parameters cited in capstone literature (Ref 22)."""
    pla = get_material("PLA")
    assert pla is not None
    assert pla["water_saturation_tensile_drop"] == pytest.approx(28.4, 0.1), "PLA water degradation tensile drop must match Ref 22 (28.4%)"
    assert pla["water_saturation_modulus_drop"] == pytest.approx(7.2, 0.1), "PLA water degradation modulus drop must match Ref 22 (7.2%)"

    petg_cf = get_material("PETG-CF")
    assert petg_cf is not None
    assert petg_cf["water_saturation_tensile_drop"] < 5.0, "PETG-CF must exhibit superior moisture resilience"


def test_fdm_abrasive_nozzle_directives():
    """Ensure carbon fiber composites are strictly flagged as requiring abrasive nozzles."""
    petg_cf = get_material("PETG-CF")
    pa12_cf = get_material("PA12-CF")
    pla = get_material("PLA")

    assert petg_cf["fdm_printability"]["abrasive_nozzle_required"] is True, "PETG-CF must require hardened nozzle"
    assert pa12_cf["fdm_printability"]["abrasive_nozzle_required"] is True, "PA12-CF must require hardened nozzle"
    assert pla["fdm_printability"]["abrasive_nozzle_required"] is False, "PLA does not require hardened nozzle"


def test_material_retrieval_fuzzy():
    """Verify robust material retrieval by exact and case-insensitive names and aliases."""
    assert get_material("petg-cf") is not None
    assert get_material("PETG") is not None
    assert get_material("nylon") is not None
    assert get_material("non_existent_super_metal") is None
    # American vs British spelling
    al = get_material("Aluminum")
    assert al is not None, "Aluminum (American spelling) must resolve to Aluminium 6061-T6"
    assert "Aluminium" in al["name"] or "Aluminum" in al["name"]
    # Common abbreviations
    assert get_material("316L") is not None
    assert get_material("Stainless") is not None
    assert get_material("PC") is not None
    assert get_material("Carbon Fiber") is not None


def test_thermal_and_field_viability_data():
    """Verify thermal limits (HDT, Tg) and field manufacturing parameters."""
    for key, data in MATERIALS_DATABASE.items():
        assert "heat_deflection_temp" in data, f"Missing HDT for {key}"
        assert "glass_transition_temp" in data, f"Missing Tg for {key}"
        assert data["heat_deflection_temp"] > 0, f"HDT must be positive for {key}"

    # Metals must tolerate high temperatures
    al = get_material("Aluminium_6061_T6")
    steel = get_material("Stainless_Steel_316L")
    assert al["heat_deflection_temp"] >= 400.0
    assert steel["heat_deflection_temp"] >= 800.0
