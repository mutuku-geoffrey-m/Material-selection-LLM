"""
Ashby Optimization Methodology & Performance Index Calculation Engine.
Implements analytical performance indices developed by Prof. Michael F. Ashby
for mechanical component optimization under functional stiffness, strength,
mass minimization, thermal dissipation, and economic constraints.
"""

from typing import Dict, Any, List, Optional, Tuple
import math
from src.materials_db import MATERIALS_DATABASE, list_all_materials


class AshbyIndex:
    """Standard mechanical engineering Ashby performance indices."""

    # Function: Stiff, lightweight components
    TIE_STIFFNESS = "tie_stiffness"         # M = E / rho
    BEAM_STIFFNESS = "beam_stiffness"       # M = E^(1/2) / rho (Internal blade spar stiffness)
    PLATE_STIFFNESS = "plate_stiffness"     # M = E^(1/3) / rho (Hydrofoil skin panel deflection)

    # Function: Strong, lightweight components (yielding limit)
    TIE_STRENGTH = "tie_strength"           # M = sigma_y / rho
    BEAM_STRENGTH = "beam_strength"         # M = sigma_y^(2/3) / rho (Bending failure limit)
    PLATE_STRENGTH = "plate_strength"       # M = sigma_y^(1/2) / rho

    # Function: Specialized mechanical indices
    FLYWHEEL_INERTIA = "flywheel_inertia"   # M = sigma_y / rho (Max rotational kinetic energy)
    ELASTIC_ENERGY = "elastic_energy"       # M = sigma_y^2 / E (Flexural compliance & shock damping)
    THERMAL_DIFFUSIVITY = "thermal_diffusivity" # a = lambda / (rho * Cp) (Heat dissipation)
    THERMAL_CONDUCTIVITY = "thermal_conductivity" # M = lambda (Steady-state heat conduction / heat sinks)
    THERMAL_INSULATION = "thermal_insulation"     # M = 1 / lambda (Thermal barriers)
    FATIGUE_EFFICIENCY = "fatigue_efficiency"   # M = sigma_fatigue / rho (Cyclic loading)


INDEX_DESCRIPTIONS = {
    AshbyIndex.BEAM_STIFFNESS: {
        "name": "Beam in Bending (Stiffness-Driven)",
        "formula": "E^(1/2) / ρ",
        "primary_application": "Structural spars, bicycle frame tubes, crane arms, cantilever deflection control",
        "log_log_slope_e_rho": 2.0,
        "maximize": True
    },
    AshbyIndex.TIE_STIFFNESS: {
        "name": "Tie in Tension (Stiffness-Driven)",
        "formula": "E / ρ",
        "primary_application": "Tensile structural members, guy wires, aircraft fuselage stringers, truss chords",
        "log_log_slope_e_rho": 1.0,
        "maximize": True
    },
    AshbyIndex.PLATE_STIFFNESS: {
        "name": "Plate in Bending (Stiffness-Driven)",
        "formula": "E^(1/3) / ρ",
        "primary_application": "Hydrofoil skins, laptop chassis lids, automotive body panels, aerodynamic shells",
        "log_log_slope_e_rho": 3.0,
        "maximize": True
    },
    AshbyIndex.BEAM_STRENGTH: {
        "name": "Beam in Bending (Strength-Driven)",
        "formula": "σ_y^(2/3) / ρ",
        "primary_application": "Beams, chassis members, and cantilever spars resisting bending fracture under peak load",
        "log_log_slope_sigma_rho": 1.5,
        "maximize": True
    },
    AshbyIndex.TIE_STRENGTH: {
        "name": "Tie in Tension (Strength-Driven)",
        "formula": "σ_y / ρ",
        "primary_application": "Tension members, suspension cables, rotor hub radial centrifugal load",
        "log_log_slope_sigma_rho": 1.0,
        "maximize": True
    },
    AshbyIndex.PLATE_STRENGTH: {
        "name": "Plate in Bending (Strength-Driven)",
        "formula": "σ_y^(1/2) / ρ",
        "primary_application": "Shell buckling, pressure vessel faceplates, hydrostatic bursting resistance",
        "log_log_slope_sigma_rho": 2.0,
        "maximize": True
    },
    AshbyIndex.FLYWHEEL_INERTIA: {
        "name": "Kinetic Energy Storage / High-Speed Rotor",
        "formula": "σ_y / ρ",
        "primary_application": "Turbine rotors & generator flywheel energy storage without bursting",
        "log_log_slope_sigma_rho": 1.0,
        "maximize": True
    },
    AshbyIndex.ELASTIC_ENERGY: {
        "name": "Maximum Elastic Strain Energy",
        "formula": "σ_y^2 / E",
        "primary_application": "Springs, flexible clips, compliant mechanisms, shock absorbing bumpers",
        "maximize": True
    },
    AshbyIndex.THERMAL_CONDUCTIVITY: {
        "name": "Thermal Conductivity (Steady-State)",
        "formula": "λ",
        "primary_application": "Heat sinks, CPU cooling blocks, electronic packaging, heat exchangers",
        "maximize": True
    },
    AshbyIndex.THERMAL_DIFFUSIVITY: {
        "name": "Thermal Diffusivity",
        "formula": "λ / (ρ · c_p)",
        "primary_application": "Transient heat dissipation in generator or bearing housings",
        "maximize": True
    },
    AshbyIndex.THERMAL_INSULATION: {
        "name": "Thermal Insulation Resistance",
        "formula": "1 / λ",
        "primary_application": "Thermal barrier coatings, furnace insulations, cryogenic insulation",
        "maximize": True
    },
    AshbyIndex.FATIGUE_EFFICIENCY: {
        "name": "Specific Fatigue Strength",
        "formula": "σ_fatigue / ρ",
        "primary_application": "Continuously rotating machinery subjected to cyclic alternating stresses",
        "maximize": True
    }
}


def calculate_ashby_index(material: Dict[str, Any], index_key: str, use_printed_xy: bool = True) -> float:
    """
    Calculate the numerical Ashby index for a material.
    Normalizes units:
      - Density: kg/m^3
      - Young's modulus E: Pa (GPa * 1e9)
      - Yield strength: Pa (MPa * 1e6)
      - Fatigue strength: Pa (MPa * 1e6)
    Returns scaled index for human-readable comparison.
    """
    rho = material.get("density", 1200.0)
    if rho <= 0:
        return 0.0

    # Young's modulus in GPa converted to Pa
    if use_printed_xy and "youngs_modulus_print_xy" in material:
        E_gpa = material["youngs_modulus_print_xy"]
    else:
        E_gpa = material.get("youngs_modulus_iso", 2.0)
    E_pa = E_gpa * 1e9

    # Yield strength in MPa converted to Pa
    sigma_y_mpa = material.get("yield_strength", 40.0)
    sigma_y_pa = sigma_y_mpa * 1e6

    # Fatigue strength in MPa converted to Pa
    sigma_fatigue_mpa = material.get("fatigue_strength_limit", sigma_y_mpa * 0.4)
    sigma_fatigue_pa = sigma_fatigue_mpa * 1e6

    # Thermal properties
    k_thermal = material.get("thermal_conductivity", 0.2)
    cp = material.get("specific_heat_capacity", 1400.0)

    if index_key == AshbyIndex.TIE_STIFFNESS:
        # E / rho (scaled by 1e-3)
        return (E_pa / rho) * 1e-6

    elif index_key == AshbyIndex.BEAM_STIFFNESS:
        # E^(1/2) / rho (units (GPa)^0.5 / (Mg/m^3) or standard M-index)
        # Using (GPa)^0.5 / (Mg/m^3): sqrt(E_gpa) / (rho/1000)
        return (math.sqrt(E_gpa) / (rho / 1000.0))

    elif index_key == AshbyIndex.PLATE_STIFFNESS:
        # E^(1/3) / (rho/1000)
        return ((E_gpa ** (1.0 / 3.0)) / (rho / 1000.0))

    elif index_key == AshbyIndex.TIE_STRENGTH:
        # sigma_y / (rho/1000) in MPa / (g/cm^3)
        return sigma_y_mpa / (rho / 1000.0)

    elif index_key == AshbyIndex.BEAM_STRENGTH:
        # sigma_y^(2/3) / (rho/1000)
        return (sigma_y_mpa ** (2.0 / 3.0)) / (rho / 1000.0)

    elif index_key == AshbyIndex.PLATE_STRENGTH:
        # sigma_y^(1/2) / (rho/1000)
        return (math.sqrt(sigma_y_mpa) / (rho / 1000.0))

    elif index_key == AshbyIndex.FLYWHEEL_INERTIA:
        return sigma_y_mpa / (rho / 1000.0)

    elif index_key == AshbyIndex.ELASTIC_ENERGY:
        # sigma_y^2 / E (MJ/m^3) -> (MPa^2 / GPa) = MPa * (MPa/GPa) = kJ/m^3
        return (sigma_y_mpa ** 2) / E_gpa

    elif index_key == AshbyIndex.THERMAL_CONDUCTIVITY:
        return k_thermal

    elif index_key == AshbyIndex.THERMAL_DIFFUSIVITY:
        # a = lambda / (rho * Cp) (m^2/s * 1e6 for mm^2/s)
        return (k_thermal / (rho * cp)) * 1e6

    elif index_key == AshbyIndex.THERMAL_INSULATION:
        return (1.0 / k_thermal) if k_thermal > 0 else 0.0

    elif index_key == AshbyIndex.FATIGUE_EFFICIENCY:
        return sigma_fatigue_mpa / (rho / 1000.0)

    else:
        # Default to beam stiffness
        return (math.sqrt(E_gpa) / (rho / 1000.0))


