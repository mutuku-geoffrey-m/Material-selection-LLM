"""
Comprehensive Materials Database for Additive Manufacturing & Engineering Selection.
Contains mechanical, thermal, environmental, and FDM manufacturing properties,
including empirical degradation data (water saturation, UV exposure, fatigue).
"""

from typing import Dict, Any, List, Optional
import math

MATERIALS_DATABASE: Dict[str, Dict[str, Any]] = {
    "PLA": {
        "name": "Polylactic Acid (PLA)",
        "family": "Thermoplastic Polymer",
        "density": 1240.0,  # kg/m^3
        "youngs_modulus_iso": 3.5,  # GPa
        "youngs_modulus_print_xy": 3.4,  # GPa
        "youngs_modulus_print_z": 2.6,  # GPa (layer adhesion drop)
        "yield_strength": 55.0,  # MPa
        "ultimate_tensile_strength": 60.0,  # MPa
        "tensile_strength_z": 32.0,  # MPa
        "flexural_modulus": 3.8,  # GPa
        "flexural_strength": 85.0,  # MPa
        "elongation_at_break": 6.0,  # %
        "impact_strength_izod": 3.2,  # kJ/m^2 (notched)
        "fatigue_strength_limit": 18.0,  # MPa at 10^6 cycles (poor/brittle)
        "glass_transition_temp": 58.0,
        "melting_point_c": 175.0,  # °C
        "heat_deflection_temp": 52.0,  # °C at 0.45 MPa
        "thermal_conductivity": 0.13,  # W/(m·K)
        "specific_heat_capacity": 1800.0,  # J/(kg·K)
        "water_absorption_24h": 0.35,  # %
        "water_saturation_tensile_drop": 28.4,  # % degradation when water saturated (Ref 22)
        "water_saturation_modulus_drop": 7.2,  # % degradation when water saturated (Ref 22)
        "uv_resistance": "Poor",  # rapid embrittlement under outdoor UV
        "hydrolysis_resistance": "Poor",  # hydrolytic cleavage in submerged aquatic environments
        "chemical_resistance": "Fair",
        "fdm_printability": {
            "ease_of_printing": "Excellent",
            "nozzle_temperature_min": 190,
            "nozzle_temperature_max": 220,
            "bed_temperature_min": 45,
            "bed_temperature_max": 60,
            "enclosure_required": False,
            "warping_tendency": "Very Low",
            "abrasive_nozzle_required": False,
            "recommended_nozzle_type": "Standard Brass (0.4mm)",
            "layer_adhesion_quality": "High (isotropic ratio ~ 0.53)",
            "hygroscopic_sensitivity": "Low-Moderate",
            "filament_drying_temp": 45,  # °C
            "filament_drying_hours": 4
        },
        "surface_characteristics": {
            "as_printed_ra_microns": 15.0,  # typical 0.2mm layer Ra
            "porosity_risk": "Moderate",
            "water_permeability_untreated": "High (micro-voids allow deep ingress)"
        },
        "cost_per_kg_usd": 18.0,
        "kenya_availability": "Very High (widely stocked in Nairobi, Mombasa)",
        "suitability_summary": "Standard prototyping polymer. Excellent printability, but unacceptable for submerged micro-hydro due to 28.4% tensile loss in water, poor fatigue life, and UV degradation."
    },
    "PETG": {
        "name": "Polyethylene Terephthalate Glycol (PETG)",
        "family": "Thermoplastic Copolymer",
        "density": 1270.0,  # kg/m^3
        "youngs_modulus_iso": 2.1,  # GPa
        "youngs_modulus_print_xy": 2.1,  # GPa
        "youngs_modulus_print_z": 1.7,  # GPa
        "yield_strength": 45.0,  # MPa
        "ultimate_tensile_strength": 50.0,  # MPa
        "tensile_strength_z": 36.0,  # MPa (strong layer bonding)
        "flexural_modulus": 2.2,  # GPa
        "flexural_strength": 70.0,  # MPa
        "elongation_at_break": 18.0,  # % (ductile under shock loads)
        "impact_strength_izod": 7.5,  # kJ/m^2
        "fatigue_strength_limit": 24.0,  # MPa at 10^6 cycles
        "glass_transition_temp": 80.0,
        "melting_point_c": 225.0,  # °C
        "heat_deflection_temp": 70.0,  # °C at 0.45 MPa
        "thermal_conductivity": 0.19,  # W/(m·K)
        "specific_heat_capacity": 1300.0,  # J/(kg·K)
        "water_absorption_24h": 0.12,  # % (very low)
        "water_saturation_tensile_drop": 3.1,  # % minimal degradation in water
        "water_saturation_modulus_drop": 2.0,  # %
        "uv_resistance": "Good",
        "hydrolysis_resistance": "Good",
        "chemical_resistance": "Good (resistant to dilute acids, alkalis, oils)",
        "fdm_printability": {
            "ease_of_printing": "Good",
            "nozzle_temperature_min": 230,
            "nozzle_temperature_max": 250,
            "bed_temperature_min": 70,
            "bed_temperature_max": 85,
            "enclosure_required": False,
            "warping_tendency": "Low",
            "abrasive_nozzle_required": False,
            "recommended_nozzle_type": "Standard Brass or Hardened Steel (0.4mm)",
            "layer_adhesion_quality": "Very High (isotropic ratio ~ 0.72)",
            "hygroscopic_sensitivity": "Moderate",
            "filament_drying_temp": 65,  # °C
            "filament_drying_hours": 6
        },
        "surface_characteristics": {
            "as_printed_ra_microns": 16.5,
            "porosity_risk": "Low-Moderate (slight stringing)",
            "water_permeability_untreated": "Moderate"
        },
        "cost_per_kg_usd": 22.0,
        "kenya_availability": "High (stocked by local distributors in Kenya)",
        "suitability_summary": "Great moisture resistance and toughness. However, pure PETG exhibits high ductility and lower Young's modulus (2.1 GPa), leading to excessive blade deflection under heavy hydrodynamic river loads."
    },
    "PETG-CF": {
        "name": "Carbon Fiber Reinforced PETG (PETG-CF)",
        "family": "Short Fiber Reinforced Polymer Composite",
        "density": 1320.0,  # kg/m^3 (approx 15-20% chopped carbon fiber)
        "youngs_modulus_iso": 5.8,  # GPa (over 2.7x stiffer than neat PETG)
        "youngs_modulus_print_xy": 6.2,  # GPa (fiber alignment in extrusion direction)
        "youngs_modulus_print_z": 3.8,  # GPa
        "yield_strength": 52.0,  # MPa
        "ultimate_tensile_strength": 65.0,  # MPa
        "tensile_strength_z": 38.0,  # MPa
        "flexural_modulus": 5.9,  # GPa
        "flexural_strength": 98.0,  # MPa
        "elongation_at_break": 4.5,  # %
        "impact_strength_izod": 6.2,  # kJ/m^2
        "fatigue_strength_limit": 36.0,  # MPa at 10^6 cycles (high fatigue threshold)
        "glass_transition_temp": 82.0,
        "melting_point_c": 225.0,  # °C
        "heat_deflection_temp": 78.0,  # °C at 0.45 MPa
        "thermal_conductivity": 0.28,  # W/(m·K) (carbon fibers enhance thermal transfer)
        "specific_heat_capacity": 1250.0,  # J/(kg·K)
        "water_absorption_24h": 0.14,  # %
        "water_saturation_tensile_drop": 3.8,  # %
        "water_saturation_modulus_drop": 2.5,  # %
        "uv_resistance": "Excellent (carbon fibers shield base polymer from photolytic breakdown)",
        "hydrolysis_resistance": "Excellent",
        "chemical_resistance": "Good-Excellent",
        "fdm_printability": {
            "ease_of_printing": "Very Good (carbon fibers eliminate thermal contraction/warping)",
            "nozzle_temperature_min": 240,
            "nozzle_temperature_max": 265,
            "bed_temperature_min": 75,
            "bed_temperature_max": 85,
            "enclosure_required": False,
            "warping_tendency": "Very Low",
            "abrasive_nozzle_required": True,  # Critical engineering directive!
            "recommended_nozzle_type": "Hardened Steel or Tungsten Carbide (>= 0.4mm, 0.6mm preferred)",
            "layer_adhesion_quality": "High",
            "hygroscopic_sensitivity": "Moderate",
            "filament_drying_temp": 65,  # °C
            "filament_drying_hours": 6
        },
        "surface_characteristics": {
            "as_printed_ra_microns": 22.0,  # micro-texture from fiber extrusion increases boundary layer drag!
            "porosity_risk": "Moderate",
            "water_permeability_untreated": "Moderate (inter-bead voids present)"
        },
        "cost_per_kg_usd": 38.0,
        "kenya_availability": "Moderate-High (accessible through engineering suppliers & 3D hubs)",
        "suitability_summary": "OPTIMAL CHOICE for micro-hydro turbine blades. Combines PETG's hydrolytic resilience with carbon-fiber dimensional rigidity, high fatigue limit, and low creep. Requires hardened nozzle and mandatory epoxy post-processing for hydrodynamic smoothing."
    },
    "ABS": {
        "name": "Acrylonitrile Butadiene Styrene (ABS)",
        "family": "Thermoplastic Terpolymer",
        "density": 1050.0,  # kg/m^3
        "youngs_modulus_iso": 2.3,  # GPa
        "youngs_modulus_print_xy": 2.2,  # GPa
        "youngs_modulus_print_z": 1.4,  # GPa (notorious layer delamination)
        "yield_strength": 40.0,  # MPa
        "ultimate_tensile_strength": 44.0,  # MPa
        "tensile_strength_z": 22.0,  # MPa
        "flexural_modulus": 2.4,  # GPa
        "flexural_strength": 65.0,  # MPa
        "elongation_at_break": 12.0,  # %
        "impact_strength_izod": 15.0,  # kJ/m^2 (high impact toughness)
        "fatigue_strength_limit": 20.0,  # MPa
        "glass_transition_temp": 105.0,
        "melting_point_c": 220.0,  # °C
        "heat_deflection_temp": 95.0,  # °C at 0.45 MPa
        "thermal_conductivity": 0.17,  # W/(m·K)
        "specific_heat_capacity": 1400.0,  # J/(kg·K)
        "water_absorption_24h": 0.40,  # %
        "water_saturation_tensile_drop": 8.5,  # %
        "water_saturation_modulus_drop": 6.0,  # %
        "uv_resistance": "Poor (butadiene bonds degrade rapidly under sunlight)",
        "hydrolysis_resistance": "Moderate",
        "chemical_resistance": "Moderate (dissolves in acetone)",
        "fdm_printability": {
            "ease_of_printing": "Challenging",
            "nozzle_temperature_min": 235,
            "nozzle_temperature_max": 255,
            "bed_temperature_min": 95,
            "bed_temperature_max": 110,
            "enclosure_required": True,  # thermal chamber mandatory to avoid catastrophic corner lifting
            "warping_tendency": "High",
            "abrasive_nozzle_required": False,
            "recommended_nozzle_type": "Standard Brass (0.4mm)",
            "layer_adhesion_quality": "Moderate-Low (anisotropic weakness)",
            "hygroscopic_sensitivity": "Moderate",
            "filament_drying_temp": 75,
            "filament_drying_hours": 4
        },
        "surface_characteristics": {
            "as_printed_ra_microns": 14.0,
            "porosity_risk": "Moderate",
            "water_permeability_untreated": "Moderate"
        },
        "cost_per_kg_usd": 20.0,
        "kenya_availability": "High",
        "suitability_summary": "Tough and temperature resistant, but requires heated enclosure (unfavorable for field repair in Kenya), suffers UV embrittlement, and exhibits weak Z-axis layer bonding under cyclic hydrodynamic shear."
    },
    "ASA": {
        "name": "Acrylonitrile Styrene Acrylate (ASA)",
        "family": "Thermoplastic Terpolymer",
        "density": 1070.0,  # kg/m^3
        "youngs_modulus_iso": 2.4,  # GPa
        "youngs_modulus_print_xy": 2.3,  # GPa
        "youngs_modulus_print_z": 1.6,  # GPa
        "yield_strength": 42.0,  # MPa
        "ultimate_tensile_strength": 48.0,  # MPa
        "tensile_strength_z": 26.0,  # MPa
        "flexural_modulus": 2.5,  # GPa
        "flexural_strength": 72.0,  # MPa
        "elongation_at_break": 15.0,  # %
        "impact_strength_izod": 12.0,  # kJ/m^2
        "fatigue_strength_limit": 22.0,  # MPa
        "glass_transition_temp": 102.0,
        "melting_point_c": 220.0,  # °C
        "heat_deflection_temp": 93.0,  # °C at 0.45 MPa
        "thermal_conductivity": 0.18,  # W/(m·K)
        "specific_heat_capacity": 1350.0,  # J/(kg·K)
        "water_absorption_24h": 0.30,  # %
        "water_saturation_tensile_drop": 4.5,  # %
        "water_saturation_modulus_drop": 3.8,  # %
        "uv_resistance": "Outstanding (designed specifically for outdoor all-weather endurance)",
        "hydrolysis_resistance": "Good",
        "chemical_resistance": "Good",
        "fdm_printability": {
            "ease_of_printing": "Moderate-Challenging",
            "nozzle_temperature_min": 240,
            "nozzle_temperature_max": 260,
            "bed_temperature_min": 90,
            "bed_temperature_max": 105,
            "enclosure_required": True,
            "warping_tendency": "Moderate-High",
            "abrasive_nozzle_required": False,
            "recommended_nozzle_type": "Standard Brass (0.4mm)",
            "layer_adhesion_quality": "Moderate",
            "hygroscopic_sensitivity": "Moderate",
            "filament_drying_temp": 75,
            "filament_drying_hours": 4
        },
        "surface_characteristics": {
            "as_printed_ra_microns": 15.0,
            "porosity_risk": "Moderate",
            "water_permeability_untreated": "Moderate"
        },
        "cost_per_kg_usd": 28.0,
        "kenya_availability": "Moderate",
        "suitability_summary": "Exceptional UV and weather durability, but requires heated enclosure, has lower modulus than composites, and is more prone to warping in decentralized field setups."
    },
    "Nylon_PA12": {
        "name": "Polyamide 12 (Nylon PA12)",
        "family": "Thermoplastic Polyamide",
        "density": 1020.0,  # kg/m^3
        "youngs_modulus_iso": 1.7,  # GPa
        "youngs_modulus_print_xy": 1.6,  # GPa
        "youngs_modulus_print_z": 1.2,  # GPa
        "yield_strength": 38.0,  # MPa
        "ultimate_tensile_strength": 48.0,  # MPa
        "tensile_strength_z": 30.0,  # MPa
        "flexural_modulus": 1.5,  # GPa
        "flexural_strength": 60.0,  # MPa
        "elongation_at_break": 120.0,  # % (extreme ductility & elongation)
        "impact_strength_izod": 18.0,  # kJ/m^2 (does not fracture easily)
        "fatigue_strength_limit": 26.0,  # MPa
        "glass_transition_temp": 45.0,
        "melting_point_c": 178.0,  # °C
        "heat_deflection_temp": 85.0,  # °C at 0.45 MPa
        "thermal_conductivity": 0.22,  # W/(m·K)
        "specific_heat_capacity": 1600.0,  # J/(kg·K)
        "water_absorption_24h": 0.25,  # % (PA12 absorbs far less moisture than PA6)
        "water_saturation_tensile_drop": 15.0,  # %
        "water_saturation_modulus_drop": 20.0,  # % (plasticization effect of water)
        "uv_resistance": "Moderate",
        "hydrolysis_resistance": "Moderate-Good",
        "chemical_resistance": "Excellent (hydrocarbons, fuels, greases)",
        "fdm_printability": {
            "ease_of_printing": "Challenging",
            "nozzle_temperature_min": 250,
            "nozzle_temperature_max": 275,
            "bed_temperature_min": 80,
            "bed_temperature_max": 100,
            "enclosure_required": True,
            "warping_tendency": "High",
            "abrasive_nozzle_required": False,
            "recommended_nozzle_type": "Hardened Steel / Brass",
            "layer_adhesion_quality": "High",
            "hygroscopic_sensitivity": "Very High (must be dried immediately before printing)",
            "filament_drying_temp": 80,
            "filament_drying_hours": 8
        },
        "surface_characteristics": {
            "as_printed_ra_microns": 18.0,
            "porosity_risk": "High if moist",
            "water_permeability_untreated": "Moderate"
        },
        "cost_per_kg_usd": 55.0,
        "kenya_availability": "Moderate-Low",
        "suitability_summary": "Superb impact toughness and chemical resilience. However, highly flexible (modulus < 2 GPa) which causes turbine blade flutter/stall, and absorbs moisture causing severe plasticization stiffness loss."
    },
    "PA12-CF": {
        "name": "Carbon Fiber Reinforced Nylon (PA12-CF)",
        "family": "Short Fiber Reinforced Polymer Composite",
        "density": 1150.0,  # kg/m^3
        "youngs_modulus_iso": 7.5,  # GPa
        "youngs_modulus_print_xy": 8.2,  # GPa
        "youngs_modulus_print_z": 4.2,  # GPa
        "yield_strength": 75.0,  # MPa
        "ultimate_tensile_strength": 95.0,  # MPa
        "tensile_strength_z": 45.0,  # MPa
        "flexural_modulus": 7.8,  # GPa
        "flexural_strength": 130.0,  # MPa
        "elongation_at_break": 5.0,  # %
        "impact_strength_izod": 8.5,  # kJ/m^2
        "fatigue_strength_limit": 48.0,  # MPa at 10^6 cycles
        "glass_transition_temp": 50.0,
        "melting_point_c": 180.0,  # °C
        "heat_deflection_temp": 140.0,  # °C at 0.45 MPa
        "thermal_conductivity": 0.35,  # W/(m·K)
        "specific_heat_capacity": 1450.0,  # J/(kg·K)
        "water_absorption_24h": 0.35,  # %
        "water_saturation_tensile_drop": 12.0,  # %
        "water_saturation_modulus_drop": 14.0,  # %
        "uv_resistance": "Good",
        "hydrolysis_resistance": "Moderate-Good",
        "chemical_resistance": "Excellent",
        "fdm_printability": {
            "ease_of_printing": "Moderate",
            "nozzle_temperature_min": 260,
            "nozzle_temperature_max": 290,
            "bed_temperature_min": 80,
            "bed_temperature_max": 100,
            "enclosure_required": True,
            "warping_tendency": "Low-Moderate (carbon fibers stabilize thermal shrinkage)",
            "abrasive_nozzle_required": True,
            "recommended_nozzle_type": "Hardened Steel / Ruby (>= 0.4mm)",
            "layer_adhesion_quality": "High",
            "hygroscopic_sensitivity": "High (requires active drybox feed)",
            "filament_drying_temp": 80,
            "filament_drying_hours": 8
        },
        "surface_characteristics": {
            "as_printed_ra_microns": 24.0,
            "porosity_risk": "Moderate",
            "water_permeability_untreated": "Moderate"
        },
        "cost_per_kg_usd": 75.0,
        "kenya_availability": "Low (specialized order in Kenya)",
        "suitability_summary": "Extremely strong and stiff mechanical properties. Excellent candidate for heavy loads, but higher cost, mandatory high-temp drying setup, and moisture sensitivity make it secondary to PETG-CF for decentralized rural maintenance."
    },
    "Polycarbonate": {
        "name": "Polycarbonate (PC)",
        "family": "Thermoplastic Polymer",
        "density": 1200.0,  # kg/m^3
        "youngs_modulus_iso": 2.4,  # GPa
        "youngs_modulus_print_xy": 2.3,  # GPa
        "youngs_modulus_print_z": 1.5,  # GPa
        "yield_strength": 62.0,  # MPa
        "ultimate_tensile_strength": 70.0,  # MPa
        "tensile_strength_z": 30.0,  # MPa
        "flexural_modulus": 2.5,  # GPa
        "flexural_strength": 90.0,  # MPa
        "elongation_at_break": 35.0,  # %
        "impact_strength_izod": 25.0,  # kJ/m^2 (immense impact resistance)
        "fatigue_strength_limit": 30.0,  # MPa
        "glass_transition_temp": 145.0,
        "melting_point_c": 230.0,  # °C
        "heat_deflection_temp": 130.0,  # °C at 0.45 MPa
        "thermal_conductivity": 0.20,  # W/(m·K)
        "specific_heat_capacity": 1200.0,  # J/(kg·K)
        "water_absorption_24h": 0.20,  # %
        "water_saturation_tensile_drop": 5.0,  # %
        "water_saturation_modulus_drop": 4.0,  # %
        "uv_resistance": "Moderate (without UV stabilizers)",
        "hydrolysis_resistance": "Moderate",
        "chemical_resistance": "Moderate",
        "fdm_printability": {
            "ease_of_printing": "Difficult",
            "nozzle_temperature_min": 270,
            "nozzle_temperature_max": 310,
            "bed_temperature_min": 105,
            "bed_temperature_max": 120,
            "enclosure_required": True,
            "warping_tendency": "Very High",
            "abrasive_nozzle_required": False,
            "recommended_nozzle_type": "Hardened / Plated Copper (0.4mm)",
            "layer_adhesion_quality": "Moderate",
            "hygroscopic_sensitivity": "High",
            "filament_drying_temp": 85,
            "filament_drying_hours": 6
        },
        "surface_characteristics": {
            "as_printed_ra_microns": 16.0,
            "porosity_risk": "Moderate",
            "water_permeability_untreated": "Moderate"
        },
        "cost_per_kg_usd": 42.0,
        "kenya_availability": "Moderate",
        "suitability_summary": "High strength and impact resistance, but extremely difficult to print without dedicated chamber heaters (110°C+ bed), making it unviable on standard portable rural printers."
    },
    "Aluminium_6061_T6": {
        "name": "Aluminium 6061-T6 (Benchmark)",
        "family": "Non-Ferrous Metal Alloy",
        "density": 2700.0,  # kg/m^3
        "youngs_modulus_iso": 68.9,  # GPa
        "youngs_modulus_print_xy": 68.9,
        "youngs_modulus_print_z": 68.9,
        "yield_strength": 276.0,  # MPa
        "ultimate_tensile_strength": 310.0,  # MPa
        "tensile_strength_z": 276.0,
        "flexural_modulus": 68.9,
        "flexural_strength": 310.0,
        "elongation_at_break": 12.0,  # %
        "impact_strength_izod": 30.0,  # kJ/m^2
        "fatigue_strength_limit": 96.0,  # MPa at 5x10^8 cycles
        "glass_transition_temp": 582.0,
        "melting_point_c": 582.0,  # Solidus °C
        "heat_deflection_temp": 500.0,  # Solidus/deflection limit (°C)
        "thermal_conductivity": 167.0,  # W/(m·K)
        "specific_heat_capacity": 896.0,  # J/(kg·K)
        "water_absorption_24h": 0.0,  # %
        "water_saturation_tensile_drop": 0.0,  # %
        "water_saturation_modulus_drop": 0.0,  # %
        "uv_resistance": "Immune",
        "hydrolysis_resistance": "Immune (susceptible to galvanic corrosion in brackish water)",
        "chemical_resistance": "Good",
        "fdm_printability": {
            "ease_of_printing": "Not FDM Printable",
            "nozzle_temperature_min": 0,
            "nozzle_temperature_max": 0,
            "bed_temperature_min": 0,
            "bed_temperature_max": 0,
            "enclosure_required": False,
            "warping_tendency": "N/A",
            "abrasive_nozzle_required": False,
            "recommended_nozzle_type": "N/A (requires CNC milling or DMLS)",
            "layer_adhesion_quality": "Isotropic",
            "hygroscopic_sensitivity": "None",
            "filament_drying_temp": 0,
            "filament_drying_hours": 0
        },
        "surface_characteristics": {
            "as_printed_ra_microns": 1.6,  # CNC machined finish
            "porosity_risk": "None",
            "water_permeability_untreated": "Impermeable"
        },
        "cost_per_kg_usd": 12.0,  # raw stock, but tooling/machining costs add $200+
        "kenya_availability": "Moderate (stock available in industrial Nairobi; requires CNC infrastructure)",
        "suitability_summary": "Traditional engineering benchmark. High stiffness and strength, but requires centralized CNC machining or expensive casting molds, causing weeks of supply-chain downtime for rural repairs."
    },
    "Stainless_Steel_316L": {
        "name": "Stainless Steel 316L (Marine Benchmark)",
        "family": "Ferrous Metal Alloy",
        "density": 8000.0,  # kg/m^3
        "youngs_modulus_iso": 193.0,  # GPa
        "youngs_modulus_print_xy": 193.0,
        "youngs_modulus_print_z": 193.0,
        "yield_strength": 290.0,  # MPa
        "ultimate_tensile_strength": 580.0,  # MPa
        "tensile_strength_z": 290.0,
        "flexural_modulus": 193.0,
        "flexural_strength": 580.0,
        "elongation_at_break": 50.0,  # %
        "impact_strength_izod": 105.0,  # kJ/m^2
        "fatigue_strength_limit": 240.0,  # MPa
        "glass_transition_temp": 1375.0,
        "melting_point_c": 1375.0,  # Solidus °C
        "heat_deflection_temp": 1000.0,  # °C
        "thermal_conductivity": 16.3,  # W/(m·K)
        "specific_heat_capacity": 500.0,  # J/(kg·K)
        "water_absorption_24h": 0.0,  # %
        "water_saturation_tensile_drop": 0.0,  # %
        "water_saturation_modulus_drop": 0.0,  # %
        "uv_resistance": "Immune",
        "hydrolysis_resistance": "Immune (marine grade corrosion proof)",
        "chemical_resistance": "Excellent",
        "fdm_printability": {
            "ease_of_printing": "Not FDM Printable",
            "nozzle_temperature_min": 0,
            "nozzle_temperature_max": 0,
            "bed_temperature_min": 0,
            "bed_temperature_max": 0,
            "enclosure_required": False,
            "warping_tendency": "N/A",
            "abrasive_nozzle_required": False,
            "recommended_nozzle_type": "N/A (Foundry casting / DMLS)",
            "layer_adhesion_quality": "Isotropic",
            "hygroscopic_sensitivity": "None",
            "filament_drying_temp": 0,
            "filament_drying_hours": 0
        },
        "surface_characteristics": {
            "as_printed_ra_microns": 0.8,
            "porosity_risk": "None",
            "water_permeability_untreated": "Impermeable"
        },
        "cost_per_kg_usd": 15.0,  # raw, but casting/import costs $500+ per blade
        "kenya_availability": "Low (imported parts; long customs delays)",
        "suitability_summary": "Gold standard for corrosion resistance and mechanical strength. However, high density (8000 kg/m3) creates high rotor inertia, and reliance on imported castings is the exact bottleneck causing months of blackout during blade fracture in Kenya."
    },
    "Titanium_Ti6Al4V": {
        "name": "Titanium Ti-6Al-4V (Grade 5)",
        "family": "Titanium Alloy",
        "density": 4430.0,  # kg/m^3 (45% lighter than steel)
        "youngs_modulus_iso": 114.0,  # GPa
        "youngs_modulus_print_xy": 114.0,
        "youngs_modulus_print_z": 114.0,
        "yield_strength": 880.0,  # MPa
        "ultimate_tensile_strength": 950.0,  # MPa
        "tensile_strength_z": 880.0,
        "flexural_modulus": 114.0,
        "flexural_strength": 950.0,
        "elongation_at_break": 14.0,  # %
        "impact_strength_izod": 34.0,  # kJ/m^2
        "fatigue_strength_limit": 510.0,  # MPa (superb fatigue resistance)
        "glass_transition_temp": 1604.0,
        "melting_point_c": 1604.0,  # Solidus °C
        "heat_deflection_temp": 350.0,  # °C (continuous service limit before alpha-case oxidation and creep)
        "thermal_conductivity": 6.7,  # W/(m·K)
        "specific_heat_capacity": 526.0,  # J/(kg·K)
        "water_absorption_24h": 0.0,
        "water_saturation_tensile_drop": 0.0,
        "water_saturation_modulus_drop": 0.0,
        "uv_resistance": "Immune",
        "hydrolysis_resistance": "Immune (biocompatible and marine inert)",
        "chemical_resistance": "Outstanding",
        "fdm_printability": {
            "ease_of_printing": "Not FDM Printable",
            "nozzle_temperature_min": 0,
            "nozzle_temperature_max": 0,
            "bed_temperature_min": 0,
            "bed_temperature_max": 0,
            "enclosure_required": False,
            "warping_tendency": "N/A",
            "abrasive_nozzle_required": False,
            "recommended_nozzle_type": "DMLS / SLM or 5-Axis CNC Milling",
            "layer_adhesion_quality": "Isotropic",
            "hygroscopic_sensitivity": "None",
            "filament_drying_temp": 0,
            "filament_drying_hours": 0
        },
        "surface_characteristics": {
            "as_printed_ra_microns": 0.8,
            "porosity_risk": "None",
            "water_permeability_untreated": "Impermeable"
        },
        "cost_per_kg_usd": 65.0,
        "kenya_availability": "Very Low (specialized aerospace/medical import)",
        "suitability_summary": "Pinnacle material for high specific strength (sigma_y/rho), extreme fatigue life, and biological inertness. Optimal for aerospace airframes, high-stress bicycle forks, racing suspension, and biomedical hip implants."
    },
    "Copper_C11000": {
        "name": "Copper C11000 (ETP Copper)",
        "family": "Non-Ferrous Metal Alloy",
        "density": 8940.0,  # kg/m^3
        "youngs_modulus_iso": 117.0,  # GPa
        "youngs_modulus_print_xy": 117.0,
        "youngs_modulus_print_z": 117.0,
        "yield_strength": 200.0,  # MPa (half-hard)
        "ultimate_tensile_strength": 280.0,  # MPa
        "tensile_strength_z": 200.0,
        "flexural_modulus": 117.0,
        "flexural_strength": 280.0,
        "elongation_at_break": 25.0,  # %
        "impact_strength_izod": 45.0,  # kJ/m^2
        "fatigue_strength_limit": 90.0,  # MPa
        "glass_transition_temp": 1083.0,
        "melting_point_c": 1083.0,  # Solidus °C
        "heat_deflection_temp": 350.0,  # °C
        "thermal_conductivity": 390.0,  # W/(m·K) (KING of heat conduction!)
        "specific_heat_capacity": 385.0,  # J/(kg·K)
        "water_absorption_24h": 0.0,
        "water_saturation_tensile_drop": 0.0,
        "water_saturation_modulus_drop": 0.0,
        "uv_resistance": "Immune",
        "hydrolysis_resistance": "Good (develops protective patina)",
        "chemical_resistance": "Good",
        "fdm_printability": {
            "ease_of_printing": "Not FDM Printable",
            "nozzle_temperature_min": 0,
            "nozzle_temperature_max": 0,
            "bed_temperature_min": 0,
            "bed_temperature_max": 0,
            "enclosure_required": False,
            "warping_tendency": "N/A",
            "abrasive_nozzle_required": False,
            "recommended_nozzle_type": "CNC Machining / Casting / Extrusion",
            "layer_adhesion_quality": "Isotropic",
            "hygroscopic_sensitivity": "None",
            "filament_drying_temp": 0,
            "filament_drying_hours": 0
        },
        "surface_characteristics": {
            "as_printed_ra_microns": 0.4,
            "porosity_risk": "None",
            "water_permeability_untreated": "Impermeable"
        },
        "cost_per_kg_usd": 12.0,
        "kenya_availability": "High (widely available in electrical and scrap markets)",
        "suitability_summary": "Unmatched thermal conductivity (390 W/mK) and electrical conductivity. The undisputed gold standard for CPU heat sinks, heat exchangers, cooling blocks, and high-power thermal management."
    },
    "Alloy_Steel_4140": {
        "name": "Chromium-Molybdenum Steel (AISI 4140, Q&T)",
        "family": "High-Strength Alloy Steel",
        "density": 7850.0,  # kg/m^3
        "youngs_modulus_iso": 205.0,  # GPa
        "youngs_modulus_print_xy": 205.0,
        "youngs_modulus_print_z": 205.0,
        "yield_strength": 655.0,  # MPa
        "ultimate_tensile_strength": 850.0,  # MPa
        "tensile_strength_z": 655.0,
        "flexural_modulus": 205.0,
        "flexural_strength": 850.0,
        "elongation_at_break": 18.0,  # %
        "impact_strength_izod": 55.0,  # kJ/m^2
        "fatigue_strength_limit": 420.0,  # MPa (superb endurance)
        "glass_transition_temp": 1420.0,
        "melting_point_c": 1420.0,  # Solidus °C
        "heat_deflection_temp": 600.0,  # °C
        "thermal_conductivity": 42.6,  # W/(m·K)
        "specific_heat_capacity": 477.0,  # J/(kg·K)
        "water_absorption_24h": 0.0,
        "water_saturation_tensile_drop": 0.0,
        "water_saturation_modulus_drop": 0.0,
        "uv_resistance": "Immune",
        "hydrolysis_resistance": "Fair (requires surface painting or black oxide against rust)",
        "chemical_resistance": "Good",
        "fdm_printability": {
            "ease_of_printing": "Not FDM Printable",
            "nozzle_temperature_min": 0,
            "nozzle_temperature_max": 0,
            "bed_temperature_min": 0,
            "bed_temperature_max": 0,
            "enclosure_required": False,
            "warping_tendency": "N/A",
            "abrasive_nozzle_required": False,
            "recommended_nozzle_type": "Forging / CNC Machining",
            "layer_adhesion_quality": "Isotropic",
            "hygroscopic_sensitivity": "None",
            "filament_drying_temp": 0,
            "filament_drying_hours": 0
        },
        "surface_characteristics": {
            "as_printed_ra_microns": 0.8,
            "porosity_risk": "None",
            "water_permeability_untreated": "Impermeable"
        },
        "cost_per_kg_usd": 4.5,
        "kenya_availability": "Moderate-High (industrial steel distributors)",
        "suitability_summary": "Exceptional toughness, high torsional strength, and fatigue resistance. Industry standard for Chromoly bicycle frames, heavy-duty automotive drive axles, crane hooks, high-load gears, and connecting rods."
    },
    "CFRP_Prepreg": {
        "name": "Carbon Fiber Epoxy Prepreg (Continuous CFRP)",
        "family": "Continuous Fiber Composite",
        "density": 1550.0,  # kg/m^3 (ultra-lightweight)
        "youngs_modulus_iso": 135.0,  # GPa (in fiber direction)
        "youngs_modulus_print_xy": 135.0,
        "youngs_modulus_print_z": 10.0,
        "yield_strength": 1200.0,  # MPa
        "ultimate_tensile_strength": 1500.0,  # MPa
        "tensile_strength_z": 50.0,
        "flexural_modulus": 120.0,
        "flexural_strength": 1100.0,
        "elongation_at_break": 1.5,  # %
        "impact_strength_izod": 65.0,  # kJ/m^2
        "fatigue_strength_limit": 750.0,  # MPa (unsurpassed specific fatigue limit)
        "glass_transition_temp": 180.0,
        "melting_point_c": 350.0,  # °C
        "heat_deflection_temp": 160.0,  # °C
        "thermal_conductivity": 4.5,  # W/(m·K)
        "specific_heat_capacity": 1100.0,  # J/(kg·K)
        "water_absorption_24h": 0.10,
        "water_saturation_tensile_drop": 2.0,
        "water_saturation_modulus_drop": 1.5,
        "uv_resistance": "Good (epoxy matrix requires UV clearcoat)",
        "hydrolysis_resistance": "Excellent",
        "chemical_resistance": "Excellent",
        "fdm_printability": {
            "ease_of_printing": "Not FDM Printable",
            "nozzle_temperature_min": 0,
            "nozzle_temperature_max": 0,
            "bed_temperature_min": 0,
            "bed_temperature_max": 0,
            "enclosure_required": False,
            "warping_tendency": "N/A",
            "abrasive_nozzle_required": False,
            "recommended_nozzle_type": "Autoclave / Vacuum Bag Compression Molding",
            "layer_adhesion_quality": "Laminate Anisotropic",
            "hygroscopic_sensitivity": "Low",
            "filament_drying_temp": 0,
            "filament_drying_hours": 0
        },
        "surface_characteristics": {
            "as_printed_ra_microns": 0.2,  # mold surface finish
            "porosity_risk": "None (autoclave cured)",
            "water_permeability_untreated": "Impermeable"
        },
        "cost_per_kg_usd": 120.0,
        "kenya_availability": "Very Low (requires cold chain freezer transit)",
        "suitability_summary": "Unrivaled specific stiffness (E/rho) and specific strength (sigma_y/rho). Benchmark choice for Formula 1 monocoques, Tour de France bicycle frames, aerospace wings, and competition drone airframes."
    },
    "PEEK": {
        "name": "Polyetheretherketone (PEEK)",
        "family": "High-Performance Thermoplastic",
        "density": 1300.0,  # kg/m^3
        "youngs_modulus_iso": 3.8,  # GPa
        "youngs_modulus_print_xy": 3.8,
        "youngs_modulus_print_z": 2.6,
        "yield_strength": 95.0,  # MPa
        "ultimate_tensile_strength": 100.0,  # MPa
        "tensile_strength_z": 60.0,
        "flexural_modulus": 3.9,
        "flexural_strength": 140.0,
        "elongation_at_break": 35.0,  # %
        "impact_strength_izod": 8.0,  # kJ/m^2
        "fatigue_strength_limit": 60.0,  # MPa
        "glass_transition_temp": 143.0,
        "melting_point_c": 343.0,  # °C
        "heat_deflection_temp": 250.0,  # °C at 0.45 MPa (continuous service up to 260°C!)
        "thermal_conductivity": 0.25,  # W/(m·K)
        "specific_heat_capacity": 1340.0,  # J/(kg·K)
        "water_absorption_24h": 0.06,  # %
        "water_saturation_tensile_drop": 0.5,  # %
        "water_saturation_modulus_drop": 0.5,  # %
        "uv_resistance": "Outstanding",
        "hydrolysis_resistance": "Outstanding (autoclave steam sterilizable)",
        "chemical_resistance": "Outstanding (unaffected by almost all acids, solvents, fuels)",
        "fdm_printability": {
            "ease_of_printing": "Expert Only",
            "nozzle_temperature_min": 380,
            "nozzle_temperature_max": 420,
            "bed_temperature_min": 130,
            "bed_temperature_max": 160,
            "enclosure_required": True,  # 70-90°C chamber required
            "warping_tendency": "Extreme",
            "abrasive_nozzle_required": False,
            "recommended_nozzle_type": "Hardened High-Temp Nozzle (0.4mm)",
            "layer_adhesion_quality": "High when properly annealed",
            "hygroscopic_sensitivity": "Moderate",
            "filament_drying_temp": 120,
            "filament_drying_hours": 6
        },
        "surface_characteristics": {
            "as_printed_ra_microns": 12.0,
            "porosity_risk": "Moderate",
            "water_permeability_untreated": "Low"
        },
        "cost_per_kg_usd": 380.0,
        "kenya_availability": "Very Low",
        "suitability_summary": "Top-tier polymer capable of replacing metal components. Continuous 250°C thermal stability, full chemical and autoclave immunity, and biocompatibility. Ideal for aerospace pump impellers, surgical implants, and high-heat semiconductor fixtures."
    },
    "TPU_95A": {
        "name": "Thermoplastic Polyurethane (TPU 95A)",
        "family": "Elastomeric Polymer",
        "density": 1210.0,  # kg/m^3
        "youngs_modulus_iso": 0.05,  # GPa (50 MPa - extremely compliant!)
        "youngs_modulus_print_xy": 0.05,
        "youngs_modulus_print_z": 0.048,
        "yield_strength": 15.0,  # MPa
        "ultimate_tensile_strength": 35.0,  # MPa
        "tensile_strength_z": 32.0,  # (near-isotropic layer adhesion!)
        "flexural_modulus": 0.06,  # GPa
        "flexural_strength": 20.0,  # MPa
        "elongation_at_break": 500.0,  # % (huge elastic strain capacity)
        "impact_strength_izod": 120.0,  # kJ/m^2 (will not shatter)
        "fatigue_strength_limit": 12.0,  # MPa
        "glass_transition_temp": -25.0,
        "melting_point_c": 200.0,  # °C
        "heat_deflection_temp": 60.0,  # °C
        "thermal_conductivity": 0.19,  # W/(m·K)
        "specific_heat_capacity": 1800.0,  # J/(kg·K)
        "water_absorption_24h": 0.50,  # %
        "water_saturation_tensile_drop": 5.0,  # %
        "water_saturation_modulus_drop": 4.0,  # %
        "uv_resistance": "Good",
        "hydrolysis_resistance": "Good",
        "chemical_resistance": "Excellent (grease, oils, fuels)",
        "fdm_printability": {
            "ease_of_printing": "Moderate (requires direct drive extruder)",
            "nozzle_temperature_min": 215,
            "nozzle_temperature_max": 235,
            "bed_temperature_min": 40,
            "bed_temperature_max": 60,
            "enclosure_required": False,
            "warping_tendency": "None",
            "abrasive_nozzle_required": False,
            "recommended_nozzle_type": "Standard Brass (0.4mm)",
            "layer_adhesion_quality": "Outstanding (indestructible layer fusion)",
            "hygroscopic_sensitivity": "High",
            "filament_drying_temp": 50,
            "filament_drying_hours": 4
        },
        "surface_characteristics": {
            "as_printed_ra_microns": 18.0,
            "porosity_risk": "Low",
            "water_permeability_untreated": "Low"
        },
        "cost_per_kg_usd": 32.0,
        "kenya_availability": "Moderate",
        "suitability_summary": "Superb elasticity, immense shock absorption, and high abrasion resistance. Optimal for smartphone protective cases, drone landing bumpers, vibration damping mounts, flexible gaskets, and compliant hinges."
    },
    "Alumina_Ceramic": {
        "name": "Alumina Ceramic (Al2O3 99.5%)",
        "family": "Technical Ceramic",
        "density": 3900.0,  # kg/m^3
        "youngs_modulus_iso": 370.0,  # GPa (extremely stiff)
        "youngs_modulus_print_xy": 370.0,
        "youngs_modulus_print_z": 370.0,
        "yield_strength": 300.0,  # MPa (flexural strength)
        "ultimate_tensile_strength": 320.0,  # MPa
        "tensile_strength_z": 300.0,
        "flexural_modulus": 370.0,
        "flexural_strength": 350.0,
        "elongation_at_break": 0.1,  # % (extremely brittle)
        "impact_strength_izod": 5.0,  # kJ/m^2
        "fatigue_strength_limit": 180.0,  # MPa
        "glass_transition_temp": 2072.0,
        "melting_point_c": 2072.0,  # Melting point °C
        "heat_deflection_temp": 1600.0,  # °C
        "thermal_conductivity": 30.0,  # W/(m·K)
        "specific_heat_capacity": 880.0,  # J/(kg·K)
        "water_absorption_24h": 0.0,
        "water_saturation_tensile_drop": 0.0,
        "water_saturation_modulus_drop": 0.0,
        "uv_resistance": "Immune",
        "hydrolysis_resistance": "Immune",
        "chemical_resistance": "Immune",
        "fdm_printability": {
            "ease_of_printing": "Not FDM Printable",
            "nozzle_temperature_min": 0,
            "nozzle_temperature_max": 0,
            "bed_temperature_min": 0,
            "bed_temperature_max": 0,
            "enclosure_required": False,
            "warping_tendency": "N/A",
            "abrasive_nozzle_required": False,
            "recommended_nozzle_type": "Ceramic Sintering / Diamond Grinding",
            "layer_adhesion_quality": "Isotropic",
            "hygroscopic_sensitivity": "None",
            "filament_drying_temp": 0,
            "filament_drying_hours": 0
        },
        "surface_characteristics": {
            "as_printed_ra_microns": 0.2,
            "porosity_risk": "None (sintered)",
            "water_permeability_untreated": "Impermeable"
        },
        "cost_per_kg_usd": 40.0,
        "kenya_availability": "Low",
        "suitability_summary": "Immense stiffness (370 GPa), extreme Mohs hardness (9.0), high thermal stability (1600°C), and superb dielectric insulation. Unmatched for electrical high-voltage insulators, spark plug sleeves, and abrasive slurry pump liners."
    },
    "POM_Delrin": {
        "name": "Polyoxymethylene / Acetal (POM Delrin)",
        "family": "Engineering Thermoplastic",
        "density": 1410.0,  # kg/m^3
        "youngs_modulus_iso": 2.8,  # GPa
        "youngs_modulus_print_xy": 2.8,
        "youngs_modulus_print_z": 2.0,
        "yield_strength": 65.0,  # MPa
        "ultimate_tensile_strength": 70.0,  # MPa
        "tensile_strength_z": 40.0,
        "flexural_modulus": 2.9,
        "flexural_strength": 90.0,
        "elongation_at_break": 25.0,  # %
        "impact_strength_izod": 6.0,  # kJ/m^2
        "fatigue_strength_limit": 32.0,  # MPa
        "glass_transition_temp": -50.0,
        "melting_point_c": 175.0,  # °C
        "heat_deflection_temp": 110.0,  # °C
        "thermal_conductivity": 0.23,  # W/(m·K)
        "specific_heat_capacity": 1500.0,  # J/(kg·K)
        "water_absorption_24h": 0.20,  # %
        "water_saturation_tensile_drop": 2.0,  # %
        "water_saturation_modulus_drop": 1.5,  # %
        "uv_resistance": "Moderate",
        "hydrolysis_resistance": "Good",
        "chemical_resistance": "Outstanding (solvents, fuels, oils)",
        "fdm_printability": {
            "ease_of_printing": "Difficult",
            "nozzle_temperature_min": 220,
            "nozzle_temperature_max": 240,
            "bed_temperature_min": 100,
            "bed_temperature_max": 120,
            "enclosure_required": True,
            "warping_tendency": "Extreme (crystallization shrinkage)",
            "abrasive_nozzle_required": False,
            "recommended_nozzle_type": "Brass or Steel (CNC machining preferred)",
            "layer_adhesion_quality": "Moderate",
            "hygroscopic_sensitivity": "Low",
            "filament_drying_temp": 80,
            "filament_drying_hours": 4
        },
        "surface_characteristics": {
            "as_printed_ra_microns": 10.0,
            "porosity_risk": "Low",
            "water_permeability_untreated": "Low"
        },
        "cost_per_kg_usd": 24.0,
        "kenya_availability": "Moderate",
        "suitability_summary": "Industry standard for low-friction mechanical components. Superb natural lubricity (friction coefficient 0.15), dimensional stability, and high fatigue endurance. Optimal for precision gears, sliding bearings, pulleys, and bushings."
    },
    "Inconel_718": {
        "name": "Inconel 718 (Nickel Superalloy)",
        "family": "Nickel Superalloy",
        "density": 8190.0,  # kg/m^3
        "youngs_modulus_iso": 211.0,  # GPa
        "youngs_modulus_print_xy": 211.0,
        "youngs_modulus_print_z": 211.0,
        "yield_strength": 1100.0,  # MPa
        "ultimate_tensile_strength": 1375.0,  # MPa
        "tensile_strength_z": 1100.0,
        "flexural_modulus": 211.0,
        "flexural_strength": 1375.0,
        "elongation_at_break": 15.0,  # %
        "impact_strength_izod": 48.0,  # kJ/m^2
        "fatigue_strength_limit": 600.0,  # MPa
        "glass_transition_temp": 1336.0,
        "melting_point_c": 1336.0,  # Solidus °C
        "heat_deflection_temp": 950.0,  # °C (sustains mechanical loads up to 700°C)
        "thermal_conductivity": 11.4,  # W/(m·K)
        "specific_heat_capacity": 435.0,  # J/(kg·K)
        "water_absorption_24h": 0.0,
        "water_saturation_tensile_drop": 0.0,
        "water_saturation_modulus_drop": 0.0,
        "uv_resistance": "Immune",
        "hydrolysis_resistance": "Immune",
        "chemical_resistance": "Immune",
        "fdm_printability": {
            "ease_of_printing": "Not FDM Printable",
            "nozzle_temperature_min": 0,
            "nozzle_temperature_max": 0,
            "bed_temperature_min": 0,
            "bed_temperature_max": 0,
            "enclosure_required": False,
            "warping_tendency": "N/A",
            "abrasive_nozzle_required": False,
            "recommended_nozzle_type": "DMLS / SLM Metal 3D Printing or Heavy CNC",
            "layer_adhesion_quality": "Isotropic",
            "hygroscopic_sensitivity": "None",
            "filament_drying_temp": 0,
            "filament_drying_hours": 0
        },
        "surface_characteristics": {
            "as_printed_ra_microns": 1.2,
            "porosity_risk": "None",
            "water_permeability_untreated": "Impermeable"
        },
        "cost_per_kg_usd": 110.0,
        "kenya_availability": "Very Low",
        "suitability_summary": "The ultimate high-temperature high-stress superalloy. Retains yield strength (>1000 MPa) at temperatures exceeding 650°C. Sovereign choice for rocket engine combustion chambers, jet turbine blades, turbocharger turbine wheels, and exhaust manifolds."
    }
}
# Canonical alias for compatibility
MATERIALS_DATABASE["Alumina_Al2O3"] = MATERIALS_DATABASE["Alumina_Ceramic"]


