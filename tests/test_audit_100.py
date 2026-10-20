"""
Comprehensive 100-Question Multi-Domain Engineering Stress Test Suite.
Verifies that the Material Selection System derives recommendations dynamically
from Michael Ashby optimization physics, continuum mechanics, environmental
degradation kinetics, and regulatory standards across 100 challenging scenarios.

Loading Modes (8):
  - Bending Beams (P001 - P013)
  - Tensile Ties (P014 - P026)
  - Shell Plates (P027 - P039)
  - Rotational Rotors (P040 - P051)
  - Elastic Springs / Dampers (P052 - P063)
  - Industrial Cutting Tools (P064 - P075)
  - Thermal Conductors & Insulators (P076 - P088)
  - Pressure Vessels & Containment (P089 - P100)

Operating Environments (6):
  - Submerged Freshwater / Marine Saline
  - Intense Solar UV Weathering
  - Cryogenic Temperatures (-50°C to -269°C)
  - Extreme Furnace Heat (up to 1100°C)
  - Corrosive Chemicals / Strong Mineral Acids
  - Ultra-High Vacuum / Space

Regulatory & Operational Constraints (6):
  - ISO 10993 Biomedical Implants
  - FDA 21 CFR 177 Food Contact Sanitary
  - Optical Transparency (>85% transmission)
  - Ultra-Lightweight Racing / Aerospace
  - Heavy Crane Hoisting & Fail-Safe Toughness
  - Decentralized Rural Micro-Grids (Kenya Baseline)
"""

import math
import pytest
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

from src.nlp_parser import NLPTranslationLayer
from src.ashby_engine import AshbyIndex, calculate_ashby_index
from src.materials_db import MATERIALS_DATABASE
from src.rag_engine import RAGEngine
from src.llm_orchestrator import LLMOrchestrator


@dataclass
class EngineeringAuditTestCase:
    test_id: str
    prompt_text: str
    cluster: str
    loading_mode: str
    operating_environment: str
    regulatory_domain: str
    expected_indices: List[str]
    expected_top_materials: List[str]
    mandatory_disqualified: List[str]
    service_temperature_c: Optional[float] = None