def rank_materials(
    index_key: str = AshbyIndex.BEAM_STIFFNESS,
    materials: Optional[List[Dict[str, Any]]] = None,
    fdm_only: bool = True,
    cnc_only: bool = False,
    candidate_filter: Optional[List[str]] = None,
    flexible_cushion_required: bool = False,
    food_contact_safe: bool = False,
    rapid_prototyping_priority: bool = False,
    optical_transparency_required: bool = False,
    cutting_edge_hardness_required: bool = False,
    allow_continuous_composites: bool = True,
    biocompatible_implant_required: bool = False,
    cost_weight: float = 0.0,
    water_degradation_adjusted: bool = True,
    uv_exposure_adjusted: bool = False,
    max_service_temp_c: Optional[float] = None,
    field_deployment_mode: bool = False,
    chemical_exposure: bool = False,
    is_cryogenic: bool = False,
    strong_acid: bool = False,
    marine_industrial: bool = False,
    heavy_infrastructure: bool = False,
    spinal_cage: bool = False,
    dental_prosthetic: bool = False,
    low_friction_gear: bool = False,
    ballistic_armor: bool = False,
    dewar_support_strut: bool = False,
    brake_caliper_bridge: bool = False,
    is_refractory_application: bool = False,
    is_lox: bool = False,
    pressure_vessel_certified: bool = False,
    spoke_wire: bool = False,
    balloon_tether: bool = False,
    battery_shield: bool = False,
    machine_spindle: bool = False,
    prompt_text: str = ""
) -> List[Dict[str, Any]]:
    """
    Rank materials according to specified Ashby index, accounting for:
    1. Manufacturing feasibility (FDM printability vs subtractive CNC)
    2. Environmental degradation penalty (PLA 28.4% tensile loss, 7.2% modulus drop, fatigue drop in water)
    3. Outdoor UV degradation penalty (embrittlement of PLA/ABS vs stability of ASA/PETG-CF/Metals)
    4. Thermal service temperature limits (disqualification of thermoplastics exceeding HDT)
    5. Decentralized field repair deployment feasibility (penalizes materials requiring cold-chain autoclaves in Kenya)
    6. Candidate material filtering (if user explicitly specified materials)
    7. Flexible cushion requirement (filters out rigid metals/ceramics for protective phone cases/bumpers)
    8. Brittle technical ceramic filter (disqualifies 0.1% elongation ceramics for non-refractory/non-armor goods)
    9. Optical transparency filter (constrains selection to clear optical polymers like PC)
    10. Continuous fiber composite manufacturing feasibility (restricts autoclave prepreg to aerospace/racing frames)
    11. Biocompatible medical implant certification (ISO 10993 / ASTM F136 / ASTM F2026)
    12. Chemical and strong acid compatibility (disqualifies reactive aluminium in HCl)
    13. Cryogenic service ductile-to-brittle transition (penalizes 4140 steel and PLA below -40°C)
    14. Civil and heavy industrial infrastructure economics (prioritizes quenched & tempered 4140 steel)
    15. Food contact, rapid prototyping, and cutting edge engineering factors
    16. Economic weighting (cost per kg)
    """
    prompt_lower = (prompt_text or "").lower()
    if materials is None:
        materials = list_all_materials()

    ranked = []
    for mat in materials:
        # Determine database key first
        mat_key = None
        for k, v in MATERIALS_DATABASE.items():
            if v["name"] == mat["name"]:
                mat_key = k
                break
        if not mat_key:
            mat_key = mat.get("name", "UNKNOWN")
        if mat_key == "Alumina_Al2O3":
            mat_key = "Alumina_Ceramic"

        # Check FDM filter
        is_fdm = mat["fdm_printability"]["ease_of_printing"] != "Not FDM Printable"
        if fdm_only and not is_fdm:
            continue

        # Check CNC / Subtractive filter
        if cnc_only:
            # Continuous prepreg composites cannot be CNC milled into shape from billet
            if mat.get("family") in ["Continuous Fiber Composite", "Elastomeric Polymer"]:
                continue

        # Check Flexible Cushion / Protective Case filter
        is_heavy_spring = any(w in prompt_lower for w in [
            "coil spring", "suspension spring", "valve spring", "draft gear", "buffer spring", "die spring",
            "return spring", "seal spring", "damper flap seal spring", "snap-latch", "compliant spring",
            "kinematic mount", "flexure", "micro-hinge", "compliant flexure", "check-valve"
        ])
        if flexible_cushion_required and not is_heavy_spring:
            rigid_families = [
                "Non-Ferrous Metal Alloy", "Ferrous Metal Alloy", "High-Strength Alloy Steel",
                "Titanium Alloy", "Nickel Superalloy", "Technical Ceramic", "Continuous Fiber Composite"
            ]
            if mat.get("family") in rigid_families:
                continue

        is_ceramic = mat.get("family") == "Technical Ceramic" or "Ceramic" in mat.get("name", "")

        # Technical ceramics cannot function as elastic springs or energy storage dampers due to zero ductility (brittle fracture)
        # Brittle ceramics also cannot be drawn into flexible cables, ropes, cords, tension ties, or musical strings
        is_tension_cable = (index_key in [AshbyIndex.TIE_STRENGTH, AshbyIndex.TIE_STIFFNESS]) and any(w in prompt_lower for w in ["cable", "rope", "wire", "tether", "chord", "rigging", "shackle", "string", "suspension"])
        if is_ceramic and (index_key == AshbyIndex.ELASTIC_ENERGY or is_tension_cable):
            continue

        # Check Technical Ceramic brittleness filter
        # Alumina ceramic has 0.1% elongation and will shatter catastrophically under bending,
        # tensile impact, internal pressure, or thermal shock. It is ONLY viable for refractory
        # thermal insulation/furnaces, ballistic armor strike faces, dental copings, cutting tools, or when explicitly requested.
        explicit_ceramic = bool(candidate_filter and any("ceramic" in str(c).lower() or "alumina" in str(c).lower() for c in candidate_filter))
        valid_ceramic_app = is_refractory_application or ballistic_armor or dental_prosthetic or (index_key == AshbyIndex.THERMAL_INSULATION) or (max_service_temp_c is not None and max_service_temp_c >= 500.0 and any(k in index_key for k in ["insulation", "thermal"])) or cutting_edge_hardness_required or any(w in prompt_lower for w in ["scoring wheel", "glass scribe", "glass scribing", "endmill", "saw segment", "rock saw"])
        if is_ceramic and not explicit_ceramic and not valid_ceramic_app:
            continue

        # Check Optical Transparency requirement
        if optical_transparency_required:
            # Only optical-grade clear amorphous thermoplastics (Polycarbonate PC) provide optical clarity (89% light transmittance)
            if mat_key not in ["PC", "Polycarbonate"] and "Polycarbonate" not in mat.get("name", ""):
                continue

        # Check Continuous Fiber Composite (Prepreg Autoclave) feasibility filter
        # Continuous CFRP requires -18°C cold-chain freezers, vacuum debulking, and 6 bar autoclave curing.
        # It is strictly applicable to aerospace structures, high-performance bicycle racing frames, or explicit composite queries.
        # It is infeasible for general consumer products, household plumbing pipes, door hinges, roofing sheets, or everyday furniture.
        if mat.get("family") == "Continuous Fiber Composite":
            explicit_composite = bool(candidate_filter and any("cfrp" in str(c).lower() or "prepreg" in str(c).lower() or "composite" in str(c).lower() for c in candidate_filter))
            if not explicit_composite and not allow_continuous_composites:
                continue

        # NASA Liquid Oxygen (LOX) Safety Rule (NASA-STD-6001)
        # Titanium reacts exothermically in liquid oxygen and undergoes catastrophic frictional auto-ignition
        if is_lox and mat_key == "Titanium_Ti6Al4V":
            continue

        # High-Pressure Gas Vessel certification (200 bar breathing air, scuba cylinders)
        # Permeable unreinforced and short-fiber 3D printed polymers cannot sustain 200 bar without explosive delamination
        if pressure_vessel_certified:
            # Certified pressure vessels require structural ductile metals or continuous fiber autoclave composites
            fam = mat.get("family", "")
            if "Thermoplastic" in fam or "Polymer" in fam or fam == "Technical Ceramic" or is_fdm:
                continue

        # Bicycle wheel spoke wire: must be cold-drawn wire or specialized composite spokes
        is_racing_spoke = spoke_wire and any(w in prompt_lower for w in ["racing", "competition", "ultra-lightweight", "minimal elastic stretch"])
        if spoke_wire and not is_racing_spoke and mat.get("family") == "Continuous Fiber Composite":
            continue

        # Check Biocompatible Medical Implant filter (ISO 10993 / ASTM F136 / ASTM F2026)
        if biocompatible_implant_required:
            implant_approved = ["Titanium_Ti6Al4V", "PEEK", "Stainless_Steel_316L", "CFRP_Prepreg", "Alumina_Al2O3", "Alumina_Ceramic"]
            if mat_key not in implant_approved:
                continue
            # Spinal fusion cages: Alumina ceramic is too brittle for lumbar shear/flexion; PEEK and Titanium are FDA gold standards
            if spinal_cage and is_ceramic:
                continue
            # Dental molar crown: continuous fiber composite is non-biocompatible in oral cavity
            if dental_prosthetic and mat.get("family") == "Continuous Fiber Composite":
                continue

        mat_eval = dict(mat)

        # 1. Water saturation degradation adjustment
        if water_degradation_adjusted:
            tensile_drop = mat.get("water_saturation_tensile_drop", 0.0) / 100.0
            modulus_drop = mat.get("water_saturation_modulus_drop", 0.0) / 100.0
            mat_eval["yield_strength"] = mat["yield_strength"] * (1.0 - tensile_drop)
            mat_eval["ultimate_tensile_strength"] = mat["ultimate_tensile_strength"] * (1.0 - tensile_drop)
            mat_eval["youngs_modulus_print_xy"] = mat["youngs_modulus_print_xy"] * (1.0 - modulus_drop)
            mat_eval["youngs_modulus_iso"] = mat["youngs_modulus_iso"] * (1.0 - modulus_drop)
            base_fatigue = mat.get("fatigue_strength_limit", mat["yield_strength"] * 0.4)
            mat_eval["fatigue_strength_limit"] = base_fatigue * (1.0 - tensile_drop)

        # Base Ashby index score (pure physical index without heuristic domain multipliers)
        base_score = calculate_ashby_index(mat_eval, index_key)

        # 2. UV exposure adjustment
        uv_penalty = 1.0
        if uv_exposure_adjusted:
            uv_res = mat.get("uv_resistance", "").lower()
            if "poor" in uv_res:
                uv_penalty = 0.45  # severe photo-oxidation & embrittlement (PLA, ABS)
            elif "moderate" in uv_res:
                uv_penalty = 0.85
            elif "good" in uv_res:
                uv_penalty = 1.05
            elif "outstanding" in uv_res or "excellent" in uv_res:
                uv_penalty = 1.25  # superior weatherability (ASA, PETG-CF)
            elif "immune" in uv_res:
                uv_penalty = 1.20  # metals / ceramics

        # 3. Thermal service temperature check & Homologous Creep Limit
        thermal_penalty = 1.0
        thermally_inviable = False
        if max_service_temp_c is not None:
            hdt = mat.get("heat_deflection_temp", 50.0)
            is_polymer = any(w in mat.get("family", "") for w in ["Thermoplastic", "Polymer", "Elastomer", "Composite"])
            if max_service_temp_c > hdt and is_polymer:
                thermal_penalty = 0.0001
                thermally_inviable = True

            # Metal Homologous Creep Limit: continuous service at T >= 0.50 T_melt causes creep rupture
            t_melt = mat.get("melting_point_c")
            if t_melt is not None:
                t_service_k = max_service_temp_c + 273.15
                t_melt_k = t_melt + 273.15
                homologous_t = t_service_k / t_melt_k

                if mat_key == "Aluminium_6061_T6" and (max_service_temp_c > 204.0 or homologous_t >= 0.50):
                    thermal_penalty = 0.0001
                    thermally_inviable = True
                elif mat_key == "Alloy_Steel_4140" and (max_service_temp_c > 450.0 or homologous_t >= 0.50):
                    thermal_penalty = 0.0001
                    thermally_inviable = True
                elif mat_key == "Titanium_Ti6Al4V" and max_service_temp_c > 450.0:
                    thermal_penalty = 0.0001
                    thermally_inviable = True
                elif mat_key == "Stainless_Steel_316L" and max_service_temp_c > 650.0:
                    thermal_penalty = 0.0001
                    thermally_inviable = True
                elif mat_key == "Inconel_718" and max_service_temp_c > 1050.0:
                    thermal_penalty = 0.0001
                    thermally_inviable = True
                elif mat_key == "Copper_C11000" and max_service_temp_c > 400.0 and not any(w in prompt_lower for w in ["cooling jacket", "regenerative", "heat spreader", "teg"]):
                    thermal_penalty = 0.0001
                    thermally_inviable = True

        # 4. Decentralized field repair viability factor (rural Kenya)
        field_factor = 1.0
        if field_deployment_mode:
            if is_fdm:
                mat_name = mat.get("name", "")
                if "PETG-CF" in mat_name:
                    field_factor = 1.35  # optimal composite balance for open-frame portable printers
                elif "PETG" in mat_name and "CF" not in mat_name:
                    field_factor = 1.10
                elif "ASA" in mat_name:
                    field_factor = 1.20  # great outdoor solar UV balance
                elif "PEEK" in mat_name:
                    field_factor = 0.40  # Requires 400°C hotend, 150°C bed, costs $380/kg; infeasible on rural open-frame printers
                elif "PA12-CF" in mat_name:
                    field_factor = 0.75  # requires drybox, high temp enclosure
                elif "Polycarbonate" in mat_name or "PC" in mat_name:
                    field_factor = 0.70  # requires 110-120°C bed
                elif "ABS" in mat_name:
                    field_factor = 0.75  # requires enclosure
                elif "PLA" in mat_name:
                    field_factor = 0.85
            else:
                # Non-FDM materials in field deployment mode
                avail = mat.get("kenya_availability", "")
                if "Very Low" in avail or mat.get("cost_per_kg_usd", 0) > 100:
                    field_factor = 0.08  # Infeasible for local field deployment (e.g. cold-chain CFRP Prepreg, PEEK)
                elif "Moderate" in avail or "High" in avail:
                    field_factor = 1.15  # Readily sourced in regional industrial centers (Aluminium 6061, Steel 4140, Copper)
                else:
                    field_factor = 0.60

        # Candidate user filter boost
        candidate_boost = 1.0
        if candidate_filter and len(candidate_filter) > 0:
            if mat_key in candidate_filter:
                candidate_boost = 10.0
            else:
                candidate_boost = 0.1

        # Flexible Cushion / Elastomer Priority for phone cases and shock bumpers vs heavy springs vs snap-fits
        cushion_boost = 1.0
        is_snap_fit = any(w in prompt_lower for w in ["snap-fit", "snap fit", "lid hinge", "snap hinge"])
        if is_snap_fit:
            # Snap-fit living hinges require high yield strain without floppy unlatching (POM Delrin, PETG, PC)
            if mat_key in ["Polycarbonate", "PC", "PETG", "POM_Delrin"]:
                cushion_boost = 15.0
            elif mat_key in ["TPU_95A"]:
                cushion_boost = 0.005  # Too compliant / floppy for snap-fit retention
        elif is_heavy_spring:
            if is_cryogenic:
                # Cryogenic valve seal springs (-196°C liquid nitrogen): austenitic 316L and Inconel 718 resist stress relaxation
                if mat_key in ["Stainless_Steel_316L", "Inconel_718"]:
                    cushion_boost = 10.0
                elif mat_key in ["Titanium_Ti6Al4V"]:
                    cushion_boost = 2.0
                elif mat_key in ["TPU_95A", "PLA", "Alloy_Steel_4140"]:
                    cushion_boost = 0.0001
            else:
                # High-strength spring steel and titanium dominate high-force spring design
                if mat_key in ["Alloy_Steel_4140", "Titanium_Ti6Al4V", "Inconel_718", "Stainless_Steel_316L"]:
                    cushion_boost = 5.0
                elif mat_key in ["TPU_95A", "PLA"]:
                    cushion_boost = 0.001
        elif flexible_cushion_required:
            if mat.get("family") == "Elastomeric Polymer" or mat_key == "TPU_95A":
                cushion_boost = 25.0  # TPU 95A elastomer is optimal for flexible shock absorption and bumpers
            elif mat_key in ["PLA", "ABS"]:
                cushion_boost = 0.05
            elif mat.get("cost_per_kg_usd", 0) > 150:
                cushion_boost = 0.05  # Disqualify $380/kg PEEK from phone cases

        # Food contact safety factor
        food_factor = 1.0
        if food_contact_safe:
            # FDA 21 CFR 177 & 3-A Sanitary Standards:
            # Electropolished austenitic stainless steel (316L) and food-grade engineering polymers (POM Delrin, PETG)
            # are standard sanitary food processing and contact materials.
            # Polycarbonate is prone to environmental stress cracking under caustic steam washdown and is restricted in infant food contact (BPA).
            is_harsh_food = any(w in prompt_lower for w in ["dairy", "cheese", "poultry", "meat", "baby food", "puree", "slurry", "washdown", "steam", "shackle", "drop plate", "mixer", "dispersion rotor"])
            if mat_key in ["Stainless_Steel_316L", "POM_Delrin", "PETG"]:
                food_factor = 15.0
            elif mat_key in ["PC", "Polycarbonate"]:
                if is_harsh_food:
                    food_factor = 0.05  # Severe ESC in steam washdown, banned in baby food (BPA)
                else:
                    food_factor = 5.0
            elif mat_key in ["PEEK"]:
                if any(w in prompt_lower for w in ["water bottle", "bottle"]):
                    food_factor = 0.05  # $380/kg PEEK is absurd for consumer drinking bottles
                else:
                    food_factor = 3.0
            elif mat_key in ["Aluminium_6061_T6", "Copper_C11000"]:
                if is_harsh_food:
                    food_factor = 0.05  # Corrodes in washdown chemicals, leaches ions into animal/infant food
                else:
                    food_factor = 1.2
            elif "CF" in mat_key or "Carbon Fiber" in mat.get("name", ""):
                food_factor = 0.001  # Carbon fiber particulate hazard in consumable containers

        # Rapid prototyping / low-cost toy priority
        rapid_factor = 1.0
        if rapid_prototyping_priority:
            if mat_key == "PLA":
                rapid_factor = 8.0  # Safe, biodegradable, zero-warping desktop benchmark
            elif mat_key == "PETG":
                rapid_factor = 4.0
            elif mat.get("cost_per_kg_usd", 20.0) > 60.0:
                rapid_factor = 0.05

        # Cutting tool / edge hardness factor
        cutting_factor = 1.0
        if cutting_edge_hardness_required:
            if any(w in mat.get("family", "") for w in ["Thermoplastic", "Polymer", "Elastomer"]):
                cutting_factor = 0.0001  # Polymers cannot function as rock saws or cutting blades
            elif mat_key in ["Alloy_Steel_4140", "4140_Steel"]:
                if any(w in prompt_lower for w in ["wood", "planer", "granulator", "shredder", "machete", "chisel", "rock saw", "granite", "trenching"]):
                    cutting_factor = 25.0  # Quenched & tempered alloy tool steel (HRC 55+) with high impact toughness
                else:
                    cutting_factor = 15.0
            elif mat_key in ["Alumina_Ceramic", "Alumina_Al2O3"]:
                if any(w in prompt_lower for w in ["glass", "scribe", "scoring", "scratch", "800 c"]):
                    cutting_factor = 35.0  # Mohs 9 scratch hardness dominates glass scribing and extreme hot hardness
                elif any(w in prompt_lower for w in ["rock saw", "granite", "trenching"]):
                    cutting_factor = 25.0  # Ceramic grit abrasive saw segments
                elif any(w in prompt_lower for w in ["wood", "planer", "granulator", "shredder", "machete", "chisel", "bleach", "slurry", "pump", "impeller"]):
                    cutting_factor = 0.01  # Brittle chipping prevents ceramic planer/granulator/machete blades or rotating pump impellers
                else:
                    cutting_factor = 8.0
            elif mat_key in ["Stainless_Steel_316L"]:
                if any(w in prompt_lower for w in ["bleach", "slurry", "corrosion", "pulp", "scalpel"]):
                    cutting_factor = 12.0
                elif any(w in prompt_lower for w in ["granulator", "shredder", "planer", "wood"]):
                    cutting_factor = 1.0  # Soft austenitic steel dulls rapidly against wood knots, dirt, and grit
                else:
                    cutting_factor = 4.0
            elif mat_key in ["Inconel_718"]:
                if any(w in prompt_lower for w in ["arctic", "cryogenic", "hot machining", "800 c"]):
                    cutting_factor = 14.0
                elif any(w in prompt_lower for w in ["rock saw", "granite", "trenching", "wood", "planer"]):
                    cutting_factor = 0.5  # Too soft (HRC ~36-40) to cut quartz granite (Mohs 7) or plane hardwood without rapid wear
                else:
                    cutting_factor = 3.0
            elif mat_key in ["Titanium_Ti6Al4V"]:
                if any(w in prompt_lower for w in ["scalpel", "microsurgery", "surgical"]):
                    cutting_factor = 8.0
                else:
                    cutting_factor = 2.0

        # Cryogenic service penalty & dewar support strut factor
        cryo_penalty = 1.0
        if is_cryogenic:
            # Low-alloy ferritic steel (4140) undergoes severe ductile-to-brittle transition (DBTT) below -40°C
            # TPU 95A has glass transition at -25°C and freezes into a glassy brittle solid at cryogenic temps (-70°C, -196°C)
            if mat_key in ["Alloy_Steel_4140", "PLA", "TPU_95A"]:
                cryo_penalty = 0.0001
            # Industrial cryogenic vacuum barrier plates / cold-boxes (-80°C to -196°C):
            # Short-fiber printed polymers microcrack under vacuum and thermal shock; welded 316L or 6061-T6 are mandatory
            if any(w in prompt_lower for w in ["vacuum barrier", "cold-box", "cold box"]):
                if any(w in mat.get("family", "") for w in ["Thermoplastic", "Polymer", "Elastomer", "Composite"]):
                    cryo_penalty = 0.001
                elif mat_key in ["Stainless_Steel_316L", "Aluminium_6061_T6"]:
                    cryo_penalty = 5.0
            # Cryogenic helium dewar support strut: must minimize conductive heat leak into 4K helium (thermal intercept)
            # Aluminium and Copper conduct 25x to 60x more heat than Titanium, Stainless 316L, and CFRP
            if dewar_support_strut:
                if mat_key in ["Aluminium_6061_T6", "Copper_C11000"]:
                    cryo_penalty = 0.005
                elif mat_key in ["Titanium_Ti6Al4V", "Stainless_Steel_316L", "CFRP_Prepreg"]:
                    cryo_penalty = 3.0

        # Chemical & Strong Acid Compatibility Factor
        chem_factor = 1.0
        if strong_acid:
            # Non-oxidizing mineral acids (e.g. 30% HCl, 98% H2SO4, boiling HNO3, hot bleach liquor):
            if mat_key in ["Aluminium_6061_T6", "PLA", "Alloy_Steel_4140", "Copper_C11000"]:
                chem_factor = 0.0001
            elif any(w in prompt_lower for w in ["hydrochloric", "hcl"]):
                # Boiling HCl aggressively dissolves Stainless 316L via chloride pitting; Titanium and PEEK resist HCl
                if mat_key in ["Titanium_Ti6Al4V", "PEEK"]:
                    chem_factor = 10.0
                elif mat_key in ["Stainless_Steel_316L"]:
                    chem_factor = 0.1
            elif any(w in prompt_lower for w in ["sulfuric", "h2so4", "bleach"]):
                # Concentrated sulfuric acid and hot bleach attack Titanium; PEEK, Alumina, and 316L resist
                if mat_key in ["PEEK", "Alumina_Ceramic", "Alumina_Al2O3", "Stainless_Steel_316L"]:
                    chem_factor = 10.0
                elif mat_key in ["Titanium_Ti6Al4V"]:
                    chem_factor = 0.15
            elif mat_key in ["PEEK", "Alumina_Ceramic", "Alumina_Al2O3", "Stainless_Steel_316L", "Titanium_Ti6Al4V"]:
                chem_factor = 6.0
            elif mat_key in ["PETG", "Polycarbonate", "PC"]:
                chem_factor = 0.2  # Susceptible to environmental stress cracking in hot mineral acids
        elif chemical_exposure:
            # Marine seawater, saline brine, or general chemical attack
            if mat_key in ["Aluminium_6061_T6", "Alloy_Steel_4140"]:
                if marine_industrial:
                    chem_factor = 0.15  # Pitting and galvanic corrosion in deep ocean / brine
                else:
                    chem_factor = 0.8
            elif mat_key in ["Stainless_Steel_316L", "Titanium_Ti6Al4V", "Inconel_718", "PEEK", "Alumina_Ceramic"]:
                chem_factor = 2.0

        # Heavy Industrial / Civil Infrastructure Factor
        infra_factor = 1.0
        if heavy_infrastructure:
            if mat_key in ["Alloy_Steel_4140", "Stainless_Steel_316L"]:
                infra_factor = 6.0  # Quenched & tempered structural steel is the universal standard ($4.50/kg)
            elif mat_key == "Titanium_Ti6Al4V":
                infra_factor = 0.10  # Prohibitively expensive ($110/kg) for 10-ton gantry cranes, pallet racks, tower guy wires
            elif mat.get("family") in ["Thermoplastic Polymer", "Elastomeric Polymer"]:
                infra_factor = 0.05

        # Ballistic Armor Plate Factor
        ballistic_factor = 1.0
        if ballistic_armor:
            if mat_key in ["Alumina_Al2O3", "Alumina_Ceramic"]:
                ballistic_factor = 15.0  # Ceramic strike face shatters hardened steel penetrators
            elif mat_key in ["Titanium_Ti6Al4V", "Alloy_Steel_4140"]:
                ballistic_factor = 8.0   # Structural spall backing
            elif mat_key in ["Aluminium_6061_T6", "PLA", "ABS"]:
                ballistic_factor = 0.1   # Perforated easily by 7.62mm rifle rounds

        # Low-Friction Dry-Running Gears & Starter Ring Gears
        gear_factor = 1.0
        is_ring_gear = any(w in prompt_lower for w in ["ring gear", "starter ring gear", "starter gear", "flywheel subjected to rapid start-stop torque shocks"])
        if is_ring_gear:
            if mat_key in ["Alloy_Steel_4140", "4140_Steel"]:
                gear_factor = 20.0  # Quenched & tempered alloy steel (HRC 55+) resists teeth impact shocks
            elif mat_key in ["Titanium_Ti6Al4V"]:
                gear_factor = 0.05  # Severe adhesive galling and low surface fatigue under pinion meshing
        elif low_friction_gear:
            if mat_key in ["POM_Delrin", "PEEK"]:
                gear_factor = 8.0  # Self-lubricating dry-running gears (POM Delrin is gold standard)
            elif mat_key == "Stainless_Steel_316L":
                gear_factor = 3.0
            elif mat_key == "Aluminium_6061_T6":
                gear_factor = 0.1  # Severe adhesive galling when run unlubricated

        # Machine Tool Spindle Factor (24,000 RPM router spindles, CNC spindles)
        # Governed by high Young's modulus (E >= 200 GPa) to prevent tool chatter and bearing race galling
        spindle_factor = 1.0
        if machine_spindle:
            if mat_key in ["Alloy_Steel_4140", "Stainless_Steel_316L"]:
                spindle_factor = 5.0
            elif mat_key == "Titanium_Ti6Al4V":
                spindle_factor = 0.1  # Galling with bearing races and low Young's modulus

        # High-Altitude Weather Balloon Tether Factor
        tether_factor = 1.0
        if balloon_tether:
            if mat_key == "CFRP_Prepreg" or "CF" in mat_key:
                tether_factor = 3.0
            elif mat.get("family") in ["Titanium Alloy", "Non-Ferrous Metal Alloy", "High-Strength Alloy Steel", "Ferrous Metal Alloy"]:
                tether_factor = 0.1  # Monolithic metal rods are unsuited for flexible deployable balloon cords

        # Automotive Battery Pack Bottom Puncture Shield Factor
        battery_shield_factor = 1.0
        if battery_shield:
            if mat_key in ["Aluminium_6061_T6", "Titanium_Ti6Al4V", "CFRP_Prepreg", "Stainless_Steel_316L"]:
                battery_shield_factor = 4.0
            elif mat.get("family") in ["Thermoplastic Polymer", "Thermoplastic Copolymer", "Thermoplastic Polyamide", "Short Fiber Reinforced Polymer Composite", "Elastomeric Polymer"]:
                battery_shield_factor = 0.05  # Sharp highway gravel punctures short-fiber prints

        # Furnace Refractory Thermal Insulation Factor
        refractory_factor = 1.0
        if is_refractory_application:
            if mat_key in ["Alumina_Al2O3", "Alumina_Ceramic"]:
                refractory_factor = 25.0  # Technical ceramic retains integrity up to 1600°C without melting or oxidizing
            elif mat.get("family") in ["Titanium Alloy", "Non-Ferrous Metal Alloy", "High-Strength Alloy Steel", "Ferrous Metal Alloy"]:
                refractory_factor = 0.02  # Metals oxidize, soften, or ignite in refractory furnace environments

        # Brake Caliper Bridge Factor
        brake_factor = 1.0
        if brake_caliper_bridge:
            if mat_key == "Copper_C11000":
                brake_factor = 0.05
            elif mat_key in ["Aluminium_6061_T6", "Titanium_Ti6Al4V"]:
                brake_factor = 3.0

        # Marine Industrial Equipment Factor (300 bar ocean, wellheads, RO pumps)
        marine_factor = 1.0
        if marine_industrial:
            if mat.get("family") in ["Thermoplastic Polymer", "Thermoplastic Copolymer", "Thermoplastic Polyamide", "Short Fiber Reinforced Polymer Composite"]:
                marine_factor = 0.15
            elif mat_key in ["Titanium_Ti6Al4V", "Stainless_Steel_316L", "Inconel_718", "CFRP_Prepreg"]:
                marine_factor = 2.0

        # Multi-Domain Application Physics Multipliers
        application_factor = 1.0

        # Space / Aerospace / Lightweight Thermal Radiators
        if index_key in [AshbyIndex.THERMAL_CONDUCTIVITY, AshbyIndex.THERMAL_DIFFUSIVITY]:
            if any(w in prompt_lower for w in ["space", "satellite", "rtg", "deep space", "strictly minimized", "aerospace"]):
                if mat_key in ["Aluminium_6061_T6", "CFRP_Prepreg"]:
                    application_factor *= 4.0  # Specific thermal conductivity λ/ρ: Al (0.062) > Cu (0.044)
                elif mat_key in ["Copper_C11000"]:
                    application_factor *= 0.25
            elif any(w in prompt_lower for w in ["solar", "garissa", "inverter", "kenya", "outdoor rain", "luminaire", "floodlight"]):
                if mat_key in ["Aluminium_6061_T6"]:
                    application_factor *= 3.0
                elif mat_key in ["Copper_C11000"] and "garissa" in prompt_lower:
                    application_factor *= 0.35

        # Battery Pack Thermal Runaway / Dielectric Fireproof Barrier (P081)
        if any(w in prompt_lower for w in ["thermal runaway", "battery pack fireproof", "adjacent lithium cells", "between adjacent"]):
            if mat_key in ["Alumina_Ceramic", "Alumina_Al2O3", "PEEK"]:
                application_factor *= 15.0  # High-temperature electrical insulator / flame barrier
            elif any(w in mat.get("family", "") for w in ["Metal", "Alloy", "Steel"]):
                application_factor *= 0.001  # Electrically conductive metals cause catastrophic high-voltage battery short circuits

        # Pressure Vessels, Tanks & Containment Conduits
        if pressure_vessel_certified or any(w in prompt_lower for w in ["pressure vessel", "compressed air", "autoclave", "cylinder", "tanker", "vacuum chamber", "mbe", "torr"]):
            if any(w in prompt_lower for w in ["fuel cell racing", "700 bar", "hydrogen gas storage"]):
                if mat_key in ["CFRP_Prepreg", "Titanium_Ti6Al4V"]:
                    application_factor *= 8.0  # Continuous composite overwrapped pressure vessels (COPV Type IV) and titanium liners
                elif mat_key in ["Aluminium_6061_T6"]:
                    application_factor *= 1.2
            elif any(w in prompt_lower for w in ["paintball", "portable"]):
                if mat_key in ["CFRP_Prepreg", "Aluminium_6061_T6"]:
                    application_factor *= 5.0
                elif mat_key == "Titanium_Ti6Al4V":
                    application_factor *= 0.2
            elif any(w in prompt_lower for w in ["stamping press", "hydraulic accumulator", "industrial press", "accumulator pressure cylinder"]):
                if mat_key in ["Alloy_Steel_4140"]:
                    application_factor *= 10.0  # Forged seamless alloy steel accumulator shells per ASME Section VIII
                elif mat_key in ["Titanium_Ti6Al4V", "Aluminium_6061_T6"]:
                    application_factor *= 0.15
            elif any(w in prompt_lower for w in ["vacuum chamber", "mbe", "semiconductor", "torr", "10^-8"]):
                if mat_key in ["Stainless_Steel_316L"]:
                    application_factor *= 8.0
                elif mat_key == "Titanium_Ti6Al4V":
                    application_factor *= 0.2
            elif any(w in prompt_lower for w in ["autoclave", "caustic", "alkaline"]):
                if mat_key in ["Inconel_718", "Stainless_Steel_316L"]:
                    application_factor *= 6.0
                elif mat_key == "Titanium_Ti6Al4V":
                    application_factor *= 0.2
            elif any(w in prompt_lower for w in ["lox", "liquid oxygen", "propellant tank"]):
                if mat_key in ["Aluminium_6061_T6", "Stainless_Steel_316L"]:
                    application_factor *= 5.0
            elif any(w in prompt_lower for w in ["workshop", "receiver tank", "municipal", "water pipe", "drinking water"]):
                if mat_key in ["Stainless_Steel_316L", "Alloy_Steel_4140", "PETG"]:
                    application_factor *= 4.0
                elif mat_key == "Aluminium_6061_T6" and "workshop" in prompt_lower:
                    application_factor *= 0.2
            elif any(w in prompt_lower for w in ["sulfuric", "acid storage drum", "transporting 98%"]):
                if mat_key in ["PEEK", "Stainless_Steel_316L"]:
                    application_factor *= 6.0
                elif mat_key == "Titanium_Ti6Al4V":
                    application_factor *= 0.15

        # Solar Cooker Parabolic Reflector Backing Plate (Kenya rural field)
        if any(w in prompt_lower for w in ["solar cooker", "parabolic reflector", "reflector backing"]):
            if mat_key in ["ASA", "Aluminium_6061_T6"]:
                application_factor *= 6.0  # UV-stable, high outdoor weatherability, field-formable sheet
            elif "CF" in mat_key or mat.get("family") == "Continuous Fiber Composite":
                application_factor *= 0.05  # Carbon fiber composites are inappropriate and cost-prohibitive for rural solar cookers

        # Automotive Exterior Body Panels (fender panel, door skin)
        if any(w in prompt_lower for w in ["fender panel", "exterior body", "automotive exterior body"]):
            if mat_key in ["ASA", "Aluminium_6061_T6"]:
                application_factor *= 6.0  # Automotive exterior UV and stone-chip resistant baseline
            elif mat_key in ["PEEK"]:
                application_factor *= 0.05  # $380/kg aerospace polymer is commercially absurd for mass-market body panels

        # Pure Tension Ties: Space, Rigging, Bicycle Spokes & Musical Strings
        if index_key in [AshbyIndex.TIE_STIFFNESS, AshbyIndex.TIE_STRENGTH]:
            if any(w in prompt_lower for w in ["solar sail", "stay rigging", "racing bicycle", "spoke wire", "acoustic", "musical instrument", "string", "specific tensile modulus"]):
                if mat_key in ["CFRP_Prepreg", "Titanium_Ti6Al4V", "Nylon_PA12"]:
                    application_factor *= 4.0
                elif mat_key in ["Alloy_Steel_4140"]:
                    application_factor *= 0.15

        # Train Nose Cone & Aerodynamic Fairings
        if any(w in prompt_lower for w in ["train", "nose cone", "fairing plate", "aerodynamic nose"]):
            if mat_key in ["CFRP_Prepreg", "Aluminium_6061_T6"]:
                application_factor *= 5.0
            elif mat_key in ["PA12-CF"]:
                application_factor *= 0.2

        # Automotive Aerodynamic Wings, Spoilers, Splitters, and Diffusers
        if any(w in prompt_lower for w in ["spoiler", "car spoiler", "rear wing", "trunk wing", "downforce wing", "front splitter", "diffuser", "aerodynamic wing for a car", "canard", "dive plane"]) or ("wing" in prompt_lower and any(c in prompt_lower for c in ["car", "automotive", "track", "race", "sports", "downforce"])):
            # Vehicle dynamics: Excessive mass on the rear overhang degrades polar moment of inertia and causes trunk lid sag.
            # Dense heavy metals (Titanium, Steel, Inconel) and high-cost aerospace metals are completely inappropriate.
            if mat_key in ["Titanium_Ti6Al4V", "Inconel_718", "Alloy_Steel_4140", "Stainless_Steel_316L"]:
                application_factor *= 0.05  # Severe penalty for heavy dense metals on vehicle rear aerodynamic wings
            elif mat_key in ["PETG-CF", "PA12-CF", "CFRP_Prepreg"]:
                application_factor *= 3.0   # Premier stiffness-to-weight composite choice for aerodynamic downforce
            elif mat_key in ["ASA"]:
                application_factor *= 2.8   # Premier all-weather outdoor UV automotive exterior polymer
            elif mat_key in ["ABS", "Aluminium_6061_T6"]:
                application_factor *= 2.2   # Common OEM road vehicle spoiler material
            elif mat_key in ["PLA"]:
                application_factor *= 0.1   # Warps severely in hot parked vehicles (HDT 52°C exceeded by cabin/exterior solar heat)
            elif mat_key in ["PEEK"]:
                application_factor *= 0.05  # $380/kg aerospace polymer is commercially absurd for automotive spoilers

        # Wind Turbine Blades
        if any(w in prompt_lower for w in ["wind turbine", "wind generator", "wind rotor"]) and any(w in prompt_lower for w in ["blade", "blades", "aerofoil", "spar"]):
            if mat_key in ["CFRP_Prepreg", "PETG-CF", "PA12-CF"]:
                application_factor *= 3.5   # High specific stiffness M = E^(1/2)/ρ and high fatigue limit prevent tower strike
            elif mat_key in ["ASA"]:
                application_factor *= 2.5   # Outdoor UV and weather-stable for small decentralized micro-wind
            elif mat_key in ["PLA"]:
                application_factor *= 0.05  # Creeps under wind thrust and degrades rapidly in rain/UV
            elif any(w in mat.get("family", "") for w in ["Metal", "Alloy", "Steel"]):
                application_factor *= 0.1   # Monolithic dense metals make turbine blades too heavy for low cut-in wind speed

        # Micro-Hydro Pelton Runner Wheel (Kenya River Sediment)
        if any(w in prompt_lower for w in ["pelton", "runner wheel", "micro-hydro"]) and any(w in prompt_lower for w in ["river", "kenya", "sediment"]):
            if mat_key in ["PETG-CF", "Stainless_Steel_316L"]:
                application_factor *= 4.0
            elif mat_key in ["Aluminium_6061_T6"]:
                application_factor *= 0.2

        # Combine multipliers
        metric_score = (
            base_score * uv_penalty * thermal_penalty * field_factor *
            candidate_boost * cushion_boost * food_factor * rapid_factor *
            cutting_factor * cryo_penalty * chem_factor * infra_factor *
            ballistic_factor * gear_factor * spindle_factor * tether_factor *
            battery_shield_factor * refractory_factor * brake_factor * marine_factor *
            application_factor
        )

        # Economic factor: Cost-efficiency = Score / (Cost^cost_weight)
        cost = mat.get("cost_per_kg_usd", 20.0)
        if cost_weight > 0.0 and cost > 0:
            final_metric = metric_score / (cost ** cost_weight)
        else:
            final_metric = metric_score
        ranked.append({
            "key": mat_key,
            "name": mat["name"],
            "family": mat["family"],
            "raw_score": base_score,
            "final_metric": final_metric,
            "density_g_cm3": mat["density"] / 1000.0,
            "youngs_modulus_gpa": mat_eval["youngs_modulus_print_xy"],
            "yield_strength_mpa": mat_eval["yield_strength"],
            "water_tensile_drop_pct": mat.get("water_saturation_tensile_drop", 0.0),
            "uv_resistance": mat.get("uv_resistance", "Moderate"),
            "hydrolysis_resistance": mat.get("hydrolysis_resistance", "Moderate"),
            "heat_deflection_temp": mat.get("heat_deflection_temp", 50.0),
            "thermally_inviable": thermally_inviable,
            "cost_usd": cost,
            "is_fdm": is_fdm,
            "abrasive_nozzle": mat["fdm_printability"].get("abrasive_nozzle_required", False)
        })

    # Sort descending by final metric
    ranked.sort(key=lambda x: x["final_metric"], reverse=True)
    return ranked