COMMON_ALIASES: Dict[str, str] = {
    "ALUMINUM": "Aluminium_6061_T6",
    "ALUMINIUM": "Aluminium_6061_T6",
    "ALUMINUM6061": "Aluminium_6061_T6",
    "ALUMINIUM6061": "Aluminium_6061_T6",
    "6061": "Aluminium_6061_T6",
    "6061T6": "Aluminium_6061_T6",
    "AL": "Aluminium_6061_T6",
    "STEEL": "Stainless_Steel_316L",
    "STAINLESS": "Stainless_Steel_316L",
    "STAINLESSSTEEL": "Stainless_Steel_316L",
    "SS316L": "Stainless_Steel_316L",
    "316L": "Stainless_Steel_316L",
    "PC": "Polycarbonate",
    "NYLON": "Nylon_PA12",
    "PA12": "Nylon_PA12",
    "PA": "Nylon_PA12",
    "POLYAMIDE": "Nylon_PA12",
    "CARBONFIBER": "PETG-CF",
    "CARBONFIBRE": "PETG-CF",
    "CF": "PETG-CF",
    "PETGCF": "PETG-CF",
    "PA12CF": "PA12-CF",
    "PACF": "PA12-CF",
    "CARBONFIBERPETG": "PETG-CF",
    "CARBONFIBERNYLON": "PA12-CF",
    "TITANIUM": "Titanium_Ti6Al4V",
    "TI": "Titanium_Ti6Al4V",
    "TI6AL4V": "Titanium_Ti6Al4V",
    "GRADE5TITANIUM": "Titanium_Ti6Al4V",
    "COPPER": "Copper_C11000",
    "CU": "Copper_C11000",
    "C11000": "Copper_C11000",
    "4140": "Alloy_Steel_4140",
    "CHROMOLY": "Alloy_Steel_4140",
    "CHROME-MOLY": "Alloy_Steel_4140",
    "AISI4140": "Alloy_Steel_4140",
    "CFRP": "CFRP_Prepreg",
    "CONTINUOUSCFRP": "CFRP_Prepreg",
    "PREPREG": "CFRP_Prepreg",
    "PEEK": "PEEK",
    "POLYETHERETHERKETONE": "PEEK",
    "TPU": "TPU_95A",
    "TPU95A": "TPU_95A",
    "POLYURETHANE": "TPU_95A",
    "RUBBER": "TPU_95A",
    "CERAMIC": "Alumina_Ceramic",
    "ALUMINA": "Alumina_Ceramic",
    "ALUMINACERAMIC": "Alumina_Ceramic",
    "ALUMINAAL2O3": "Alumina_Ceramic",
    "AL2O3": "Alumina_Ceramic",
    "DELRIN": "POM_Delrin",
    "POM": "POM_Delrin",
    "ACETAL": "POM_Delrin",
    "INCONEL": "Inconel_718",
    "INCONEL718": "Inconel_718",
    "INCO718": "Inconel_718",
}