# Authoritative 100-Prompt Audit Catalog (P001 - P100)
AUDIT_TEST_CASES: Dict[str, EngineeringAuditTestCase] = {
    # -------------------------------------------------------------------------
    # Cluster 1: Bending Beams & Cantilever Structures (P001 - P013)
    # -------------------------------------------------------------------------
    "P001": EngineeringAuditTestCase(
        test_id="P001",
        prompt_text="I want to make a blade that will push water, carry a heavy load, and sit in a river all day, but I don't know the exact weight.",
        cluster="Bending Beams",
        loading_mode="bending_beam",
        operating_environment="submerged_freshwater",
        regulatory_domain="rural_field_kenya",
        expected_indices=["beam_strength"],
        expected_top_materials=["PETG-CF"],
        mandatory_disqualified=["PLA", "PEEK"],
    ),
    "P002": EngineeringAuditTestCase(
        test_id="P002",
        prompt_text="High-speed hydrofoil strut operating in corrosive saltwater at 35 knots, requiring maximum flexural stiffness to prevent hydrodynamic flutter.",
        cluster="Bending Beams",
        loading_mode="bending_beam",
        operating_environment="marine_saltwater",
        regulatory_domain="ultra_lightweight_racing",
        expected_indices=["beam_stiffness"],
        expected_top_materials=["CFRP_Prepreg", "Titanium_Ti6Al4V"],
        mandatory_disqualified=["Alloy_Steel_4140", "PLA"],
    ),
    "P003": EngineeringAuditTestCase(
        test_id="P003",
        prompt_text="Outdoor cantilever mounting spar for solar tracking panels in Garissa under equatorial UV radiation and high wind gusts.",
        cluster="Bending Beams",
        loading_mode="bending_beam",
        operating_environment="solar_uv_equatorial",
        regulatory_domain="weathering_outdoor",
        expected_indices=["beam_stiffness"],
        expected_top_materials=["ASA", "PETG-CF", "Aluminium_6061_T6"],
        mandatory_disqualified=["ABS", "PLA"],
    ),
    "P004": EngineeringAuditTestCase(
        test_id="P004",
        prompt_text="Tour de France competition road bicycle front fork requiring maximum bending rigidity per unit weight and road vibration damping.",
        cluster="Bending Beams",
        loading_mode="bending_beam",
        operating_environment="ambient",
        regulatory_domain="ultra_lightweight_racing",
        expected_indices=["beam_stiffness"],
        expected_top_materials=["CFRP_Prepreg", "Titanium_Ti6Al4V"],
        mandatory_disqualified=["Alloy_Steel_4140", "TPU_95A"],
    ),
    "P005": EngineeringAuditTestCase(
        test_id="P005",
        prompt_text="Cryogenic liquid nitrogen transfer pipe support beam operating at -196 C subject to cantilever bending loads.",
        cluster="Bending Beams",
        loading_mode="bending_beam",
        operating_environment="cryogenic",
        regulatory_domain="cryogenic_toughness",
        expected_indices=["beam_strength", "beam_stiffness"],
        expected_top_materials=["Stainless_Steel_316L", "Titanium_Ti6Al4V"],
        mandatory_disqualified=["Alloy_Steel_4140", "PLA", "PETG"],
        service_temperature_c=-196.0,
    ),
    "P006": EngineeringAuditTestCase(
        test_id="P006",
        prompt_text="Industrial furnace charging fork cantilever arm operating inside a ceramic kiln at 950 C carrying heavy molten crucibles.",
        cluster="Bending Beams",
        loading_mode="bending_beam",
        operating_environment="extreme_furnace_heat",
        regulatory_domain="high_temp_creep",
        expected_indices=["beam_strength"],
        expected_top_materials=["Alumina_Ceramic", "Inconel_718"],
        mandatory_disqualified=["Aluminium_6061_T6", "PLA", "PETG", "PEEK", "ABS", "Alloy_Steel_4140"],
        service_temperature_c=950.0,
    ),
    "P007": EngineeringAuditTestCase(
        test_id="P007",
        prompt_text="Submersible robotic manipulator arm articulating in deep ocean marine trenches under 500 bar hydrostatic pressure.",
        cluster="Bending Beams",
        loading_mode="bending_beam",
        operating_environment="deep_marine_saline",
        regulatory_domain="marine_corrosion_proof",
        expected_indices=["beam_strength"],
        expected_top_materials=["Titanium_Ti6Al4V"],
        mandatory_disqualified=["Alloy_Steel_4140", "PLA"],
    ),
    "P008": EngineeringAuditTestCase(
        test_id="P008",
        prompt_text="Lightweight satellite deployable solar array boom operating in hard vacuum under solar radiation thermal cycling.",
        cluster="Bending Beams",
        loading_mode="bending_beam",
        operating_environment="high_vacuum",
        regulatory_domain="space_low_outgassing",
        expected_indices=["beam_stiffness"],
        expected_top_materials=["CFRP_Prepreg", "Titanium_Ti6Al4V", "Aluminium_6061_T6"],
        mandatory_disqualified=["PLA", "TPU_95A"],
    ),
    "P009": EngineeringAuditTestCase(
        test_id="P009",
        prompt_text="Heavy duty crane gantry boom arm lifting 20 ton shipping containers in a marine port.",
        cluster="Bending Beams",
        loading_mode="bending_beam",
        operating_environment="coastal_marine",
        regulatory_domain="heavy_crane_hoisting",
        expected_indices=["beam_strength"],
        expected_top_materials=["Alloy_Steel_4140", "Stainless_Steel_316L"],
        mandatory_disqualified=["Alumina_Ceramic", "PLA", "TPU_95A"],
    ),
    "P010": EngineeringAuditTestCase(
        test_id="P010",
        prompt_text="Orthopedic internal spinal fixation rod bridging two lumbar vertebrae to resist flexural spine bending.",
        cluster="Bending Beams",
        loading_mode="bending_beam",
        operating_environment="in_vivo_biomedical",
        regulatory_domain="iso_10993_biomedical",
        expected_indices=["beam_strength", "beam_stiffness"],
        expected_top_materials=["Titanium_Ti6Al4V", "PEEK"],
        mandatory_disqualified=["Aluminium_6061_T6", "Copper_C11000", "Alloy_Steel_4140"],
    ),
    "P011": EngineeringAuditTestCase(
        test_id="P011",
        prompt_text="Chemical scrubber spray nozzle support beam exposed to continuous 20% sulfuric acid vapor.",
        cluster="Bending Beams",
        loading_mode="bending_beam",
        operating_environment="corrosive_acid",
        regulatory_domain="chemical_inertness",
        expected_indices=["beam_strength"],
        expected_top_materials=["PEEK", "Alumina_Ceramic", "Stainless_Steel_316L"],
        mandatory_disqualified=["Aluminium_6061_T6", "Alloy_Steel_4140"],
    ),
    "P012": EngineeringAuditTestCase(
        test_id="P012",
        prompt_text="Rural pedestrian footbridge cantilever deck joist for a remote village river crossing in Kenya.",
        cluster="Bending Beams",
        loading_mode="bending_beam",
        operating_environment="outdoor_river_humid",
        regulatory_domain="rural_field_kenya",
        expected_indices=["beam_strength"],
        expected_top_materials=["Alloy_Steel_4140", "Aluminium_6061_T6", "PETG-CF"],
        mandatory_disqualified=["PEEK", "CFRP_Prepreg"],
    ),
    "P013": EngineeringAuditTestCase(
        test_id="P013",
        prompt_text="High-speed Formula 1 suspension double wishbone arm resisting extreme aerodynamic downforce and cornering bending loads.",
        cluster="Bending Beams",
        loading_mode="bending_beam",
        operating_environment="racing_track",
        regulatory_domain="ultra_lightweight_racing",
        expected_indices=["beam_stiffness"],
        expected_top_materials=["CFRP_Prepreg", "Titanium_Ti6Al4V"],
        mandatory_disqualified=["PLA", "TPU_95A", "Alloy_Steel_4140"],
    ),

    # -------------------------------------------------------------------------
    # Cluster 2: Tensile Ties, Guy Wires & Suspension Chords (P014 - P026)
    # -------------------------------------------------------------------------
    "P014": EngineeringAuditTestCase(
        test_id="P014",
        prompt_text="Guy wire cable in pure tension stabilizing a 50-meter rural wind turbine tower against storm gale winds.",
        cluster="Tensile Ties",
        loading_mode="tensile_tie",
        operating_environment="outdoor_all_weather",
        regulatory_domain="rural_field_kenya",
        expected_indices=["tie_strength"],
        expected_top_materials=["Alloy_Steel_4140", "Stainless_Steel_316L"],
        mandatory_disqualified=["PLA", "TPU_95A"],
    ),
    "P015": EngineeringAuditTestCase(
        test_id="P015",
        prompt_text="Ultra-lightweight tension spoke wire for competition racing bicycle wheels requiring minimal elastic stretch.",
        cluster="Tensile Ties",
        loading_mode="tensile_tie",
        operating_environment="ambient",
        regulatory_domain="ultra_lightweight_racing",
        expected_indices=["tie_stiffness"],
        expected_top_materials=["CFRP_Prepreg", "Titanium_Ti6Al4V"],
        mandatory_disqualified=["TPU_95A", "PLA"],
    ),
    "P016": EngineeringAuditTestCase(
        test_id="P016",
        prompt_text="Mooring hawser tension tie securing an offshore floating oil platform in stormy marine saltwater.",
        cluster="Tensile Ties",
        loading_mode="tensile_tie",
        operating_environment="marine_saltwater",
        regulatory_domain="marine_corrosion_resistance",
        expected_indices=["tie_strength"],
        expected_top_materials=["Stainless_Steel_316L", "Titanium_Ti6Al4V"],
        mandatory_disqualified=["Alloy_Steel_4140", "PLA"],
    ),
    "P017": EngineeringAuditTestCase(
        test_id="P017",
        prompt_text="High-vacuum ion propulsion tether wire in low Earth orbit subjected to continuous axial tension.",
        cluster="Tensile Ties",
        loading_mode="tensile_tie",
        operating_environment="high_vacuum",
        regulatory_domain="space_low_outgassing",
        expected_indices=["tie_strength"],
        expected_top_materials=["Titanium_Ti6Al4V", "CFRP_Prepreg"],
        mandatory_disqualified=["PLA", "TPU_95A"],
    ),
    "P018": EngineeringAuditTestCase(
        test_id="P018",
        prompt_text="Chemical reactor agitator suspension tie rod immersed in hot concentrated hydrochloric acid at 80 C.",
        cluster="Tensile Ties",
        loading_mode="tensile_tie",
        operating_environment="corrosive_acid",
        regulatory_domain="acid_resistance",
        expected_indices=["tie_strength"],
        expected_top_materials=["PEEK", "Titanium_Ti6Al4V"],
        mandatory_disqualified=["Aluminium_6061_T6", "Alloy_Steel_4140"],
        service_temperature_c=80.0,
    ),
    "P019": EngineeringAuditTestCase(
        test_id="P019",
        prompt_text="Heavy mining hoist elevator cable lifting 15 ton ore cars from a deep vertical shaft.",
        cluster="Tensile Ties",
        loading_mode="tensile_tie",
        operating_environment="mine_humid",
        regulatory_domain="heavy_crane_hoisting",
        expected_indices=["tie_strength"],
        expected_top_materials=["Alloy_Steel_4140"],
        mandatory_disqualified=["Alumina_Ceramic", "PLA", "TPU_95A"],
    ),
    "P020": EngineeringAuditTestCase(
        test_id="P020",
        prompt_text="Biocompatible artificial tendon tensile chord replacing a ruptured human Achilles tendon.",
        cluster="Tensile Ties",
        loading_mode="tensile_tie",
        operating_environment="in_vivo_biomedical",
        regulatory_domain="iso_10993_biomedical",
        expected_indices=["tie_strength"],
        expected_top_materials=["PEEK", "Titanium_Ti6Al4V"],
        mandatory_disqualified=["Aluminium_6061_T6", "Copper_C11000", "Alloy_Steel_4140"],
    ),
    "P021": EngineeringAuditTestCase(
        test_id="P021",
        prompt_text="Furnace door counterweight tension suspension cable operating directly above a 600 C smelting retort.",
        cluster="Tensile Ties",
        loading_mode="tensile_tie",
        operating_environment="extreme_furnace_heat",
        regulatory_domain="high_temp_creep",
        expected_indices=["tie_strength"],
        expected_top_materials=["Inconel_718", "Stainless_Steel_316L"],
        mandatory_disqualified=["Aluminium_6061_T6", "PLA", "PETG", "ABS", "PC"],
        service_temperature_c=600.0,
    ),
    "P022": EngineeringAuditTestCase(
        test_id="P022",
        prompt_text="Cryogenic liquid hydrogen propellant tank tension support strut operating at -253 C.",
        cluster="Tensile Ties",
        loading_mode="tensile_tie",
        operating_environment="cryogenic",
        regulatory_domain="cryogenic_toughness",
        expected_indices=["tie_stiffness", "tie_strength"],
        expected_top_materials=["Inconel_718", "Titanium_Ti6Al4V", "Stainless_Steel_316L"],
        mandatory_disqualified=["Alloy_Steel_4140", "PLA", "ABS"],
        service_temperature_c=-253.0,
    ),
    "P023": EngineeringAuditTestCase(
        test_id="P023",
        prompt_text="Solar sail tensioning stay rigging deployed under intense direct unattenuated space UV radiation.",
        cluster="Tensile Ties",
        loading_mode="tensile_tie",
        operating_environment="solar_uv_space",
        regulatory_domain="space_low_outgassing",
        expected_indices=["tie_stiffness"],
        expected_top_materials=["CFRP_Prepreg", "Titanium_Ti6Al4V"],
        mandatory_disqualified=["ABS", "PLA"],
    ),
    "P024": EngineeringAuditTestCase(
        test_id="P024",
        prompt_text="Food processing plant poultry suspension shackle tie in constant contact with meat and steam washdown.",
        cluster="Tensile Ties",
        loading_mode="tensile_tie",
        operating_environment="washdown_moisture",
        regulatory_domain="fda_food_contact",
        expected_indices=["tie_strength"],
        expected_top_materials=["Stainless_Steel_316L", "POM_Delrin", "PETG"],
        mandatory_disqualified=["PETG-CF", "PA12-CF", "Alloy_Steel_4140"],
    ),
    "P025": EngineeringAuditTestCase(
        test_id="P025",
        prompt_text="Emergency rapid-replacement guy wire for a damaged telecommunication antenna mast in rural Kenya.",
        cluster="Tensile Ties",
        loading_mode="tensile_tie",
        operating_environment="outdoor_tropical",
        regulatory_domain="rural_field_kenya",
        expected_indices=["tie_strength"],
        expected_top_materials=["Alloy_Steel_4140", "Aluminium_6061_T6"],
        mandatory_disqualified=["CFRP_Prepreg", "PEEK"],
    ),
    "P026": EngineeringAuditTestCase(
        test_id="P026",
        prompt_text="Acoustic musical instrument tension string requiring maximum specific tensile modulus for crisp tonal pitch.",
        cluster="Tensile Ties",
        loading_mode="tensile_tie",
        operating_environment="ambient",
        regulatory_domain="precision_elasticity",
        expected_indices=["tie_stiffness"],
        expected_top_materials=["PA12", "Titanium_Ti6Al4V", "CFRP_Prepreg"],
        mandatory_disqualified=["Alumina_Ceramic"],
    ),

    # -------------------------------------------------------------------------
    # Cluster 3: Thin Shell Plates, Enclosures & Faceplates (P027 - P039)
    # -------------------------------------------------------------------------
    "P027": EngineeringAuditTestCase(
        test_id="P027",
        prompt_text="High-performance laptop chassis outer display lid requiring minimum flexural deflection under thumb pressure.",
        cluster="Shell Plates",
        loading_mode="shell_plate",
        operating_environment="ambient_consumer",
        regulatory_domain="ultra_lightweight_consumer",
        expected_indices=["plate_stiffness"],
        expected_top_materials=["CFRP_Prepreg", "Aluminium_6061_T6", "Magnesium_AZ91D", "Polycarbonate"],
        mandatory_disqualified=["TPU_95A"],
    ),
    "P028": EngineeringAuditTestCase(
        test_id="P028",
        prompt_text="Hydro-turbine exterior blade skin faceplate resisting water pressure deflection and boundary layer drag.",
        cluster="Shell Plates",
        loading_mode="shell_plate",
        operating_environment="submerged_freshwater",
        regulatory_domain="rural_field_kenya",
        expected_indices=["plate_stiffness"],
        expected_top_materials=["PETG-CF", "PETG_CF_Reinforced", "Stainless_Steel_316L"],
        mandatory_disqualified=["PLA"],
    ),
    "P029": EngineeringAuditTestCase(
        test_id="P029",
        prompt_text="Submersible camera housing window cover plate resisting hydrostatic bursting rupture at 100 meters depth.",
        cluster="Shell Plates",
        loading_mode="shell_plate",
        operating_environment="marine_saltwater",
        regulatory_domain="high_strength_watertight",
        expected_indices=["plate_strength"],
        expected_top_materials=["Polycarbonate", "Polycarbonate_Optical", "Titanium_Ti6Al4V"],
        mandatory_disqualified=["PLA", "Alloy_Steel_4140"],
    ),
    "P030": EngineeringAuditTestCase(
        test_id="P030",
        prompt_text="Optical safety face shield visor requiring crystal-clear see-through transparency and ballistic projectile shatter resistance.",
        cluster="Shell Plates",
        loading_mode="shell_plate",
        operating_environment="workshop_indoor",
        regulatory_domain="optical_transparency",
        expected_indices=["plate_strength"],
        expected_top_materials=["Polycarbonate", "PC", "Polycarbonate_Optical"],
        mandatory_disqualified=["Aluminium_6061_T6", "PETG-CF", "PEEK", "Alumina_Ceramic", "Alloy_Steel_4140"],
    ),
    "P031": EngineeringAuditTestCase(
        test_id="P031",
        prompt_text="Chemical fume hood side baffle panel exposed to boiling nitric acid vapors.",
        cluster="Shell Plates",
        loading_mode="shell_plate",
        operating_environment="corrosive_acid",
        regulatory_domain="chemical_inertness",
        expected_indices=["plate_stiffness"],
        expected_top_materials=["PEEK", "Alumina_Ceramic", "PTFE"],
        mandatory_disqualified=["Aluminium_6061_T6", "Alloy_Steel_4140"],
    ),
    "P032": EngineeringAuditTestCase(
        test_id="P032",
        prompt_text="Outdoor automotive exterior body fender panel exposed to blazing sun and gravel impact.",
        cluster="Shell Plates",
        loading_mode="shell_plate",
        operating_environment="solar_uv_outdoor",
        regulatory_domain="automotive_exterior",
        expected_indices=["plate_stiffness"],
        expected_top_materials=["ASA", "Aluminium_6061_T6"],
        mandatory_disqualified=["ABS", "PLA"],
    ),
    "P033": EngineeringAuditTestCase(
        test_id="P033",
        prompt_text="Cryogenic cold-box insulation outer vacuum barrier plate operating at -80 C.",
        cluster="Shell Plates",
        loading_mode="shell_plate",
        operating_environment="cryogenic",
        regulatory_domain="cryogenic_ductility",
        expected_indices=["plate_strength"],
        expected_top_materials=["Stainless_Steel_316L", "Aluminium_6061_T6"],
        mandatory_disqualified=["Alloy_Steel_4140"],
        service_temperature_c=-80.0,
    ),
    "P034": EngineeringAuditTestCase(
        test_id="P034",
        prompt_text="Industrial blast furnace thermal radiation heat shield plate facing 1050 C glowing embers.",
        cluster="Shell Plates",
        loading_mode="shell_plate",
        operating_environment="extreme_furnace_heat",
        regulatory_domain="refractory_safety",
        expected_indices=["thermal_insulation", "plate_strength"],
        expected_top_materials=["Alumina_Ceramic", "Inconel_718"],
        mandatory_disqualified=["Aluminium_6061_T6", "PLA", "PETG", "PEEK", "ABS"],
        service_temperature_c=1050.0,
    ),
    "P035": EngineeringAuditTestCase(
        test_id="P035",
        prompt_text="Food contact conveyor sliding drop plate for raw dairy and cheese production.",
        cluster="Shell Plates",
        loading_mode="shell_plate",
        operating_environment="sanitary_wet",
        regulatory_domain="fda_food_contact",
        expected_indices=["plate_stiffness"],
        expected_top_materials=["Stainless_Steel_316L", "POM_Delrin", "PETG"],
        mandatory_disqualified=["PETG-CF", "PA12-CF"],
    ),
    "P036": EngineeringAuditTestCase(
        test_id="P036",
        prompt_text="Biocompatible cranial defect protection plate (cranioplasty implant) shielding brain tissue under the scalp.",
        cluster="Shell Plates",
        loading_mode="shell_plate",
        operating_environment="in_vivo_biomedical",
        regulatory_domain="iso_10993_biomedical",
        expected_indices=["plate_strength"],
        expected_top_materials=["Titanium_Ti6Al4V", "PEEK"],
        mandatory_disqualified=["Aluminium_6061_T6", "Copper_C11000", "Alloy_Steel_4140"],
    ),
    "P037": EngineeringAuditTestCase(
        test_id="P037",
        prompt_text="Decentralized solar cooker parabolic reflector backing plate built locally in rural Kenya.",
        cluster="Shell Plates",
        loading_mode="shell_plate",
        operating_environment="solar_uv_equatorial",
        regulatory_domain="rural_field_kenya",
        expected_indices=["plate_stiffness"],
        expected_top_materials=["ASA", "Aluminium_6061_T6"],
        mandatory_disqualified=["CFRP_Prepreg", "PEEK"],
    ),
    "P038": EngineeringAuditTestCase(
        test_id="P038",
        prompt_text="Spacecraft satellite micrometeoroid impact protection plate shielding internal avionics.",
        cluster="Shell Plates",
        loading_mode="shell_plate",
        operating_environment="high_vacuum",
        regulatory_domain="space_low_outgassing",
        expected_indices=["plate_strength"],
        expected_top_materials=["Titanium_Ti6Al4V", "CFRP_Prepreg", "Aluminium_6061_T6"],
        mandatory_disqualified=["PLA", "TPU_95A"],
    ),
    "P039": EngineeringAuditTestCase(
        test_id="P039",
        prompt_text="High-speed train aerodynamic nose cone fairing plate resisting turbulent air pressure buffeting.",
        cluster="Shell Plates",
        loading_mode="shell_plate",
        operating_environment="outdoor_transport",
        regulatory_domain="ultra_lightweight_transport",
        expected_indices=["plate_stiffness"],
        expected_top_materials=["CFRP_Prepreg", "Aluminium_6061_T6"],
        mandatory_disqualified=["Alloy_Steel_4140", "TPU_95A"],
    ),

    # -------------------------------------------------------------------------
    # Cluster 4: Rotational Rotors, Flywheels & Centrifuges (P040 - P051)
    # -------------------------------------------------------------------------
    "P040": EngineeringAuditTestCase(
        test_id="P040",
        prompt_text="Kinetic energy storage flywheel rotor spinning at 60,000 RPM to store maximum rotational energy without centrifugal bursting.",
        cluster="Rotational Rotors",
        loading_mode="rotational_rotor",
        operating_environment="high_vacuum",
        regulatory_domain="kinetic_storage_burst",
        expected_indices=["flywheel_inertia", "tie_strength"],
        expected_top_materials=["CFRP_Prepreg", "Titanium_Ti6Al4V"],
        mandatory_disqualified=["TPU_95A", "Copper_C11000"],
    ),
    "P041": EngineeringAuditTestCase(
        test_id="P041",
        prompt_text="Micro-hydro Pelton runner wheel spinning in a sediment-laden river in Kenya driving an off-grid alternator.",
        cluster="Rotational Rotors",
        loading_mode="rotational_rotor",
        operating_environment="submerged_freshwater",
        regulatory_domain="rural_field_kenya",
        expected_indices=["flywheel_inertia", "beam_strength"],
        expected_top_materials=["PETG-CF", "Stainless_Steel_316L"],
        mandatory_disqualified=["PLA", "PEEK"],
    ),
    "P042": EngineeringAuditTestCase(
        test_id="P042",
        prompt_text="Blood fractionation medical centrifuge rotor head spinning at 15,000 RPM in a clinical laboratory.",
        cluster="Rotational Rotors",
        loading_mode="rotational_rotor",
        operating_environment="clinical_clean",
        regulatory_domain="clinical_centrifuge_safety",
        expected_indices=["flywheel_inertia"],
        expected_top_materials=["Titanium_Ti6Al4V", "Aluminium_6061_T6"],
        mandatory_disqualified=["Alumina_Ceramic"],
    ),
    "P043": EngineeringAuditTestCase(
        test_id="P043",
        prompt_text="Jet engine turbocharger compressor impeller wheel sucking air at 120,000 RPM under 180 C induction heat.",
        cluster="Rotational Rotors",
        loading_mode="rotational_rotor",
        operating_environment="thermal_180c",
        regulatory_domain="high_temp_burst",
        expected_indices=["flywheel_inertia"],
        expected_top_materials=["Titanium_Ti6Al4V"],
        mandatory_disqualified=["PLA", "PETG", "ABS", "PC"],
        service_temperature_c=180.0,
    ),
    "P044": EngineeringAuditTestCase(
        test_id="P044",
        prompt_text="Gas turbine hot-stage exhaust turbine wheel spinning in combustion gases at 700 C.",
        cluster="Rotational Rotors",
        loading_mode="rotational_rotor",
        operating_environment="extreme_furnace_heat",
        regulatory_domain="high_temp_creep",
        expected_indices=["flywheel_inertia"],
        expected_top_materials=["Inconel_718"],
        mandatory_disqualified=["Aluminium_6061_T6", "Alloy_Steel_4140", "PLA", "PETG", "PEEK"],
        service_temperature_c=700.0,
    ),
    "P045": EngineeringAuditTestCase(
        test_id="P045",
        prompt_text="Submersible bilge pump open impeller pumping saltwater and sand slurry on a marine fishing trawler.",
        cluster="Rotational Rotors",
        loading_mode="rotational_rotor",
        operating_environment="marine_saltwater",
        regulatory_domain="marine_corrosion_resistance",
        expected_indices=["flywheel_inertia"],
        expected_top_materials=["Stainless_Steel_316L", "Titanium_Ti6Al4V"],
        mandatory_disqualified=["Alloy_Steel_4140", "PLA"],
    ),
    "P046": EngineeringAuditTestCase(
        test_id="P046",
        prompt_text="High-speed dental drill turbine rotor spinning at 400,000 RPM requiring steam autoclave sterilization.",
        cluster="Rotational Rotors",
        loading_mode="rotational_rotor",
        operating_environment="steam_autoclave_134c",
        regulatory_domain="iso_10993_biomedical",
        expected_indices=["flywheel_inertia"],
        expected_top_materials=["Titanium_Ti6Al4V", "PEEK", "Stainless_Steel_316L"],
        mandatory_disqualified=["PLA", "ABS", "PETG"],
        service_temperature_c=134.0,
    ),
    "P047": EngineeringAuditTestCase(
        test_id="P047",
        prompt_text="Uranium enrichment ultracentrifuge rotor tube operating in ultra-high vacuum under extreme peripheral velocity.",
        cluster="Rotational Rotors",
        loading_mode="rotational_rotor",
        operating_environment="high_vacuum",
        regulatory_domain="extreme_specific_strength",
        expected_indices=["flywheel_inertia"],
        expected_top_materials=["CFRP_Prepreg", "Titanium_Ti6Al4V", "Alloy_Steel_4140"],
        mandatory_disqualified=["PLA", "TPU_95A"],
    ),
    "P048": EngineeringAuditTestCase(
        test_id="P048",
        prompt_text="Cryogenic liquid methane turbopump inducer impeller spinning at -160 C in a rocket propulsion system.",
        cluster="Rotational Rotors",
        loading_mode="rotational_rotor",
        operating_environment="cryogenic",
        regulatory_domain="cryogenic_burst",
        expected_indices=["flywheel_inertia"],
        expected_top_materials=["Titanium_Ti6Al4V", "Inconel_718", "Stainless_Steel_316L"],
        mandatory_disqualified=["Alloy_Steel_4140", "PLA"],
        service_temperature_c=-160.0,
    ),
    "P049": EngineeringAuditTestCase(
        test_id="P049",
        prompt_text="Industrial food mixer high-shear dispersion rotor homogenizing baby food puree.",
        cluster="Rotational Rotors",
        loading_mode="rotational_rotor",
        operating_environment="food_slurry",
        regulatory_domain="fda_food_contact",
        expected_indices=["flywheel_inertia"],
        expected_top_materials=["Stainless_Steel_316L", "POM_Delrin"],
        mandatory_disqualified=["PETG-CF", "PA12-CF", "Copper_C11000"],
    ),
    "P050": EngineeringAuditTestCase(
        test_id="P050",
        prompt_text="Automotive high-speed engine starter ring gear flywheel subjected to rapid start-stop torque shocks.",
        cluster="Rotational Rotors",
        loading_mode="rotational_rotor",
        operating_environment="automotive_engine",
        regulatory_domain="automotive_endurance",
        expected_indices=["flywheel_inertia"],
        expected_top_materials=["Alloy_Steel_4140"],
        mandatory_disqualified=["PLA", "TPU_95A"],
    ),
    "P051": EngineeringAuditTestCase(
        test_id="P051",
        prompt_text="High-altitude weather drone propulsion propeller spinning in freezing sub-zero UV-rich stratosphere.",
        cluster="Rotational Rotors",
        loading_mode="rotational_rotor",
        operating_environment="freezing_uv_stratosphere",
        regulatory_domain="ultra_lightweight_aerospace",
        expected_indices=["flywheel_inertia", "beam_stiffness"],
        expected_top_materials=["CFRP_Prepreg", "PETG-CF"],
        mandatory_disqualified=["Alloy_Steel_4140", "PLA"],
    ),

    # -------------------------------------------------------------------------
    # Cluster 5: Elastic Springs, Bumpers & Compliant Dampers (P052 - P063)
    # -------------------------------------------------------------------------
    "P052": EngineeringAuditTestCase(
        test_id="P052",
        prompt_text="Protective smartphone bumper case that can survive repeated 2-meter drop impacts onto concrete without cracking.",
        cluster="Elastic Dampers",
        loading_mode="elastic_damper",
        operating_environment="ambient_consumer",
        regulatory_domain="impact_cushion",
        expected_indices=["elastic_energy"],
        expected_top_materials=["TPU_95A"],
        mandatory_disqualified=["Alumina_Ceramic", "Alloy_Steel_4140", "PEEK"],
    ),
    "P053": EngineeringAuditTestCase(
        test_id="P053",
        prompt_text="Automotive off-road suspension coil spring absorbing severe trail terrain shock loads without settling.",
        cluster="Elastic Dampers",
        loading_mode="elastic_damper",
        operating_environment="outdoor_muddy",
        regulatory_domain="automotive_suspension",
        expected_indices=["elastic_energy"],
        expected_top_materials=["Alloy_Steel_4140", "Titanium_Ti6Al4V"],
        mandatory_disqualified=["Alumina_Ceramic", "PLA"],
    ),
    "P054": EngineeringAuditTestCase(
        test_id="P054",
        prompt_text="Marine dock piling fender bumper absorbing the berthing impact kinetic energy of arriving ferry boats.",
        cluster="Elastic Dampers",
        loading_mode="elastic_damper",
        operating_environment="marine_saltwater",
        regulatory_domain="marine_fender_cushion",
        expected_indices=["elastic_energy"],
        expected_top_materials=["TPU_95A"],
        mandatory_disqualified=["Alloy_Steel_4140", "PLA"],
    ),
    "P055": EngineeringAuditTestCase(
        test_id="P055",
        prompt_text="Cryogenic valve seal spring energizer maintaining elastic sealing pressure in liquid nitrogen at -196 C.",
        cluster="Elastic Dampers",
        loading_mode="elastic_damper",
        operating_environment="cryogenic",
        regulatory_domain="cryogenic_spring",
        expected_indices=["elastic_energy"],
        expected_top_materials=["Stainless_Steel_316L", "Inconel_718"],
        mandatory_disqualified=["TPU_95A", "Alloy_Steel_4140"],
        service_temperature_c=-196.0,
    ),
    "P056": EngineeringAuditTestCase(
        test_id="P056",
        prompt_text="High-temperature furnace exhaust damper flap seal spring operating continuously at 550 C.",
        cluster="Elastic Dampers",
        loading_mode="elastic_damper",
        operating_environment="extreme_furnace_heat",
        regulatory_domain="high_temp_spring",
        expected_indices=["elastic_energy"],
        expected_top_materials=["Inconel_718"],
        mandatory_disqualified=["Aluminium_6061_T6", "PLA", "PETG", "ABS", "PC"],
        service_temperature_c=550.0,
    ),
    "P057": EngineeringAuditTestCase(
        test_id="P057",
        prompt_text="Biocompatible compliant flexural micro-hinge for a minimally invasive surgical laparoscopic grasper.",
        cluster="Elastic Dampers",
        loading_mode="elastic_damper",
        operating_environment="in_vivo_biomedical",
        regulatory_domain="iso_10993_biomedical",
        expected_indices=["elastic_energy"],
        expected_top_materials=["Titanium_Ti6Al4V", "PEEK"],
        mandatory_disqualified=["Aluminium_6061_T6", "Copper_C11000", "Alloy_Steel_4140"],
    ),
    "P058": EngineeringAuditTestCase(
        test_id="P058",
        prompt_text="Athletic running shoe midsole cushion providing maximum energy return and shock attenuation under foot strike.",
        cluster="Elastic Dampers",
        loading_mode="elastic_damper",
        operating_environment="outdoor_wet",
        regulatory_domain="footwear_cushion",
        expected_indices=["elastic_energy"],
        expected_top_materials=["TPU_95A"],
        mandatory_disqualified=["Alumina_Ceramic", "Alloy_Steel_4140"],
    ),
    "P059": EngineeringAuditTestCase(
        test_id="P059",
        prompt_text="Vibration isolation damping mount for an off-grid diesel generator installed on a concrete slab in Kenya.",
        cluster="Elastic Dampers",
        loading_mode="elastic_damper",
        operating_environment="diesel_oil_tropical",
        regulatory_domain="rural_field_kenya",
        expected_indices=["elastic_energy"],
        expected_top_materials=["TPU_95A"],
        mandatory_disqualified=["PLA"],
    ),
    "P060": EngineeringAuditTestCase(
        test_id="P060",
        prompt_text="Spacecraft payload satellite separation snap-latch compliant spring deployed in high vacuum.",
        cluster="Elastic Dampers",
        loading_mode="elastic_damper",
        operating_environment="high_vacuum",
        regulatory_domain="space_low_outgassing",
        expected_indices=["elastic_energy"],
        expected_top_materials=["Titanium_Ti6Al4V", "Stainless_Steel_316L"],
        mandatory_disqualified=["TPU_95A", "PLA"],
    ),
    "P061": EngineeringAuditTestCase(
        test_id="P061",
        prompt_text="Food-safe compliant snap-fit lid hinge for a reusable baby food container.",
        cluster="Elastic Dampers",
        loading_mode="elastic_damper",
        operating_environment="dishwasher_80c",
        regulatory_domain="fda_food_contact",
        expected_indices=["elastic_energy"],
        expected_top_materials=["Polycarbonate", "PETG", "POM_Delrin"],
        mandatory_disqualified=["PETG-CF", "PA12-CF"],
    ),
    "P062": EngineeringAuditTestCase(
        test_id="P062",
        prompt_text="Precision optical mirror kinematic mount compliant flexure requiring zero hysteresis and micro-radian deflection.",
        cluster="Elastic Dampers",
        loading_mode="elastic_damper",
        operating_environment="laboratory_clean",
        regulatory_domain="precision_instrument",
        expected_indices=["elastic_energy"],
        expected_top_materials=["Titanium_Ti6Al4V", "Aluminium_6061_T6"],
        mandatory_disqualified=["PLA", "TPU_95A"],
    ),
    "P063": EngineeringAuditTestCase(
        test_id="P063",
        prompt_text="Acid pump check-valve return spring immersed in concentrated hydrochloric acid.",
        cluster="Elastic Dampers",
        loading_mode="elastic_damper",
        operating_environment="corrosive_acid",
        regulatory_domain="acid_resistance",
        expected_indices=["elastic_energy"],
        expected_top_materials=["PEEK", "Titanium_Ti6Al4V"],
        mandatory_disqualified=["Aluminium_6061_T6", "Alloy_Steel_4140"],
    ),

    # -------------------------------------------------------------------------
    # Cluster 6: Industrial Cutting Tools & Wear Machinery (P064 - P075)
    # -------------------------------------------------------------------------
    "P064": EngineeringAuditTestCase(
        test_id="P064",
        prompt_text="Heavy-duty agricultural sugarcane harvesting machete blade chopping tough fibrous stalks in humid Kenyan soil.",
        cluster="Cutting Tools",
        loading_mode="cutting_tool",
        operating_environment="tropical_soil",
        regulatory_domain="rural_field_kenya",
        expected_indices=["tie_strength", "beam_strength"],
        expected_top_materials=["Alloy_Steel_4140"],
        mandatory_disqualified=["PLA", "TPU_95A", "Alumina_Ceramic"],
    ),
    "P065": EngineeringAuditTestCase(
        test_id="P065",
        prompt_text="High-speed CNC milling cutter endmill machining titanium aerospace forgings generating 800 C chip friction.",
        cluster="Cutting Tools",
        loading_mode="cutting_tool",
        operating_environment="hot_machining_800c",
        regulatory_domain="extreme_hot_hardness",
        expected_indices=["beam_strength", "tie_strength"],
        expected_top_materials=["Alumina_Ceramic", "Inconel_718"],
        mandatory_disqualified=["Aluminium_6061_T6", "Copper_C11000", "PLA", "PETG"],
        service_temperature_c=800.0,
    ),
    "P066": EngineeringAuditTestCase(
        test_id="P066",
        prompt_text="Food processing plant rotary butcher slicing knife dicing frozen beef sides.",
        cluster="Cutting Tools",
        loading_mode="cutting_tool",
        operating_environment="sanitary_cold_washdown",
        regulatory_domain="fda_food_contact",
        expected_indices=["beam_strength", "tie_strength"],
        expected_top_materials=["Stainless_Steel_316L", "Alloy_Steel_4140"],
        mandatory_disqualified=["PETG-CF", "PA12-CF"],
    ),
    "P067": EngineeringAuditTestCase(
        test_id="P067",
        prompt_text="Subsea pipeline trenching rock saw blade cutter segment cutting granite under marine seawater.",
        cluster="Cutting Tools",
        loading_mode="cutting_tool",
        operating_environment="marine_saltwater_abrasive",
        regulatory_domain="rock_cutting_wear",
        expected_indices=["beam_strength", "tie_strength"],
        expected_top_materials=["Alloy_Steel_4140", "Alumina_Ceramic"],
        mandatory_disqualified=["PLA", "Aluminium_6061_T6"],
    ),
    "P068": EngineeringAuditTestCase(
        test_id="P068",
        prompt_text="Surgical scalpel blade for microsurgery requiring ultra-sharp edge retention without tissue toxicity.",
        cluster="Cutting Tools",
        loading_mode="cutting_tool",
        operating_environment="in_vivo_biomedical",
        regulatory_domain="iso_10993_biomedical",
        expected_indices=["beam_strength", "tie_strength"],
        expected_top_materials=["Stainless_Steel_316L", "Titanium_Ti6Al4V"],
        mandatory_disqualified=["Aluminium_6061_T6", "Copper_C11000"],
    ),
    "P069": EngineeringAuditTestCase(
        test_id="P069",
        prompt_text="Woodworking high-speed planer blade smoothing kiln-dried tropical hardwood.",
        cluster="Cutting Tools",
        loading_mode="cutting_tool",
        operating_environment="dry_abrasive_dust",
        regulatory_domain="keen_edge_retention",
        expected_indices=["beam_strength", "tie_strength"],
        expected_top_materials=["Alloy_Steel_4140"],
        mandatory_disqualified=["PLA", "TPU_95A"],
    ),
    "P070": EngineeringAuditTestCase(
        test_id="P070",
        prompt_text="Plastic recycling shredder granulator blade chopping post-consumer PET bottles containing dirt and grit.",
        cluster="Cutting Tools",
        loading_mode="cutting_tool",
        operating_environment="dry_abrasive_recycling",
        regulatory_domain="impact_shear_toughness",
        expected_indices=["beam_strength", "tie_strength"],
        expected_top_materials=["Alloy_Steel_4140"],
        mandatory_disqualified=["Alumina_Ceramic", "PLA"],
    ),
    "P071": EngineeringAuditTestCase(
        test_id="P071",
        prompt_text="Chemical slurry pump shearing impeller chopping fibrous cellulose pulp in hot bleach liquor.",
        cluster="Cutting Tools",
        loading_mode="cutting_tool",
        operating_environment="hot_bleach_liquor",
        regulatory_domain="corrosion_and_wear",
        expected_indices=["beam_strength", "tie_strength"],
        expected_top_materials=["Stainless_Steel_316L", "PEEK"],
        mandatory_disqualified=["Alloy_Steel_4140", "Aluminium_6061_T6"],
    ),
    "P072": EngineeringAuditTestCase(
        test_id="P072",
        prompt_text="Cryogenic scrap metal shredder shear tooth operating at -50 C in an Arctic recycling facility.",
        cluster="Cutting Tools",
        loading_mode="cutting_tool",
        operating_environment="cryogenic",
        regulatory_domain="cryogenic_impact_toughness",
        expected_indices=["beam_strength", "tie_strength"],
        expected_top_materials=["Stainless_Steel_316L", "Inconel_718"],
        mandatory_disqualified=["Alloy_Steel_4140"],
        service_temperature_c=-50.0,
    ),
    "P073": EngineeringAuditTestCase(
        test_id="P073",
        prompt_text="Glass cutting scoring wheel scribe requiring extreme micro-indentation hardness to scratch soda-lime glass.",
        cluster="Cutting Tools",
        loading_mode="cutting_tool",
        operating_environment="ambient",
        regulatory_domain="mohs_scratch_hardness",
        expected_indices=["beam_strength", "tie_strength"],
        expected_top_materials=["Alumina_Ceramic"],
        mandatory_disqualified=["Copper_C11000", "Aluminium_6061_T6", "PLA"],
    ),
    "P074": EngineeringAuditTestCase(
        test_id="P074",
        prompt_text="Textile fabric laser/rotary cutter blade slitting synthetic Kevlar and carbon fiber woven fabric.",
        cluster="Cutting Tools",
        loading_mode="cutting_tool",
        operating_environment="ambient_dry",
        regulatory_domain="textile_slitting",
        expected_indices=["beam_strength", "tie_strength"],
        expected_top_materials=["Alloy_Steel_4140", "Alumina_Ceramic"],
        mandatory_disqualified=["Aluminium_6061_T6", "PLA"],
    ),
    "P075": EngineeringAuditTestCase(
        test_id="P075",
        prompt_text="Hand chisel for a rural carpenter workshop in Kenya carving local mahogany furniture.",
        cluster="Cutting Tools",
        loading_mode="cutting_tool",
        operating_environment="tropical_ambient",
        regulatory_domain="rural_field_kenya",
        expected_indices=["beam_strength", "tie_strength"],
        expected_top_materials=["Alloy_Steel_4140"],
        mandatory_disqualified=["PEEK", "PLA"],
    ),

    # -------------------------------------------------------------------------
    # Cluster 7: Thermal Management: Conductors & Insulators (P076 - P088)
    # -------------------------------------------------------------------------
    "P076": EngineeringAuditTestCase(
        test_id="P076",
        prompt_text="High-performance overclocked computer CPU cooling block heat sink requiring maximum thermal conductivity.",
        cluster="Thermal Management",
        loading_mode="thermal_management",
        operating_environment="indoor_electronics",
        regulatory_domain="max_heat_flux",
        expected_indices=["thermal_conductivity"],
        expected_top_materials=["Copper_C11000", "Aluminium_6061_T6"],
        mandatory_disqualified=["PLA", "PEEK", "Alumina_Ceramic", "Stainless_Steel_316L"],
    ),
    "P077": EngineeringAuditTestCase(
        test_id="P077",
        prompt_text="Aerospace satellite electronics thermal ground plane heat sink where mass must be strictly minimized.",
        cluster="Thermal Management",
        loading_mode="thermal_management",
        operating_environment="high_vacuum",
        regulatory_domain="ultra_lightweight_aerospace",
        expected_indices=["thermal_conductivity", "thermal_diffusivity"],
        expected_top_materials=["Aluminium_6061_T6", "Copper_C11000"],
        mandatory_disqualified=["Alloy_Steel_4140", "PLA"],
    ),
    "P078": EngineeringAuditTestCase(
        test_id="P078",
        prompt_text="Culinary gourmet frying pan cooking base providing instantaneous, hotspot-free heat spreading over gas flames.",
        cluster="Thermal Management",
        loading_mode="thermal_management",
        operating_environment="kitchen_cooking_250c",
        regulatory_domain="fda_food_contact",
        expected_indices=["thermal_conductivity"],
        expected_top_materials=["Copper_C11000", "Aluminium_6061_T6"],
        mandatory_disqualified=["PLA", "PETG", "Stainless_Steel_316L"],
        service_temperature_c=250.0,
    ),
    "P079": EngineeringAuditTestCase(
        test_id="P079",
        prompt_text="Industrial electric kiln thermal insulation refractory barrier wall containing 1100 C furnace heat.",
        cluster="Thermal Management",
        loading_mode="thermal_management",
        operating_environment="extreme_furnace_heat",
        regulatory_domain="refractory_insulation",
        expected_indices=["thermal_insulation"],
        expected_top_materials=["Alumina_Ceramic"],
        mandatory_disqualified=["Copper_C11000", "Aluminium_6061_T6", "PLA", "PETG", "PEEK"],
        service_temperature_c=1100.0,
    ),
    "P080": EngineeringAuditTestCase(
        test_id="P080",
        prompt_text="Cryogenic liquid helium dewar thermal insulating neck support barrier minimizing conductive boil-off heat leak.",
        cluster="Thermal Management",
        loading_mode="thermal_management",
        operating_environment="cryogenic_4k",
        regulatory_domain="cryogenic_insulation",
        expected_indices=["thermal_insulation"],
        expected_top_materials=["Stainless_Steel_316L", "PEEK", "Titanium_Ti6Al4V"],
        mandatory_disqualified=["Copper_C11000", "Aluminium_6061_T6"],
    ),
    "P081": EngineeringAuditTestCase(
        test_id="P081",
        prompt_text="Electric vehicle battery pack fireproof thermal runaway insulation barrier between adjacent lithium cells.",
        cluster="Thermal Management",
        loading_mode="thermal_management",
        operating_environment="thermal_runaway_800c",
        regulatory_domain="dielectric_flame_barrier",
        expected_indices=["thermal_insulation"],
        expected_top_materials=["Alumina_Ceramic", "PEEK"],
        mandatory_disqualified=["Aluminium_6061_T6", "Copper_C11000"],
        service_temperature_c=800.0,
    ),
    "P082": EngineeringAuditTestCase(
        test_id="P082",
        prompt_text="Solar photovoltaic inverter cooling radiator heat sink operating under scorching equatorial sun in Garissa Kenya.",
        cluster="Thermal Management",
        loading_mode="thermal_management",
        operating_environment="solar_uv_equatorial",
        regulatory_domain="rural_field_kenya",
        expected_indices=["thermal_conductivity"],
        expected_top_materials=["Aluminium_6061_T6"],
        mandatory_disqualified=["PLA", "ABS"],
    ),
    "P083": EngineeringAuditTestCase(
        test_id="P083",
        prompt_text="High-power LED stadium floodlight luminaire heat sink dissipating 1000 W in outdoor rain.",
        cluster="Thermal Management",
        loading_mode="thermal_management",
        operating_environment="outdoor_rain_sun",
        regulatory_domain="weatherproof_cooling",
        expected_indices=["thermal_conductivity"],
        expected_top_materials=["Aluminium_6061_T6", "Copper_C11000"],
        mandatory_disqualified=["PLA", "PETG"],
    ),
    "P084": EngineeringAuditTestCase(
        test_id="P084",
        prompt_text="Chemical distillation column heat exchanger tube bundle boiling hydrochloric acid.",
        cluster="Thermal Management",
        loading_mode="thermal_management",
        operating_environment="corrosive_acid",
        regulatory_domain="acid_corrosion_heat_exchanger",
        expected_indices=["thermal_conductivity"],
        expected_top_materials=["Titanium_Ti6Al4V", "PEEK"],
        mandatory_disqualified=["Copper_C11000", "Aluminium_6061_T6"],
    ),
    "P085": EngineeringAuditTestCase(
        test_id="P085",
        prompt_text="Rocket nozzle throat thermal regenerative cooling jacket conducting heat to cryogenic propellant.",
        cluster="Thermal Management",
        loading_mode="thermal_management",
        operating_environment="rocket_combustion_1000c",
        regulatory_domain="high_pressure_thermal_flux",
        expected_indices=["thermal_conductivity"],
        expected_top_materials=["Copper_C11000", "Inconel_718"],
        mandatory_disqualified=["PLA", "Alumina_Ceramic"],
    ),
    "P086": EngineeringAuditTestCase(
        test_id="P086",
        prompt_text="Biomedical hyperthermia cancer therapy catheter probe tip conducting heat locally into tumor tissue.",
        cluster="Thermal Management",
        loading_mode="thermal_management",
        operating_environment="in_vivo_biomedical",
        regulatory_domain="iso_10993_biomedical",
        expected_indices=["thermal_conductivity"],
        expected_top_materials=["Titanium_Ti6Al4V", "Stainless_Steel_316L"],
        mandatory_disqualified=["Copper_C11000", "Aluminium_6061_T6"],
    ),
    "P087": EngineeringAuditTestCase(
        test_id="P087",
        prompt_text="Thermoelectric generator (TEG) hot-side thermal coupling spreader on a rural biomass cookstove in Kenya.",
        cluster="Thermal Management",
        loading_mode="thermal_management",
        operating_environment="biomass_fire_350c",
        regulatory_domain="rural_field_kenya",
        expected_indices=["thermal_conductivity"],
        expected_top_materials=["Copper_C11000", "Aluminium_6061_T6"],
        mandatory_disqualified=["PLA", "PETG", "ABS", "PC"],
        service_temperature_c=350.0,
    ),
    "P088": EngineeringAuditTestCase(
        test_id="P088",
        prompt_text="Deep-space probe radioisotope thermoelectric generator (RTG) outer thermal radiator panel.",
        cluster="Thermal Management",
        loading_mode="thermal_management",
        operating_environment="high_vacuum",
        regulatory_domain="space_low_outgassing",
        expected_indices=["thermal_conductivity", "thermal_diffusivity"],
        expected_top_materials=["Aluminium_6061_T6", "CFRP_Prepreg"],
        mandatory_disqualified=["PLA", "TPU_95A"],
    ),

    # -------------------------------------------------------------------------
    # Cluster 8: Pressure Vessels, Tanks & Conduits (P089 - P100)
    # -------------------------------------------------------------------------
    "P089": EngineeringAuditTestCase(
        test_id="P089",
        prompt_text="Ultra-lightweight compressed hydrogen gas storage cylinder operating at 700 bar for a fuel cell racing car.",
        cluster="Pressure Vessels",
        loading_mode="pressure_vessel",
        operating_environment="ambient",
        regulatory_domain="ultra_lightweight_racing",
        expected_indices=["tie_strength", "plate_strength"],
        expected_top_materials=["CFRP_Prepreg", "Titanium_Ti6Al4V"],
        mandatory_disqualified=["PLA", "TPU_95A"],
    ),
    "P090": EngineeringAuditTestCase(
        test_id="P090",
        prompt_text="Rural village gravity-fed municipal drinking water supply plumbing pipe operating under 6 bar water pressure in Kenya.",
        cluster="Pressure Vessels",
        loading_mode="pressure_vessel",
        operating_environment="freshwater_buried",
        regulatory_domain="rural_field_kenya",
        expected_indices=["tie_strength", "plate_strength"],
        expected_top_materials=["PETG", "Stainless_Steel_316L"],
        mandatory_disqualified=["PLA", "Alloy_Steel_4140"],
    ),
    "P091": EngineeringAuditTestCase(
        test_id="P091",
        prompt_text="High-pressure chemical synthesis autoclave reactor operating at 200 bar and 250 C with caustic alkaline solutions.",
        cluster="Pressure Vessels",
        loading_mode="pressure_vessel",
        operating_environment="chemical_caustic_250c",
        regulatory_domain="asme_pressure_code",
        expected_indices=["tie_strength", "plate_strength"],
        expected_top_materials=["Inconel_718", "Stainless_Steel_316L"],
        mandatory_disqualified=["Aluminium_6061_T6", "PLA", "PETG", "ABS", "PC"],
        service_temperature_c=250.0,
    ),
    "P092": EngineeringAuditTestCase(
        test_id="P092",
        prompt_text="Deep-sea manned exploration submersible spherical pressure hull descending to 4,000 meters depth.",
        cluster="Pressure Vessels",
        loading_mode="pressure_vessel",
        operating_environment="deep_ocean_marine",
        regulatory_domain="extreme_fracture_safety",
        expected_indices=["tie_strength", "plate_strength"],
        expected_top_materials=["Titanium_Ti6Al4V"],
        mandatory_disqualified=["Alloy_Steel_4140", "PLA"],
    ),
    "P093": EngineeringAuditTestCase(
        test_id="P093",
        prompt_text="Liquid oxygen cryogenic propellant tank for an orbital launch vehicle stage.",
        cluster="Pressure Vessels",
        loading_mode="pressure_vessel",
        operating_environment="cryogenic_lox",
        regulatory_domain="ultra_lightweight_aerospace",
        expected_indices=["tie_strength", "plate_strength"],
        expected_top_materials=["Aluminium_6061_T6", "Stainless_Steel_316L"],
        mandatory_disqualified=["PLA", "ABS"],
    ),
    "P094": EngineeringAuditTestCase(
        test_id="P094",
        prompt_text="Reusable portable sports water bottle for everyday hydration that survives dishwasher cleaning without leaching chemicals.",
        cluster="Pressure Vessels",
        loading_mode="pressure_vessel",
        operating_environment="dishwasher_75c",
        regulatory_domain="fda_food_contact",
        expected_indices=["tie_strength", "plate_strength"],
        expected_top_materials=["PETG", "Polycarbonate", "Stainless_Steel_316L"],
        mandatory_disqualified=["PLA", "PETG-CF", "PA12-CF"],
    ),
    "P095": EngineeringAuditTestCase(
        test_id="P095",
        prompt_text="Hydraulic accumulator pressure cylinder in a heavy industrial metal stamping press.",
        cluster="Pressure Vessels",
        loading_mode="pressure_vessel",
        operating_environment="hydraulic_mineral_oil",
        regulatory_domain="fatigue_burst_resistance",
        expected_indices=["tie_strength", "plate_strength"],
        expected_top_materials=["Alloy_Steel_4140"],
        mandatory_disqualified=["PLA", "TPU_95A"],
    ),
    "P096": EngineeringAuditTestCase(
        test_id="P096",
        prompt_text="Biomedical implantable drug infusion pump reservoir pressurized inside the human abdominal cavity.",
        cluster="Pressure Vessels",
        loading_mode="pressure_vessel",
        operating_environment="in_vivo_biomedical",
        regulatory_domain="iso_10993_biomedical",
        expected_indices=["tie_strength", "plate_strength"],
        expected_top_materials=["Titanium_Ti6Al4V", "PEEK"],
        mandatory_disqualified=["Aluminium_6061_T6", "Copper_C11000", "Alloy_Steel_4140"],
    ),
    "P097": EngineeringAuditTestCase(
        test_id="P097",
        prompt_text="Industrial vacuum chamber vessel maintaining 10^-8 Torr for semiconductor molecular beam epitaxy.",
        cluster="Pressure Vessels",
        loading_mode="pressure_vessel",
        operating_environment="high_vacuum",
        regulatory_domain="cleanroom_vacuum_bakeable",
        expected_indices=["tie_strength", "plate_strength"],
        expected_top_materials=["Stainless_Steel_316L"],
        mandatory_disqualified=["PLA", "TPU_95A", "PETG"],
    ),
    "P098": EngineeringAuditTestCase(
        test_id="P098",
        prompt_text="Acid storage drum transporting 98% concentrated sulfuric acid on public highways.",
        cluster="Pressure Vessels",
        loading_mode="pressure_vessel",
        operating_environment="corrosive_acid",
        regulatory_domain="un_hazmat_transport",
        expected_indices=["tie_strength", "plate_strength"],
        expected_top_materials=["PEEK", "Stainless_Steel_316L"],
        mandatory_disqualified=["Aluminium_6061_T6", "Alloy_Steel_4140"],
    ),
    "P099": EngineeringAuditTestCase(
        test_id="P099",
        prompt_text="Outdoor compressed air receiver tank for an off-grid solar micro-hydro workshop in Kenya.",
        cluster="Pressure Vessels",
        loading_mode="pressure_vessel",
        operating_environment="humid_tropical",
        regulatory_domain="rural_field_kenya",
        expected_indices=["tie_strength", "plate_strength"],
        expected_top_materials=["Stainless_Steel_316L", "Alloy_Steel_4140"],
        mandatory_disqualified=["PLA", "TPU_95A"],
    ),
    "P100": EngineeringAuditTestCase(
        test_id="P100",
        prompt_text="Pneumatic paintball compressed air cylinder operating at 300 bar carried by players.",
        cluster="Pressure Vessels",
        loading_mode="pressure_vessel",
        operating_environment="ambient_outdoor",
        regulatory_domain="portable_human_safety",
        expected_indices=["tie_strength", "plate_strength"],
        expected_top_materials=["CFRP_Prepreg", "Aluminium_6061_T6"],
        mandatory_disqualified=["PLA", "TPU_95A"],
    ),
}