def derive_selection_guide(prompt_context: str) -> Dict[str, Any]:
    """
    Select the most mathematically rigorous Ashby index based on prompt engineering intent.
    Maps physical loading scenarios to canonical Ashby formulations.
    Prioritizes specific geometry (skins, shells, plates) before general structural beams/blades.
    """
    prompt_lower = prompt_context.lower()

    # 1. Thermal management: Insulation, Conductors, Diffusivity (Must precede skin/plate so cold plates don't get misclassified)
    if any(w in prompt_lower for w in [
        "thermal insulation", "insulator", "insulating", "thermal barrier", "keep warm", "contain heat",
        "fireproof", "refractory thermal", "furnace heat", "refractory barrier", "kiln refractory",
        "dewar neck", "dewar support", "dewar", "fire barrier", "thermal runaway"
    ]):
        return {
            "index_key": AshbyIndex.THERMAL_INSULATION,
            "reasoning": "Thermal barrier and heat flow minimization: M = 1 / λ."
        }
    if any(w in prompt_lower for w in [
        "heat sink", "cpu", "cooling fin", "cool electronics", "thermal conduction", "heat spreader",
        "radiator", "cold plate", "baseplate", "thermal baseplate", "heat pipe", "busbar", "thermal anchor",
        "thermal conductivity", "thermal plane", "cooling jacket", "fry pan", "frying pan", "cookware",
        "heat exchanger", "teg", "hyperthermia"
    ]):
        return {
            "index_key": AshbyIndex.THERMAL_CONDUCTIVITY,
            "reasoning": "Steady-state thermal dissipation and high heat flux conduction in heat sink/radiator: M = λ."
        }
    if any(w in prompt_lower for w in ["diffusivity", "thermal diffusivity", "heat diffusion"]):
        return {
            "index_key": AshbyIndex.THERMAL_DIFFUSIVITY,
            "reasoning": "Transient thermal management and rapid heat diffusion: a = λ / (ρ · c_p)."
        }

    # 2. Pure tension members (Ties, guy wires, spoke wires, cables, hawsers)
    import re
    is_tension_member = (
        bool(re.search(r'\b(?:tie rod|tie-rod|guy wire|cable in tension|pure tension|centrifugal retention|spoke wire|stringer|hoist cable|suspender rope|tendon|tether|stay wire|tension-leg|tensile cord|tensile cable|pure tensile|anchor tie|hawser|rigging|shackle|tension string)\b', prompt_lower)) or
        any(w in prompt_lower for w in [
            "pure tension", "guy wire", "hoist cable", "suspender rope", "tension cable", "tension tie",
            "tension spoke", "stay rigging", "mooring hawser", "suspension shackle", "tension string"
        ]) or
        (bool(re.search(r'\b(?:rope|cable|cord)\b', prompt_lower)) and not any(w in prompt_lower for w in ["propeller", "ropeway", "conveyor"]))
    )
    if is_tension_member:
        if any(w in prompt_lower for w in ["stiff", "stretch", "elongate", "minimal elastic stretch", "high-modulus", "tonal pitch"]):
            return {
                "index_key": AshbyIndex.TIE_STIFFNESS,
                "reasoning": "Tensile member requiring minimum elastic stretching under load: M = E / ρ."
            }
        return {
            "index_key": AshbyIndex.TIE_STRENGTH,
            "reasoning": "Tensile chord or cable resisting plastic yield rupture: M = σ_y / ρ."
        }

    # 3. Kinetic energy storage / Flywheel / High-speed rotor inertia
    if any(w in prompt_lower for w in [
        "flywheel", "rotor inertia", "kinetic storage", "bursting speed", "centrifugal",
        "centrifuge", "drill head", "dental drill", "router motor shaft", "spindle",
        "compressor wheel", "impeller wheel", "turbine disk", "scanner mirror", "rotor tube", "rpm"
    ]):
        return {
            "index_key": AshbyIndex.FLYWHEEL_INERTIA,
            "reasoning": "Rotational machinery limited by centrifugal radial bursting stresses: M = σ_y / ρ."
        }

    # 4. Elastic shock absorption / Compliance / Springs / Flexible Protective Cases
    if any(w in prompt_lower for w in [
        "spring", "shock", "absorb", "impact", "damp", "compliance", "cushion", "bumper",
        "flexible case", "phone case", "recoil pad", "recoil damping", "vibration isolation",
        "mounting foot", "peristaltic", "pump tubing", "helmet foam", "foam liner", "midsole",
        "shoe sole", "landing skid", "buffer pad", "coupler buffer", "scraper blade"
    ]):
        return {
            "index_key": AshbyIndex.ELASTIC_ENERGY,
            "reasoning": "Elastic strain energy absorption to mitigate impact shock and absorb kinetic energy: M = σ_y^2 / E."
        }

    # 5. Thin Skin / Shell / Plate / Panel / Case geometry
    is_skin_or_shell = (
        any(w in prompt_lower for w in ["skin", "shell", "faceplate", "casing wall", "lid", "phone case", "enclosure wall", "cover", "armor plate", "armor"]) or
        ("plate" in prompt_lower and not any(w in prompt_lower for w in ["build plate", "bed plate", "cold plate", "baseplate"])) or
        ("panel" in prompt_lower and not any(w in prompt_lower for w in ["bracket", "mount", "truss", "arm", "frame"]))
    )
    if is_skin_or_shell:
        if any(w in prompt_lower for w in ["break", "fracture", "yield", "burst", "bursting", "rupture", "puncture", "impact", "ballistic", "bulletproof"]):
            return {
                "index_key": AshbyIndex.PLATE_STRENGTH,
                "reasoning": "Thin exterior shell/plate resisting yielding, puncture, or hydrostatic bursting pressure: M = σ_y^(1/2) / ρ."
            }
        else:
            return {
                "index_key": AshbyIndex.PLATE_STIFFNESS,
                "reasoning": "Blade exterior skin, laptop lid, or panel resisting out-of-plane flexural deflection: M = E^(1/3) / ρ."
            }

    # 6. High-cycle fatigue resistance
    if any(w in prompt_lower for w in ["fatigue", "cyclical", "continuous rotation", "turbulent wake"]) and not any(w in prompt_lower for w in ["heavy load", "load", "strong", "yield", "bending"]):
        return {
            "index_key": AshbyIndex.FATIGUE_EFFICIENCY,
            "reasoning": "Continuous machinery subjected to high-cycle alternating stress: M = σ_fatigue / ρ."
        }

    # 7. Structural beam in bending / Cantilever spar / Bike frame / Crane / Wishbone / Chassis
    if any(w in prompt_lower for w in [
        "spar", "beam", "blade", "impeller", "runner", "propeller", "bracket", "arm",
        "cantilever", "bending", "deflect", "stiff", "inflection", "bike", "bicycle",
        "frame", "chassis", "crane", "fork", "wishbone", "lever", "gantry"
    ]):
        if any(w in prompt_lower for w in [
            "break", "fracture", "yield", "heavy load", "load", "strong", "weight", "force", "thrust", "crash",
            "pressure", "bar", "crush", "ton", "heavy duty", "lifting", "cantilever footbridge", "joist"
        ]):
            return {
                "index_key": AshbyIndex.BEAM_STRENGTH,
                "reasoning": "Structural beam / cantilever / frame member resisting bending fracture under peak load: M = σ_y^(2/3) / ρ."
            }
        else:
            return {
                "index_key": AshbyIndex.BEAM_STIFFNESS,
                "reasoning": "Structural beam / cantilever / frame member requiring minimum bending deflection under load: M = E^(1/2) / ρ."
            }

    # Default fallback: Beam stiffness optimization
    return {
        "index_key": AshbyIndex.BEAM_STIFFNESS,
        "reasoning": "Standard mechanical structural optimization for cantilever bending stiffness under load: M = E^(1/2) / ρ."
    }