def get_material(name: str) -> Optional[Dict[str, Any]]:
    """Retrieve material record by exact or partial key match, with synonym & alias normalization."""
    if not name:
        return None
    if name in MATERIALS_DATABASE:
        return MATERIALS_DATABASE[name]

    clean_name = name.strip().upper().replace(" ", "").replace("_", "").replace("-", "").replace("(", "").replace(")", "")
    
    # Check direct common aliases first
    if clean_name in COMMON_ALIASES:
        target_key = COMMON_ALIASES[clean_name]
        return MATERIALS_DATABASE.get(target_key)

    # Normalize American/British spelling variation
    normalized_name = clean_name.replace("ALUMINUM", "ALUMINIUM").replace("FIBRE", "FIBER")

    for key, data in MATERIALS_DATABASE.items():
        clean_key = key.upper().replace(" ", "").replace("_", "").replace("-", "").replace("(", "").replace(")", "")
        clean_mat_name = data["name"].upper().replace(" ", "").replace("_", "").replace("-", "").replace("(", "").replace(")", "").replace("ALUMINUM", "ALUMINIUM")
        if (clean_key == normalized_name or 
            normalized_name in clean_key or 
            clean_key in normalized_name or 
            normalized_name in clean_mat_name):
            return data
    return None


def list_all_materials() -> List[Dict[str, Any]]:
    """Return all unique materials as a list."""
    seen = set()
    unique = []
    for mat in MATERIALS_DATABASE.values():
        if mat["name"] not in seen:
            seen.add(mat["name"])
            unique.append(mat)
    return unique


def filter_fdm_printable_materials() -> List[Dict[str, Any]]:
    """Return only materials compatible with FDM 3D printing."""
    return [
        mat for mat in MATERIALS_DATABASE.values()
        if mat["fdm_printability"]["ease_of_printing"] != "Not FDM Printable"
    ]

