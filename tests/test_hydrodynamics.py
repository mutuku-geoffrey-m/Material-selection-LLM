"""
Unit tests for hydrodynamic boundary layer physics, Reynolds number regimes, and epoxy post-processing.
"""

import pytest
from src.hydrodynamics import HydrodynamicsEngine


def test_reynolds_number_calculation():
    """Verify Reynolds number calculation in freshwater river flows."""
    # u = 2.4 m/s, c = 0.18 m, nu = 1.004e-6 m^2/s
    # Re = 2.4 * 0.18 / 1.004e-6 = 430,278
    re_c = HydrodynamicsEngine.calculate_reynolds_number(0.18, 2.4)
    assert re_c == pytest.approx(430278, rel=1e-2)

    # High flow river runner: u = 3.5 m/s, c = 0.30 m
    # Re = 3.5 * 0.30 / 1.004e-6 = 1,045,816 (~1.05e6)
    re_high = HydrodynamicsEngine.calculate_reynolds_number(0.30, 3.5)
    assert 8e5 <= re_high <= 4.8e6, "Must fall within typical capstone turbine Reynolds envelope"


def test_roughness_drag_penalty_uncoated():
    """Verify that raw FDM surface roughness induces up to a 40% lift-to-drag penalty."""
    analysis = HydrodynamicsEngine.analyze_blade_hydrodynamics(
        chord_m=0.18,
        blade_span_m=0.45,
        flow_velocity_m_s=2.4,
        as_printed_ra_microns=22.0,
        is_epoxy_coated=False
    )

    assert analysis["drag_penalty_percent"] > 0.0
    assert analysis["drag_penalty_percent"] <= 40.0
    assert "Premature laminar-to-turbulent" in analysis["boundary_layer_state"]
    assert analysis["epoxy_post_processing_directive"]["status"] == "MANDATORY_SURFACE_TREATMENT_REQUIRED"


def test_epoxy_coated_drag_penalty_elimination():
    """Verify that applying epoxy sealant eliminates the hydrodynamic drag penalty."""
    analysis = HydrodynamicsEngine.analyze_blade_hydrodynamics(
        chord_m=0.18,
        blade_span_m=0.45,
        flow_velocity_m_s=2.4,
        as_printed_ra_microns=22.0,
        is_epoxy_coated=True
    )

    assert analysis["drag_penalty_percent"] == 0.0
    assert analysis["effective_roughness_ra_microns"] < 1.5
    assert "Hydraulically Smooth" in analysis["hydraulic_regime"]
    assert analysis["epoxy_post_processing_directive"]["status"] == "COMPLIANT"