# Shared module-level fixture for fast RAG & Orchestrator reuse
@pytest.fixture(scope="module")
def audit_system():
    rag = RAGEngine()
    orchestrator = LLMOrchestrator(mode=LLMOrchestrator.MODE_AUTONOMOUS_EXPERT)
    return rag, orchestrator


def execute_audit_test_case(case_id: str, audit_system):
    """
    Executes a single audit test case through the complete engineering pipeline
    and evaluates:
      1. Governing Ashby performance index (M) matches geometry.
      2. Top selected material meets physical thermal limits (T_service < HDT for polymers, creep limits for metals).
      3. Environmental degradation penalties are applied (PLA water hydrolysis -28.4%, ABS UV embrittlement).
      4. Regulatory filters are enforced (no toxic Al in vivo, no loose CF in food contact, no opaque materials in optics).
      5. Dynamic calculation provenance: M_calc mathematically matches physical equation (|M_calc - M_formula|/M <= 10^-4).
      6. Recommended top material is physically sound and matches domain expectations.
      7. No prohibited or disqualified material is selected.
    """
    rag, orchestrator = audit_system
    case = AUDIT_TEST_CASES[case_id]

    # Step 1: NLP Translation Layer
    spec = NLPTranslationLayer.parse_layman_prompt(case.prompt_text)
    primary_index = spec.get("synthesized_engineering_spec", {}).get("primary_governing_ashby_index")

    # Check 1: Governing Ashby performance index matches geometry
    assert primary_index in case.expected_indices, (
        f"[{case_id}] Governing Ashby index mismatch: got '{primary_index}', "
        f"expected one of {case.expected_indices} for loading mode '{case.loading_mode}'"
    )

    # Step 2: RAG Vector Knowledge Base Query
    rag_prompt = rag.build_augmented_prompt(case.prompt_text, spec, top_k=3)
    chunks = rag.query(case.prompt_text, top_k=3)

    # Step 3: LLM Orchestrator Synthesis & Ashby Evaluation
    res = orchestrator.generate_recommendation(
        user_prompt=case.prompt_text,
        engineering_spec=spec,
        rag_prompt=rag_prompt,
        retrieved_chunks=chunks
    )

    ranked = res.get("ranked_materials", [])
    assert len(ranked) > 0, f"[{case_id}] No materials ranked by Ashby engine"
    top_entry = ranked[0]
    top_material_key = top_entry["key"]
    calculated_metric = top_entry["raw_score"]

    # Check 2: Physical thermal deflection limits & creep gating
    temp_c = case.service_temperature_c
    if temp_c is None:
        temp_c = spec.get("numerical_parameters", {}).get("target_service_temperature_c")

    if temp_c is not None:
        mat_db_props = MATERIALS_DATABASE.get(top_material_key, {})
        hdt = mat_db_props.get("heat_deflection_temp")
        if hdt is not None and mat_db_props.get("family") in ["Thermoplastic Polymer", "Thermoplastic Composite", "Elastomeric Polymer"]:
            assert temp_c < hdt, (
                f"[{case_id}] Thermal deflection limit violated: {top_material_key} has HDT={hdt}°C, "
                f"which is exceeded by service temperature {temp_c}°C"
            )
        # Metal creep limit: continuous service above ~0.5 T_melt causes severe creep rupture
        t_melt = mat_db_props.get("melting_point_c")
        if t_melt is not None and mat_db_props.get("family") in ["Metallic Alloy"]:
            t_service_k = temp_c + 273.15
            t_melt_k = t_melt + 273.15
            homologous_t = t_service_k / t_melt_k
            assert homologous_t < 0.55, (
                f"[{case_id}] Creep rupture limit violated: {top_material_key} has homologous temperature "
                f"T_H={homologous_t:.2f} >= 0.55 at service temp {temp_c}°C (T_melt={t_melt}°C)"
            )
        assert not top_entry.get("thermally_inviable", False), (
            f"[{case_id}] Material {top_material_key} was selected despite being marked thermally inviable at {temp_c}°C"
        )

    # Check 3: Environmental degradation penalties applied
    boundary = spec.get("boundary_conditions_and_constraints", {})
    if boundary.get("submerged_aquatic_exposure", False) or case.operating_environment in ["submerged_freshwater", "marine_saltwater"]:
        if "PLA" in case.mandatory_disqualified:
            assert top_material_key != "PLA", (
                f"[{case_id}] Degradation penalty violation: PLA recommended for submerged structural use "
                f"despite empirical 28.4% tensile loss and hydrolytic embrittlement"
            )
    if boundary.get("outdoor_uv_exposure", False) or case.operating_environment in ["solar_uv_equatorial", "solar_uv_outdoor"]:
        if "ABS" in case.mandatory_disqualified:
            assert top_material_key != "ABS", (
                f"[{case_id}] UV penalty violation: ABS recommended for outdoor UV application "
                f"despite severe polybutadiene photo-oxidation embrittlement"
            )
    if boundary.get("is_cryogenic", False) or case.operating_environment == "cryogenic":
        if "Alloy_Steel_4140" in case.mandatory_disqualified:
            assert top_material_key != "Alloy_Steel_4140", (
                f"[{case_id}] DBTT violation: 4140 alloy steel recommended at cryogenic temperatures below DBTT"
            )
    if case.operating_environment == "corrosive_acid":
        if "Aluminium_6061_T6" in case.mandatory_disqualified:
            assert top_material_key != "Aluminium_6061_T6", (
                f"[{case_id}] Chemical corrosion violation: Aluminium 6061 recommended in mineral acid"
            )
    if case.operating_environment == "high_vacuum":
        if "PLA" in case.mandatory_disqualified:
            assert top_material_key != "PLA", (
                f"[{case_id}] Vacuum outgassing violation: PLA recommended in high vacuum"
            )

    # Check 4: Regulatory filters enforced
    if case.regulatory_domain == "iso_10993_biomedical" or boundary.get("biocompatible_implant_required", False):
        assert top_material_key not in ["Aluminium_6061_T6", "Copper_C11000", "Alloy_Steel_4140"], (
            f"[{case_id}] ISO 10993 Cytotoxicity violation: Cytotoxic {top_material_key} recommended in vivo"
        )
    if case.regulatory_domain == "fda_food_contact" or boundary.get("food_contact_safe", False):
        assert top_material_key not in ["PETG-CF", "PA12-CF"], (
            f"[{case_id}] FDA 21 CFR 177 violation: Loose carbon fiber composite {top_material_key} in food contact"
        )
    if case.regulatory_domain == "optical_transparency" or boundary.get("optical_transparency_required", False):
        assert top_material_key in ["Polycarbonate", "PC", "Polycarbonate_Optical"], (
            f"[{case_id}] Optical transparency violation: Opaque {top_material_key} recommended for optical application"
        )
    if case.regulatory_domain == "heavy_crane_hoisting":
        assert top_material_key not in ["Alumina_Ceramic", "PLA", "TPU_95A"], (
            f"[{case_id}] Crane hoisting safety violation: Low-toughness / brittle {top_material_key} recommended"
        )

    # Check 5: Dynamic calculation provenance: M_calc mathematically matches physical equation
    mat_db = MATERIALS_DATABASE.get(top_material_key, {})
    is_water_deg = boundary.get("submerged_aquatic_exposure", False)
    # Copy material and apply empirical drops if in water
    mat_calc = dict(mat_db)
    if is_water_deg:
        t_drop = mat_db.get("water_saturation_tensile_drop", 0.0) / 100.0
        m_drop = mat_db.get("water_saturation_modulus_drop", 0.0) / 100.0
        mat_calc["yield_strength"] = mat_db["yield_strength"] * (1.0 - t_drop)
        mat_calc["youngs_modulus_print_xy"] = mat_db["youngs_modulus_print_xy"] * (1.0 - m_drop)

    expected_raw_metric = calculate_ashby_index(mat_calc, primary_index, use_printed_xy=True)
    if expected_raw_metric > 1e-9:
        rel_diff = abs(calculated_metric - expected_raw_metric) / expected_raw_metric
        assert rel_diff <= 1e-4, (
            f"[{case_id}] Calculation provenance violation: calculated M={calculated_metric:.6f} "
            f"does not match physical formula M={expected_raw_metric:.6f} (rel_diff={rel_diff:.2e} > 1e-4)"
        )

    # Check 6: Recommended top material is physically sound and matches expected selections
    assert top_material_key in case.expected_top_materials, (
        f"[{case_id}] Material selection mismatch: got '{top_material_key}', "
        f"expected one of {case.expected_top_materials}"
    )

    # Check 7: No prohibited or disqualified material is selected
    assert top_material_key not in case.mandatory_disqualified, (
        f"[{case_id}] Mandatory disqualified material '{top_material_key}' was selected!"
    )