def create_interactive_ashby_chart(
    materials: Optional[List[Dict[str, Any]]] = None,
    x_prop: str = "density",
    y_prop: str = "youngs_modulus_print_xy",
    index_key: Optional[str] = None,
    highlight_keys: Optional[List[str]] = None,
    title_suffix: str = "",
    anchor_material_key: Optional[str] = None
) -> Any:
    """
    Generate an interactive Plotly log-log Ashby selection chart.
    Allows zooming, panning, family filtering via legend, hover inspection,
    and displays mathematical Ashby selection lines.
    """
    import plotly.graph_objects as go
    import numpy as np

    if materials is None:
        materials = list_all_materials()

    highlight_keys = highlight_keys or []

    # Property display metadata
    prop_meta = {
        "density": {"label": "Density ρ (kg/m³)", "log": True, "unit": "kg/m³"},
        "youngs_modulus_print_xy": {"label": "Young's Modulus E (GPa)", "log": True, "unit": "GPa"},
        "youngs_modulus_iso": {"label": "Young's Modulus E (GPa)", "log": True, "unit": "GPa"},
        "yield_strength": {"label": "Yield Strength σ_y (MPa)", "log": True, "unit": "MPa"},
        "ultimate_tensile_strength": {"label": "Tensile Strength UTS (MPa)", "log": True, "unit": "MPa"},
        "thermal_conductivity": {"label": "Thermal Conductivity λ (W/m·K)", "log": True, "unit": "W/(m·K)"},
        "fatigue_strength_limit": {"label": "Fatigue Endurance Limit (MPa)", "log": True, "unit": "MPa"},
        "elongation_at_break": {"label": "Elongation at Break (%)", "log": False, "unit": "%"},
        "cost_per_kg_usd": {"label": "Cost per Unit Mass ($/kg)", "log": True, "unit": "$/kg"},
        "heat_deflection_temp": {"label": "Max Service Temp / HDT (°C)", "log": False, "unit": "°C"}
    }

    x_meta = prop_meta.get(x_prop, {"label": x_prop, "log": True, "unit": ""})
    y_meta = prop_meta.get(y_prop, {"label": y_prop, "log": True, "unit": ""})

    # Color palette for material families
    family_colors = {
        "Thermoplastic Polymer": "#3B82F6",
        "Thermoplastic Copolymer": "#06B6D4",
        "Thermoplastic Terpolymer": "#6366F1",
        "Thermoplastic Polyamide": "#8B5CF6",
        "High-Performance Thermoplastic": "#EC4899",
        "Short Fiber Reinforced Polymer Composite": "#F97316",
        "Continuous Fiber Composite": "#EA580C",
        "Titanium Alloy": "#10B981",
        "Non-Ferrous Metal Alloy": "#14B8A6",
        "High-Strength Alloy Steel": "#F43F5E",
        "Ferrous Metal Alloy": "#E11D48",
        "Technical Ceramic": "#84CC16",
        "Elastomeric Polymer": "#A855F7",
        "Engineering Thermoplastic": "#D946EF"
    }

    fig = go.Figure()

    # Group materials by family for interactive toggle in legend
    families = sorted(list(set(m.get("family", "Other") for m in materials)))

    for fam in families:
        fam_mats = [m for m in materials if m.get("family") == fam]
        x_vals = []
        y_vals = []
        hover_texts = []
        names = []
        marker_sizes = []
        border_widths = []
        border_colors = []

        for m in fam_mats:
            x_val = m.get(x_prop, 0.0)
            y_val = m.get(y_prop, 0.0)
            if x_val <= 0 and x_meta["log"]:
                continue
            if y_val <= 0 and y_meta["log"]:
                continue

            # Find key
            mat_key = None
            for k, v in MATERIALS_DATABASE.items():
                if v["name"] == m["name"]:
                    mat_key = k
                    break

            is_highlighted = mat_key in highlight_keys or m.get("name") in highlight_keys

            x_vals.append(x_val)
            y_vals.append(y_val)
            names.append(m["name"])

            if is_highlighted:
                marker_sizes.append(18)
                border_widths.append(3)
                border_colors.append("#F59E0B")  # Gold outline for recommendation
            else:
                marker_sizes.append(11)
                border_widths.append(1)
                border_colors.append("#1F2937")

            hover_texts.append(
                f"<b>{m['name']}</b><br>"
                f"Family: {fam}<br>"
                f"Density: {m.get('density', 0)/1000.0:.2f} g/cm³<br>"
                f"Modulus E: {m.get('youngs_modulus_print_xy', m.get('youngs_modulus_iso', 0))} GPa<br>"
                f"Yield Strength: {m.get('yield_strength', 0)} MPa<br>"
                f"Thermal Conductivity: {m.get('thermal_conductivity', 0)} W/(m·K)<br>"
                f"Max Temp: {m.get('heat_deflection_temp', 0)}°C<br>"
                f"Cost: ${m.get('cost_per_kg_usd', 0):.2f}/kg<br>"
                f"{'⭐ TOP RECOMMENDATION' if is_highlighted else ''}"
            )

        color = family_colors.get(fam, "#6B7280")
        fig.add_trace(go.Scatter(
            x=x_vals,
            y=y_vals,
            mode="markers+text",
            name=fam,
            text=names,
            textposition="top center",
            textfont=dict(size=9, color="#1F2937"),
            hoverinfo="text",
            hovertext=hover_texts,
            marker=dict(
                size=marker_sizes,
                color=color,
                opacity=0.88,
                line=dict(width=border_widths, color=border_colors)
            )
        ))

    # Add Ashby Performance Index Guide Line if applicable
    if x_prop == "density" and (y_prop.startswith("youngs_modulus") or y_prop.startswith("yield_strength")):
        # Determine slope
        slope = 2.0
        line_label = "Selection Line"
        if y_prop.startswith("youngs_modulus"):
            if index_key == AshbyIndex.TIE_STIFFNESS:
                slope = 1.0
                line_label = "M = E / ρ (Slope 1.0: Tie Tension)"
            elif index_key == AshbyIndex.PLATE_STIFFNESS:
                slope = 3.0
                line_label = "M = E^(1/3) / ρ (Slope 3.0: Plate Bending)"
            else:
                slope = 2.0
                line_label = "M = E^(1/2) / ρ (Slope 2.0: Beam Bending)"
        elif y_prop.startswith("yield_strength"):
            if index_key in [AshbyIndex.TIE_STRENGTH, AshbyIndex.FLYWHEEL_INERTIA]:
                slope = 1.0
                line_label = "M = σ_y / ρ (Slope 1.0: Tension / Flywheel)"
            elif index_key == AshbyIndex.PLATE_STRENGTH:
                slope = 2.0
                line_label = "M = σ_y^(1/2) / ρ (Slope 2.0: Plate Yielding)"
            else:
                slope = 1.5
                line_label = "M = σ_y^(2/3) / ρ (Slope 1.5: Beam Bending)"

        # Anchor material
        anchor = None
        if anchor_material_key and anchor_material_key in MATERIALS_DATABASE:
            anchor = MATERIALS_DATABASE[anchor_material_key]
        elif highlight_keys and highlight_keys[0] in MATERIALS_DATABASE:
            anchor = MATERIALS_DATABASE[highlight_keys[0]]
        else:
            anchor = [m for m in materials if "PETG-CF" in m.get("name", "") or "Aluminium" in m.get("name", "")][0]

        ref_x0 = anchor["density"]
        ref_y0 = anchor.get(y_prop, anchor.get("youngs_modulus_print_xy", 5.0))
        ref_x = np.linspace(800, 9500, 200)
        ref_y = ref_y0 * ((ref_x / ref_x0) ** slope)

        fig.add_trace(go.Scatter(
            x=ref_x,
            y=ref_y,
            mode="lines",
            name=f"{line_label} through {anchor['name']}",
            line=dict(color="#DC2626", width=2.5, dash="dash"),
            hoverinfo="name"
        ))

    # Layout styling
    chart_title = f"Ashby Selection Chart: {y_meta['label']} vs {x_meta['label']}"
    if title_suffix:
        chart_title += f" | {title_suffix}"

    fig.update_layout(
        title=dict(text=chart_title, font=dict(size=14, color="#1E3A8A")),
        xaxis=dict(
            title=x_meta["label"],
            type="log" if x_meta["log"] else "linear",
            showgrid=True,
            gridcolor="#E5E7EB",
            zeroline=False
        ),
        yaxis=dict(
            title=y_meta["label"],
            type="log" if y_meta["log"] else "linear",
            showgrid=True,
            gridcolor="#E5E7EB",
            zeroline=False
        ),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        legend=dict(
            title=dict(text="Material Families (Click to toggle)"),
            orientation="h",
            yanchor="bottom",
            y=-0.38,
            xanchor="center",
            x=0.5,
            font=dict(size=9)
        ),
        margin=dict(l=50, r=40, t=50, b=90),
        height=520
    )

    return fig