# =============================================================================
# 100 INDIVIDUAL TEST FUNCTIONS (P001 - P100)
# =============================================================================

# --- Cluster 1: Bending Beams (P001 - P013) ---
def test_p001_bending_beam_river_turbine(audit_system):
    """P001: River turbine blade in freshwater (Capstone benchmark)."""
    execute_audit_test_case("P001", audit_system)

def test_p002_bending_beam_hydrofoil_strut(audit_system):
    """P002: High-speed hydrofoil strut in seawater."""
    execute_audit_test_case("P002", audit_system)

def test_p003_bending_beam_solar_spar_garissa(audit_system):
    """P003: Outdoor solar tracking spar in Garissa under equatorial UV."""
    execute_audit_test_case("P003", audit_system)

def test_p004_bending_beam_racing_bike_fork(audit_system):
    """P004: Road bicycle competition front fork."""
    execute_audit_test_case("P004", audit_system)

def test_p005_bending_beam_cryogenic_pipe_support(audit_system):
    """P005: Liquid nitrogen transfer pipe support beam at -196 C."""
    execute_audit_test_case("P005", audit_system)

def test_p006_bending_beam_furnace_charging_fork(audit_system):
    """P006: Industrial furnace charging fork cantilever arm at 950 C."""
    execute_audit_test_case("P006", audit_system)

def test_p007_bending_beam_submersible_manipulator(audit_system):
    """P007: Submersible robotic manipulator in deep marine trench (500 bar)."""
    execute_audit_test_case("P007", audit_system)

def test_p008_bending_beam_satellite_solar_boom(audit_system):
    """P008: Deployable satellite solar array boom in hard vacuum."""
    execute_audit_test_case("P008", audit_system)

def test_p009_bending_beam_crane_gantry_boom(audit_system):
    """P009: Marine port heavy-duty crane gantry boom arm (20 ton)."""
    execute_audit_test_case("P009", audit_system)

def test_p010_bending_beam_spinal_fixation_rod(audit_system):
    """P010: Orthopedic spinal fixation rod bridging lumbar vertebrae."""
    execute_audit_test_case("P010", audit_system)

def test_p011_bending_beam_chemical_scrubber_support(audit_system):
    """P011: Chemical scrubber spray nozzle beam in 20% sulfuric acid."""
    execute_audit_test_case("P011", audit_system)

def test_p012_bending_beam_rural_footbridge_joist(audit_system):
    """P012: Remote village pedestrian footbridge cantilever deck joist."""
    execute_audit_test_case("P012", audit_system)

def test_p013_bending_beam_f1_suspension_wishbone(audit_system):
    """P013: Formula 1 suspension double wishbone arm."""
    execute_audit_test_case("P013", audit_system)

# --- Cluster 2: Tensile Ties (P014 - P026) ---
def test_p014_tensile_tie_wind_turbine_guy_wire(audit_system):
    """P014: Guy wire cable stabilizing 50m rural wind turbine."""
    execute_audit_test_case("P014", audit_system)

def test_p015_tensile_tie_racing_spoke_wire(audit_system):
    """P015: Ultra-lightweight competition bicycle tension spoke wire."""
    execute_audit_test_case("P015", audit_system)

def test_p016_tensile_tie_offshore_mooring_hawser(audit_system):
    """P016: Offshore floating platform mooring hawser in seawater."""
    execute_audit_test_case("P016", audit_system)

def test_p017_tensile_tie_space_propulsion_tether(audit_system):
    """P017: Ion propulsion tether wire in high vacuum."""
    execute_audit_test_case("P017", audit_system)

def test_p018_tensile_tie_acid_reactor_agitator(audit_system):
    """P018: Chemical reactor agitator tie rod in 80 C hydrochloric acid."""
    execute_audit_test_case("P018", audit_system)

def test_p019_tensile_tie_mining_hoist_cable(audit_system):
    """P019: Heavy vertical mining hoist elevator cable (15 ton)."""
    execute_audit_test_case("P019", audit_system)

def test_p020_tensile_tie_artificial_achilles_tendon(audit_system):
    """P020: Biocompatible artificial Achilles tendon replacement chord."""
    execute_audit_test_case("P020", audit_system)

def test_p021_tensile_tie_furnace_counterweight_cable(audit_system):
    """P021: Furnace retort counterweight suspension cable at 600 C."""
    execute_audit_test_case("P021", audit_system)

def test_p022_tensile_tie_hydrogen_propellant_strut(audit_system):
    """P022: Liquid hydrogen propellant tank tension strut at -253 C."""
    execute_audit_test_case("P022", audit_system)

def test_p023_tensile_tie_solar_sail_rigging(audit_system):
    """P023: Solar sail stay rigging in deep space UV."""
    execute_audit_test_case("P023", audit_system)

def test_p024_tensile_tie_food_plant_poultry_shackle(audit_system):
    """P024: Sanitary food plant poultry suspension shackle."""
    execute_audit_test_case("P024", audit_system)

def test_p025_tensile_tie_rural_telecom_guy_wire(audit_system):
    """P025: Rapid replacement antenna guy wire in rural Kenya."""
    execute_audit_test_case("P025", audit_system)

def test_p026_tensile_tie_instrument_acoustic_string(audit_system):
    """P026: Acoustic musical instrument high-modulus tension string."""
    execute_audit_test_case("P026", audit_system)

# --- Cluster 3: Shell Plates & Enclosures (P027 - P039) ---
def test_p027_shell_plate_laptop_display_lid(audit_system):
    """P027: Ultra-lightweight laptop chassis display lid."""
    execute_audit_test_case("P027", audit_system)

def test_p028_shell_plate_hydro_turbine_skin(audit_system):
    """P028: Hydro-turbine blade skin faceplate in river water."""
    execute_audit_test_case("P028", audit_system)

def test_p029_shell_plate_submersible_camera_cover(audit_system):
    """P029: Marine submersible camera housing cover plate (100m depth)."""
    execute_audit_test_case("P029", audit_system)

def test_p030_shell_plate_optical_safety_visor(audit_system):
    """P030: Clear optical safety face shield visor."""
    execute_audit_test_case("P030", audit_system)

def test_p031_shell_plate_nitric_acid_fume_baffle(audit_system):
    """P031: Fume hood baffle plate in boiling nitric acid vapors."""
    execute_audit_test_case("P031", audit_system)

def test_p032_shell_plate_automotive_fender_panel(audit_system):
    """P032: Automotive exterior body fender panel under solar UV."""
    execute_audit_test_case("P032", audit_system)

def test_p033_shell_plate_cryogenic_vacuum_barrier(audit_system):
    """P033: Cold-box outer vacuum barrier plate at -80 C."""
    execute_audit_test_case("P033", audit_system)

def test_p034_shell_plate_furnace_radiation_shield(audit_system):
    """P034: Blast furnace thermal radiation shield plate at 1050 C."""
    execute_audit_test_case("P034", audit_system)

def test_p035_shell_plate_dairy_conveyor_drop_plate(audit_system):
    """P035: Sanitary food conveyor drop plate for cheese/dairy."""
    execute_audit_test_case("P035", audit_system)

def test_p036_shell_plate_cranioplasty_brain_shield(audit_system):
    """P036: Biocompatible cranial defect protection plate (cranioplasty)."""
    execute_audit_test_case("P036", audit_system)

def test_p037_shell_plate_solar_cooker_reflector(audit_system):
    """P037: Parabolic solar cooker reflector backing in rural Kenya."""
    execute_audit_test_case("P037", audit_system)

def test_p038_shell_plate_micrometeoroid_space_shield(audit_system):
    """P038: Satellite micrometeoroid protection plate in vacuum."""
    execute_audit_test_case("P038", audit_system)

def test_p039_shell_plate_high_speed_train_nose_fairing(audit_system):
    """P039: High-speed train aerodynamic nose cone fairing plate."""
    execute_audit_test_case("P039", audit_system)

# --- Cluster 4: Rotational Rotors & Centrifuges (P040 - P051) ---
def test_p040_rotational_rotor_energy_storage_flywheel(audit_system):
    """P040: 60,000 RPM flywheel rotor for kinetic energy storage."""
    execute_audit_test_case("P040", audit_system)

def test_p041_rotational_rotor_pelton_runner_wheel(audit_system):
    """P041: Micro-hydro Pelton runner wheel in Kenyan river."""
    execute_audit_test_case("P041", audit_system)

def test_p042_rotational_rotor_clinical_centrifuge(audit_system):
    """P042: Blood fractionation medical centrifuge head at 15,000 RPM."""
    execute_audit_test_case("P042", audit_system)

def test_p043_rotational_rotor_turbocharger_compressor(audit_system):
    """P043: Turbocharger compressor impeller at 120,000 RPM and 180 C."""
    execute_audit_test_case("P043", audit_system)

def test_p044_rotational_rotor_gas_turbine_hot_wheel(audit_system):
    """P044: Gas turbine exhaust wheel in 700 C combustion gas."""
    execute_audit_test_case("P044", audit_system)

def test_p045_rotational_rotor_submersible_bilge_impeller(audit_system):
    """P045: Submersible bilge pump impeller in saltwater sand slurry."""
    execute_audit_test_case("P045", audit_system)

def test_p046_rotational_rotor_dental_drill_turbine(audit_system):
    """P046: 400,000 RPM dental drill turbine requiring 134 C autoclave."""
    execute_audit_test_case("P046", audit_system)

def test_p047_rotational_rotor_ultracentrifuge_tube(audit_system):
    """P047: Gas ultracentrifuge rotor tube operating in high vacuum."""
    execute_audit_test_case("P047", audit_system)

def test_p048_rotational_rotor_methane_turbopump_inducer(audit_system):
    """P048: Liquid methane turbopump inducer impeller at -160 C."""
    execute_audit_test_case("P048", audit_system)

def test_p049_rotational_rotor_food_shear_mixer(audit_system):
    """P049: High-shear food dispersion rotor for baby food puree."""
    execute_audit_test_case("P049", audit_system)

def test_p050_rotational_rotor_engine_ring_gear_flywheel(audit_system):
    """P050: Engine starter ring gear flywheel resisting shock torque."""
    execute_audit_test_case("P050", audit_system)

def test_p051_rotational_rotor_stratosphere_drone_propeller(audit_system):
    """P051: High-altitude drone propulsion propeller in freezing UV."""
    execute_audit_test_case("P051", audit_system)

# --- Cluster 5: Elastic Springs & Dampers (P052 - P063) ---
def test_p052_elastic_damper_smartphone_case(audit_system):
    """P052: Impact absorbing smartphone bumper case."""
    execute_audit_test_case("P052", audit_system)

def test_p053_elastic_damper_offroad_suspension_spring(audit_system):
    """P053: Off-road vehicle suspension coil spring."""
    execute_audit_test_case("P053", audit_system)

def test_p054_elastic_damper_marine_dock_fender(audit_system):
    """P054: Marine dock piling fender bumper absorbing ferry berthing."""
    execute_audit_test_case("P054", audit_system)

def test_p055_elastic_damper_cryogenic_valve_spring(audit_system):
    """P055: Cryogenic valve seal energizer spring in liquid nitrogen (-196 C)."""
    execute_audit_test_case("P055", audit_system)

def test_p056_elastic_damper_furnace_damper_spring(audit_system):
    """P056: Furnace exhaust damper seal spring at 550 C."""
    execute_audit_test_case("P056", audit_system)

def test_p057_elastic_damper_surgical_laparoscopic_hinge(audit_system):
    """P057: Surgical laparoscopic grasper flexural micro-hinge."""
    execute_audit_test_case("P057", audit_system)

def test_p058_elastic_damper_running_shoe_midsole(audit_system):
    """P058: Running shoe midsole cushion for energy return."""
    execute_audit_test_case("P058", audit_system)

def test_p059_elastic_damper_generator_vibration_mount(audit_system):
    """P059: Generator vibration isolation mount in Kenya."""
    execute_audit_test_case("P059", audit_system)

def test_p060_elastic_damper_satellite_separation_latch(audit_system):
    """P060: Spacecraft separation snap-latch spring in high vacuum."""
    execute_audit_test_case("P060", audit_system)

def test_p061_elastic_damper_food_container_snap_hinge(audit_system):
    """P061: Food-safe compliant snap-fit lid hinge."""
    execute_audit_test_case("P061", audit_system)

def test_p062_elastic_damper_optical_mirror_kinematic_flexure(audit_system):
    """P062: Precision optical mirror kinematic mount flexure."""
    execute_audit_test_case("P062", audit_system)

def test_p063_elastic_damper_acid_pump_check_valve_spring(audit_system):
    """P063: Acid pump return spring in concentrated hydrochloric acid."""
    execute_audit_test_case("P063", audit_system)

# --- Cluster 6: Industrial Cutting Tools & Wear (P064 - P075) ---
def test_p064_cutting_tool_sugarcane_machete_kenya(audit_system):
    """P064: Agricultural sugarcane harvesting machete in Kenyan soil."""
    execute_audit_test_case("P064", audit_system)

def test_p065_cutting_tool_titanium_milling_endmill(audit_system):
    """P065: High-speed CNC endmill machining titanium at 800 C."""
    execute_audit_test_case("P065", audit_system)

def test_p066_cutting_tool_food_plant_butcher_knife(audit_system):
    """P066: Food plant rotary butcher knife for frozen beef."""
    execute_audit_test_case("P066", audit_system)

def test_p067_cutting_tool_subsea_rock_trenching_saw(audit_system):
    """P067: Subsea rock trenching saw blade segment in saltwater."""
    execute_audit_test_case("P067", audit_system)

def test_p068_cutting_tool_surgical_microsurgery_scalpel(audit_system):
    """P068: Microsurgery scalpel blade requiring keen sharpness."""
    execute_audit_test_case("P068", audit_system)

def test_p069_cutting_tool_woodworking_planer_blade(audit_system):
    """P069: High-speed planer blade smoothing hardwood."""
    execute_audit_test_case("P069", audit_system)

def test_p070_cutting_tool_recycling_granulator_blade(audit_system):
    """P070: Plastic shredder granulator blade chopping gritty PET bottles."""
    execute_audit_test_case("P070", audit_system)

def test_p071_cutting_tool_bleach_liquor_pump_impeller(audit_system):
    """P071: Shearing impeller in hot chemical bleach pulp."""
    execute_audit_test_case("P071", audit_system)

def test_p072_cutting_tool_arctic_scrap_shredder_tooth(audit_system):
    """P072: Scrap metal shredder shear tooth at -50 C."""
    execute_audit_test_case("P072", audit_system)

def test_p073_cutting_tool_glass_scoring_scribe_wheel(audit_system):
    """P073: Micro-indentation glass scoring wheel scribe."""
    execute_audit_test_case("P073", audit_system)

def test_p074_cutting_tool_kevlar_textile_slitter(audit_system):
    """P074: Rotary cutter blade slitting Kevlar/CFRP fabric."""
    execute_audit_test_case("P074", audit_system)

def test_p075_cutting_tool_rural_carpenter_hand_chisel(audit_system):
    """P075: Hand chisel for rural Kenyan furniture workshop."""
    execute_audit_test_case("P075", audit_system)

# --- Cluster 7: Thermal Management (P076 - P088) ---
def test_p076_thermal_management_cpu_cooler_block(audit_system):
    """P076: High-performance overclocked CPU cooling block heat sink."""
    execute_audit_test_case("P076", audit_system)

def test_p077_thermal_management_satellite_ground_plane(audit_system):
    """P077: Satellite electronics thermal ground plane in vacuum."""
    execute_audit_test_case("P077", audit_system)

def test_p078_thermal_management_culinary_frying_pan(audit_system):
    """P078: Instantaneous hotspot-free cooking pan base at 250 C."""
    execute_audit_test_case("P078", audit_system)

def test_p079_thermal_management_kiln_refractory_barrier(audit_system):
    """P079: Electric kiln refractory insulation barrier at 1100 C."""
    execute_audit_test_case("P079", audit_system)

def test_p080_thermal_management_helium_dewar_neck_insulator(audit_system):
    """P080: Liquid helium dewar insulating support neck at 4 K."""
    execute_audit_test_case("P080", audit_system)

def test_p081_thermal_management_battery_fire_barrier(audit_system):
    """P081: EV battery pack thermal runaway barrier at 800 C."""
    execute_audit_test_case("P081", audit_system)

def test_p082_thermal_management_solar_inverter_radiator_garissa(audit_system):
    """P082: Solar inverter cooling radiator under Garissa equatorial sun."""
    execute_audit_test_case("P082", audit_system)

def test_p083_thermal_management_led_stadium_heatsink(audit_system):
    """P083: 1000W stadium floodlight luminaire outdoor heat sink."""
    execute_audit_test_case("P083", audit_system)

def test_p084_thermal_management_hcl_acid_heat_exchanger(audit_system):
    """P084: Distillation column heat exchanger bundle boiling HCl."""
    execute_audit_test_case("P084", audit_system)

def test_p085_thermal_management_rocket_cooling_jacket(audit_system):
    """P085: Rocket nozzle regenerative cooling jacket at 1000 C."""
    execute_audit_test_case("P085", audit_system)

def test_p086_thermal_management_hyperthermia_cancer_probe(audit_system):
    """P086: Biocompatible cancer hyperthermia catheter probe tip."""
    execute_audit_test_case("P086", audit_system)

def test_p087_thermal_management_biomass_cookstove_teg(audit_system):
    """P087: Rural biomass cookstove TEG thermal spreader at 350 C."""
    execute_audit_test_case("P087", audit_system)

def test_p088_thermal_management_rtg_deep_space_radiator(audit_system):
    """P088: Deep-space RTG generator outer radiator panel in vacuum."""
    execute_audit_test_case("P088", audit_system)

# --- Cluster 8: Pressure Vessels & Conduits (P089 - P100) ---
def test_p089_pressure_vessel_700bar_hydrogen_tank(audit_system):
    """P089: 700 bar compressed hydrogen tank for fuel cell racecar."""
    execute_audit_test_case("P089", audit_system)

def test_p090_pressure_vessel_rural_water_pipe_kenya(audit_system):
    """P090: Rural gravity-fed municipal drinking water pipe (6 bar)."""
    execute_audit_test_case("P090", audit_system)

def test_p091_pressure_vessel_chemical_autoclave_250c(audit_system):
    """P091: Chemical synthesis autoclave reactor (200 bar, 250 C)."""
    execute_audit_test_case("P091", audit_system)

def test_p092_pressure_vessel_deep_sea_submersible_hull(audit_system):
    """P092: Manned exploration submersible pressure hull (4,000m depth)."""
    execute_audit_test_case("P092", audit_system)

def test_p093_pressure_vessel_liquid_oxygen_rocket_tank(audit_system):
    """P093: Orbital launch vehicle liquid oxygen propellant tank."""
    execute_audit_test_case("P093", audit_system)

def test_p094_pressure_vessel_reusable_water_bottle(audit_system):
    """P094: Dishwasher-safe (75 C) reusable sports hydration bottle."""
    execute_audit_test_case("P094", audit_system)

def test_p095_pressure_vessel_hydraulic_stamping_press_cylinder(audit_system):
    """P095: Industrial metal stamping press hydraulic accumulator cylinder."""
    execute_audit_test_case("P095", audit_system)

def test_p096_pressure_vessel_implantable_infusion_reservoir(audit_system):
    """P096: Implantable biomedical drug infusion pump reservoir."""
    execute_audit_test_case("P096", audit_system)

def test_p097_pressure_vessel_semiconductor_mbe_vacuum_chamber(audit_system):
    """P097: Semiconductor molecular beam epitaxy vacuum vessel (10^-8 Torr)."""
    execute_audit_test_case("P097", audit_system)

def test_p098_pressure_vessel_sulfuric_acid_highway_tanker(audit_system):
    """P098: Highway transport drum for 98% concentrated sulfuric acid."""
    execute_audit_test_case("P098", audit_system)

def test_p099_pressure_vessel_workshop_compressed_air_tank(audit_system):
    """P099: Off-grid workshop compressed air receiver tank in Kenya."""
    execute_audit_test_case("P099", audit_system)

def test_p100_pressure_vessel_paintball_compressed_air_tank(audit_system):
    """P100: Portable 300 bar pneumatic paintball compressed air cylinder."""
    execute_audit_test_case("P100", audit_system)
