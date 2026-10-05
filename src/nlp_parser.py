"""
Natural Language Translation Layer for Engineering Intent Parsing.
Translates colloquial, non-technical layman prompts into structured mechanical
engineering parameters, boundary conditions, and Ashby performance constraints.
"""

from typing import Dict, Any, List, Optional
import os
import re
from src.ashby_engine import AshbyIndex, derive_selection_guide

_ML_INTENT_MODEL = None


def _get_ml_intent_model():
    """Lazily load the trained pure-numpy ML intent model."""
    global _ML_INTENT_MODEL
    if _ML_INTENT_MODEL is None:
        model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "nlp_intent_model.json")
        if os.path.exists(model_path):
            try:
                from src.train_nlp import MultiOutputIntentModel
                _ML_INTENT_MODEL = MultiOutputIntentModel.load(model_path)
            except Exception:
                _ML_INTENT_MODEL = False
        else:
            _ML_INTENT_MODEL = False
    return _ML_INTENT_MODEL if _ML_INTENT_MODEL is not False else None


class NLPTranslationLayer:
    """
    Translates unstructured layman intent into structured engineering specifications,
    extracts explicit and implicit constraints, and binds them to Ashby optimization models.
    """

    @classmethod
    def get_ml_intent_model(cls):
        """Access the trained ML intent model."""
        return _get_ml_intent_model()

    @classmethod
    def _get_ml_intent_model(cls):
        return _get_ml_intent_model()

    @classmethod
    def predict_ml_intent(cls, prompt: str):
        """Predict component and Ashby index from text using trained ML model."""
        model = _get_ml_intent_model()
        if model is None:
            return None, None, None
        return model.predict(prompt)

    @classmethod
    def parse_layman_prompt(cls, prompt: str) -> Dict[str, Any]:
        """
        Parse non-technical prompt into structured engineering requirements.
        Handles queries like:
        "I want to make a blade that will push water, carry a heavy load,
         and sit in a river all day, but I don't know the exact weight."
        """
        prompt_clean = prompt.strip()
        prompt_lower = prompt_clean.lower()

        # 1. Physical Domain & Function Identification
        # 1. Physical Domain & Function Identification (Comprehensive Everyday Layman Engine)
        component_type = "generic_mechanical_component"
        
        # Check culinary cookware with whole-word boundary to avoid matching "panel", "japan", etc.
        import re
        is_cookware = bool(re.search(r'\b(?:cooking pan|frying pan|saucepan|pan|pans|pot|pots|skillet|cookware|baking sheet|wok|kettle|kitchen pan)\b', prompt_lower)) and not any(p in prompt_lower for p in ["panel", "panels", "company", "japan", "expand", "reflector", "solar cooker", "solar"])
        # Pressure cooker vessel body resisting internal pressure is a structural containment shell, not thermal cookware
        if "pressure cooker" in prompt_lower and any(w in prompt_lower for w in ["pressure", "vessel", "bar", "burst", "steam"]):
            is_cookware = False

        # Distinguish food dining plates from structural cold plates, armor plates, and baseplates
        is_food_plate = bool(re.search(r'\b(?:dinner plate|eating plate|food plate|serving plate|paper plate|saucer)\b', prompt_lower))

        # Cutting tool / blade detection (Must precede bottle / optical glass detection)
        is_cutting_tool = bool(re.search(
            r'\b(?:knife|cutting blade|machete|sword|chisel|saw blade|scissors|shears|scraper|axe|scalpel|'
            r'planer|wood planer|planer blade|shredder blade|granulator blade|rock saw|saw segment|shear blade|'
            r'guillotine|scoring wheel|glass scribe|glass scribing|wire cutter|bone saw|slitter|slitter blade|'
            r'textile slitter|endmill|milling endmill|rotary cutter|shearing impeller|shear tooth|shredder tooth|cutter tooth)\b',
            prompt_lower
        )) and not any(w in prompt_lower for w in ["turbine blade", "runner blade"]) or ("shearing impeller" in prompt_lower)

        # Pure tension member / cable / tie detection
        is_pure_tension = bool(re.search(
            r'\b(?:suspender rope|hoist cable|tendon tie|tendon|tendons|spoke wire|spoke|spokes|stay wire|stay|stays|'
            r'guy wire|guy wires|pure tension|tie-rod|tie rod|tether|tethers|tension-leg|tensile cable|tensile wire|'
            r'tensile chord|mooring tether|mooring tethers|mooring hawser|suspender cable|suspender cables|suspension links|'
            r'post-tensioning|tension string|shackle tie|suspension shackle|stay rigging|propellant tank tension|'
            r'tension suspension|hoist.*cable|elevator.*cable|tension tie|tension spoke|tension chord)\b',
            prompt_lower
        )) or (
            bool(re.search(r'\b(?:cable|wire|rope|tether|rigging|shackle)\b', prompt_lower)) and
            any(w in prompt_lower for w in ["tension", "hoist", "lift", "elevator", "suspension", "guy", "spoke", "rigging", "tether", "tie", "string", "pull", "axial"])
        )

        # Pressure vessel & fluid/gas containment detection
        # Note: Exclude high-speed rotating equipment that mentions autoclave sterilization
        is_autoclave_cleaning = any(w in prompt_lower for w in ["dental drill", "turbine rotor", "rotor", "impeller", "flywheel"]) and "autoclave" in prompt_lower
        is_pressure_vessel = not is_autoclave_cleaning and (bool(re.search(
            r'\b(?:pressure vessel|pressure chamber|autoclave|storage tank|fuel tank|fermentation tank|'
            r'accumulator cylinder|cng tank|lox tank|propellant tank|vacuum chamber|uhv chamber|gas cylinder|'
            r'compressed gas|cng fuel|co2 pneumatic|infusion reservoir|reservoir pouch|transmission conduit|'
            r'conduit pipe|external pressure hull|pressure hull|air receiver tank|compressed air tank|'
            r'compressed air receiver|water pipe|municipal drinking water pipe|drinking water pipe|'
            r'hydration bottle|acid storage drum|storage drum|tanker|compressed air cylinder|vacuum vessel|'
            r'storage cylinder|pressure cylinder|gas storage cylinder|air cylinder|water bottle|sports bottle|'
            r'accumulator pressure cylinder|paintball compressed air|compressed air|receiver tank)\b',
            prompt_lower
        )) or any(w in prompt_lower for w in [
            "pressure vessel", "pressure hull", "autoclave chamber", "accumulator cylinder",
            "gas cylinder", "fermentation tank", "saline infusion", "uhv chamber", "storage tank",
            "conduit pipe", "receiver tank", "pressurized inside", "air receiver", "compressed air tank",
            "compressed air cylinder", "air cylinder", "vacuum chamber", "vacuum vessel", "water bottle"
        ]) or (
            any(w in prompt_lower for w in ["bar", "psi", "kpa", "mpa", "torr", "10^-8", "vacuum"]) and
            any(w in prompt_lower for w in ["cylinder", "tank", "vessel", "accumulator", "pipe", "conduit", "bottle", "hull", "chamber", "drum"])
        ))

        # Thermal insulation detection
        is_thermal_insulator = bool(re.search(
            r'\b(?:thermal insulation|insulator|insulation barrier|thermal barrier|refractory barrier|'
            r'dewar neck|dewar support|fire barrier|thermal runaway|fireproof barrier|contain heat|'
            r'insulation board|kiln refractory|insulating liner|thermal insulating|insulating support neck|'
            r'fireproof thermal runaway|insulating neck|boiler|handle|door knob|pot handle|pan handle)\b',
            prompt_lower
        )) or any(w in prompt_lower for w in ["thermal insulation", "insulation refractory barrier", "fireproof thermal runaway", "thermal runaway barrier"])

        # Shell Plate detection (covers lids, fairings, baffles, panels, vacuum barriers)
        is_plate_shell = any(w in prompt_lower for w in [
            "laptop lid", "display lid", "exterior lid shell", "enclosure wall", "cylinder tank wall", "tank wall",
            "speaker diaphragm", "baffle", "fender panel", "body panel", "drop plate", "reflector backing",
            "parabolic reflector", "fairing plate", "nose cone fairing", "camera housing window cover",
            "vacuum barrier plate", "cranial defect protection plate", "cranioplasty", "brain shield"
        ]) or (
            "fender" in prompt_lower and not any(w in prompt_lower for w in ["bumper", "dock", "piling", "berthing", "cushion"])
        ) or (
            "plate" in prompt_lower and not any(w in prompt_lower for w in ["cold plate", "baseplate", "dinner plate", "food plate", "serving plate"])
        )

        if is_cutting_tool:
            component_type = "cutting_tool_or_blade"
        elif is_pure_tension:
            component_type = "pure_tension_tie"
        elif is_plate_shell:
            component_type = "structural_plate_or_shell"
        elif is_pressure_vessel:
            component_type = "pressure_vessel_or_containment"
        elif is_thermal_insulator:
            component_type = "thermal_insulation_barrier"
        elif is_cookware:
            component_type = "culinary_thermal_ware"
        elif is_food_plate or any(w in prompt_lower for w in ["spoon", "cutlery", "spatula", "bowl", "chopsticks"]) or bool(re.search(r'\b(?:eating fork|table fork|dinner fork|cutlery fork)\b', prompt_lower)):
            component_type = "food_contact_utensil"
        elif any(w in prompt_lower for w in ["water bottle", "bottle", "jug", "flask", "canister", "jar", "canteen", "liquid container"]):
            component_type = "fluid_containment_vessel"
        elif any(w in prompt_lower for w in ["heatsink", "heat sink", "cpu", "gpu", "cooler", "cooling fin", "cool electronics", "thermal conduction", "heat spreader", "cold plate", "baseplate", "thermal baseplate", "heat pipe", "busbar", "thermal anchor", "cooling jacket", "heat exchanger", "catheter probe tip", "thermal coupling spreader"]) or ("radiator" in prompt_lower and not is_thermal_insulator):
            component_type = "thermal_management_heat_sink"
        elif any(w in prompt_lower for w in ["clear like glass", "transparent", "see-through", "optical glass", "window", "lens", "visor", "hud visor", "face shield", "spectacle", "goggles", "viewport", "dome cover", "camera dome"]):
            component_type = "transparent_optical_component"
        elif any(w in prompt_lower for w in ["recoil damping", "recoil pad", "vibration isolation", "mounting foot", "peristaltic", "pump tubing", "helmet foam", "foam liner", "midsole", "shoe sole", "landing gear skid", "landing skid", "buffer pad", "coupler buffer", "conveyor belt scraper", "valve seal spring", "damper flap seal spring", "check-valve return spring", "return spring", "snap-latch", "compliant spring", "kinematic mount flexure", "compliant flexural micro-hinge", "snap-fit lid hinge", "compliant flexure", "bumper", "fender bumper"]):
            component_type = "elastic_suspension_or_damping"
        elif any(w in prompt_lower for w in ["flywheel", "spindle", "motor shaft", "drive shaft", "rotor shaft", "router motor shaft", "coupling", "centrifuge", "dental drill", "compressor wheel", "impeller wheel", "turbine disk", "scanner mirror", "rotor tube", "pelton runner", "runner wheel", "bilge pump open impeller", "turbopump inducer", "dispersion rotor", "starter ring gear flywheel", "propulsion propeller", "propeller", "turbine wheel", "exhaust turbine"]) and not any(w in prompt_lower for w in ["paddle", "kayak", "oar"]):
            component_type = "rotational_drive_element"
        elif any(w in prompt_lower for w in ["armor plate", "ballistic", "bulletproof", "armor", "shield plate", "door armor"]):
            component_type = "ballistic_armor_plate"
        elif any(w in prompt_lower for w in ["shoe sole", "shoe", "boot", "sneaker", "sandal", "insole", "footwear", "tread"]):
            component_type = "wear_cushion_footwear"
        elif (bool(re.search(r'\b(?:rubber|rubbery|silicone|gasket|wristband|strap|o-ring)\b', prompt_lower)) or any(w in prompt_lower for w in ["flexible like rubber", "squishy", "soft and squishy"])) and "scrubber" not in prompt_lower:
            component_type = "flexible_elastomeric_component"
        elif any(w in prompt_lower for w in ["toy", "figurine", "kid", "cheap model", "quick print", "test a model", "hobby model", "miniature"]):
            component_type = "rapid_prototyping_or_toy"
        elif any(w in prompt_lower for w in ["door hinge", "hinge", "latch", "clamp", "bolt", "screw", "heavy hinge", "fastener"]) and not any(w in prompt_lower for w in ["compliant", "snap-fit", "flexure"]):
            component_type = "structural_hardware_or_pivot"
        elif any(w in prompt_lower for w in ["support beam", "pipe support", "cantilever beam", "beam", "spar", "arm", "lever", "cantilever", "bracket", "mount", "mounting bracket", "solar bracket", "joist", "deck joist", "boom", "gantry boom"]):
            component_type = "structural_cantilever_beam"
        elif any(w in prompt_lower for w in ["broken pipe", "plumbing", "water pipe", "drain pipe", "fluid tube", "conduit"]) or ("pipe" in prompt_lower and not any(p in prompt_lower for p in ["phone", "heat pipe", "support", "beam", "cantilever"])):
            component_type = "fluid_conduit_plumbing"
        elif any(w in prompt_lower for w in ["chair", "table", "desk", "stool", "bench", "shelf", "shelving", "bed frame", "furniture", "bookcase"]):
            component_type = "structural_furniture_or_load_frame"
        elif any(w in prompt_lower for w in ["car bumper", "dashboard"]) or ("bumper" in prompt_lower and any(w in prompt_lower for w in ["car", "automotive", "vehicle", "chassis"])):
            component_type = "automotive_impact_component"
        elif bool(re.search(r'\b(?:drone|quadcopter|drone arm|drone frame|rc plane|wing|wings|fuselage|aircraft|airplane)\b', prompt_lower)) and not any(w in prompt_lower for w in ["skid", "landing gear", "chewing", "propeller", "car", "automotive", "spoiler", "sports car"]):
            component_type = "aerospace_airframe_or_drone"
        elif any(w in prompt_lower for w in ["roof", "roofing", "gutter", "solar mount", "fence", "pergola", "outdoor pole", "facade", "awning"]):
            component_type = "outdoor_architectural_structure"
        elif any(w in prompt_lower for w in ["boat", "hull", "canoe", "kayak", "surfboard", "paddle", "oar", "rudder", "paddle shaft"]):
            component_type = "marine_vessel_or_hull"
        elif any(w in prompt_lower for w in ["bike", "bicycle", "scooter", "skateboard", "rollerblade", "wheelchair", "fork", "wishbone", "chassis", "pole vault", "vaulting pole", "springboard", "diving board"]):
            component_type = "structural_frame_or_chassis"
        elif any(w in prompt_lower for w in ["implant", "biomedical", "hip", "knee", "bone", "prosthetic", "surgical", "femoral", "spinal", "spine", "molar crown", "dental"]) or (bool(re.search(r'\bcoping\b', prompt_lower)) and "telescoping" not in prompt_lower):
            component_type = "biomedical_device_or_implant"
        elif any(w in prompt_lower for w in ["phone case", "protective case", "cushion", "enclosure", "housing", "strong box", "box to hold", "box to keep", "toolbox"]) or (bool(re.search(r'\bbox\b', prompt_lower)) and "cold-box" not in prompt_lower and "cold box" not in prompt_lower):
            component_type = "protective_housing_or_case"
        elif any(w in prompt_lower for w in ["crane", "hook", "gantry", "winch", "heavy axle", "lifting hook", "hoist", "pallet rack", "ladder rung"]):
            component_type = "heavy_duty_lifting_or_crane"
        elif any(w in prompt_lower for w in ["gear", "bushing", "bearing", "pulley", "low friction", "sliding"]):
            component_type = "low_friction_gear_or_bushing"
        elif any(w in prompt_lower for w in ["furnace", "kiln", "crucible", "refractory", "foundry ladle", "hearth stone", "baking hearth", "oven", "exhaust", "rocket nozzle", "manifold", "700 c", "350 c", "500 c", "650 c", "800 c", "900 c", "1000 c"]):
            component_type = "high_temperature_thermal_barrier"
        elif any(w in prompt_lower for w in ["spoiler", "car spoiler", "rear wing", "trunk wing", "downforce wing", "front splitter", "diffuser", "canard", "dive plane"]) or ("wing" in prompt_lower and any(c in prompt_lower for c in ["car", "automotive", "track", "race", "sports", "downforce"])):
            component_type = "automotive_aerodynamic_wing_or_spoiler"
        elif any(w in prompt_lower for w in ["wind turbine", "wind generator", "wind rotor"]) and any(w in prompt_lower for w in ["blade", "blades", "aerofoil", "vane", "rotor"]):
            component_type = "wind_turbine_blade"
        elif any(w in prompt_lower for w in ["blade", "impeller", "runner", "propeller", "rotor", "turbomachine", "push water", "water wheel", "turbine"]):
            component_type = "turbine_blade_or_impeller"
        elif any(w in prompt_lower for w in ["spring", "shock", "damper", "buffer", "bumper"]):
            component_type = "elastic_suspension_or_damping"

        # Fallback to trained Machine Learning Intent Model if still generic
        if component_type == "generic_mechanical_component":
            ml_model = _get_ml_intent_model()
            if ml_model is not None:
                try:
                    ml_pred = ml_model.predict(prompt_clean)
                    if ml_pred.get("component_confidence", 0.0) >= 0.15:
                        component_type = ml_pred["component_classification"]
                except Exception:
                    pass

        # 2. Environmental Constraints Translation
        # Distinguish actual submerged river / hydrokinetic environments from bottles/cups
        is_submerged = any(w in prompt_lower for w in [
            "river", "submerged", "underwater", "aquatic", "stream",
            "sit in a river", "wet", "lake", "ocean", "marine", "rapids", "flood"
        ]) or (
            bool(re.search(r'\b(?:hydro|hydro-turbine|hydroelectric|hydrokinetic|hydrodynamic|hydrofoil)\b', prompt_lower))
        ) or (
            "water" in prompt_lower and (
                any(w in prompt_lower for w in [
                    "push water", "sit in a river", "stream", "flow", "submerged", "boat", "hull", "marine",
                    "for water", "in water", "under water", "submerge", "river", "spin", "spinning", "blade", "runner", "impeller", "propeller"
                ]) and not any(w in prompt_lower for w in ["bottle", "jug", "cup", "canteen", "flask", "pipe", "plumbing"])
            )
        )

        # Layman: "sun", "sunlight", "outdoor", "uv", "outside", "kenya", "car", "automotive", "spoiler", "wind turbine"
        is_outdoor_uv = any(w in prompt_lower for w in [
            "sun", "sunlight", "outdoor", "outside", "uv", "equator", "weather", "roof", "roofing", "solar",
            "car", "automotive", "vehicle", "spoiler", "wind turbine", "wind generator"
        ]) or ("kenya" in prompt_lower and not is_submerged)

        # Chemical / Saline
        is_strong_acid = any(w in prompt_lower for w in [
            "hydrochloric", "sulfuric", "nitric", "30% acid", "concentrated acid", "acid storage",
            "hcl", "h2so4", "bleach liquor", "hot bleach", "acid vapor", "acid bath", "caustic", "acid drum"
        ])
        is_chem_exposure = is_strong_acid or any(w in prompt_lower for w in [
            "acid", "chemical", "salt", "saline", "seawater", "saltwater", "corrosive", "oil", "fuel", "petrol", "ocean", "marine"
        ])
        is_marine_industrial = any(w in prompt_lower for w in [
            "submarine", "deep ocean", "300 bar", "wellhead", "2000m", "offshore", "desalination", "reverse osmosis",
            "trawler", "hydrofoil", "commercial fishing", "marine port", "subsea", "trenching", "saline"
        ])

        # Refractory & High Temperature Inference
        is_refractory = any(w in prompt_lower for w in [
            "furnace", "crucible", "refractory", "foundry ladle", "hearth stone", "baking hearth",
            "combustion", "900 c", "700 c", "800 c", "1000 c", "1100 c", "450 c", "650 c", "500 c", "350 c", "400 c",
            "fireproof", "thermal runaway"
        ]) or ("kiln" in prompt_lower and not any(k in prompt_lower for k in ["kiln-dried", "kiln dried"]))
        is_high_temp = any(w in prompt_lower for w in [
            "hot", "heat", "high temperature", "thermal", "boiling", "exhaust", "engine", "oven", "furnace", "boiler"
        ]) or is_cookware or is_refractory

        # 3. Structural Mechanics & Loading Intent
        high_load_intent = any(w in prompt_lower for w in [
            "heavy load", "heavy weight", "strong", "huge force", "high load",
            "heavy", "carry", "push water", "not break", "won't snap", "durable",
            "10-ton", "2000 kg", "800 mpa", "300 bar"
        ])

        cyclical_fatigue_intent = any(w in prompt_lower for w in [
            "push water", "all day", "continuous", "cyclical", "spin", "spinning",
            "rotating", "constantly", "24/7", "fatigue", "vibration", "turbulent",
            "impeller", "runner", "propeller", "turbine", "rotor", "alternating", "pedal", "cycle", "rpm"
        ])

        lightweight_intent = any(w in prompt_lower for w in [
            "light", "lightweight", "low mass", "portable", "weightless", "minimize weight", "ultralight", "racing", "high-speed"
        ])

        low_cost_intent = any(w in prompt_lower for w in [
            "cheap", "affordable", "low cost", "budget", "inexpensive", "cost-effective", "economical"
        ])

        # Domain Specific Flags
        is_heavy_infrastructure = bool(re.search(
            r'\b(?:gantry crane|crane|gantry|hoist|elevator|10-ton|20 ton|15 ton|10 ton|\d+\s*ton|'
            r'shipping container|pallet rack|broadcast tower|guy wire|antenna mast|mast|footbridge|joist|deck joist|infrastructure)\b',
            prompt_lower
        )) or any(w in prompt_lower for w in ["gantry crane", "crane gantry", "20 ton", "15 ton", "shipping container", "pallet rack", "mining hoist", "antenna mast", "footbridge"])
        is_spinal = any(w in prompt_lower for w in ["spinal", "spine", "lumbar", "interbody cage", "vertebral"])
        is_dental = any(w in prompt_lower for w in ["dental", "molar crown", "mastication"]) or (bool(re.search(r'\bcoping\b', prompt_lower)) and "telescoping" not in prompt_lower)
        is_gear_dry = any(w in prompt_lower for w in ["spur gear", "gear", "bushing", "ring gear"]) and any(w in prompt_lower for w in ["dry", "self-lubricating", "food processing", "starter ring gear", "torque shocks"])
        is_ballistic = any(w in prompt_lower for w in ["ballistic", "bulletproof", "7.62mm", "rifle rounds", "armor plate", "armor"])
        is_brake_caliper = any(w in prompt_lower for w in ["brake caliper", "caliper bridge", "racing brake"])
        is_pressure_vessel_certified = is_pressure_vessel or any(w in prompt_lower for w in ["200 bar", "300 bar", "700 bar", "6 bar", "scuba", "compressed air tank", "pressure cooker", "autoclave", "accumulator", "storage drum", "compressed air cylinder", "air cylinder"])
        is_spoke_wire = any(w in prompt_lower for w in ["spoke wire", "wheel spoke"])
        is_balloon_tether = any(w in prompt_lower for w in ["weather balloon", "balloon suspension"])
        is_battery_shield = any(w in prompt_lower for w in ["battery pack", "bottom shield", "road debris puncture"])
        is_speaker_cone = any(w in prompt_lower for w in ["speaker diaphragm", "cone plate", "acoustic speaker"])
        is_machine_spindle = any(w in prompt_lower for w in ["spindle router", "woodworking spindle", "router motor shaft"])
        is_lox = any(w in prompt_lower for w in ["liquid oxygen", "lox"])

        # 4. Additive Manufacturing Context vs Subtractive / CNC vs Universal
        is_explicit_3d_print = any(w in prompt_lower for w in [
            "3d print", "3d-print", "3d-printed", "3d printing", "fdm", "filament",
            "additive manufacturing", "3d printer nozzle", "print nozzle", "layer line", "extruder", "slicer", "infill"
        ])
        is_explicit_cnc = any(w in prompt_lower for w in [
            "cnc", "cast", "casting", "foundry", "forge", "lathe", "mill", "milling",
            "machining", "subtractive", "metal only", "sheet metal", "weld", "welding"
        ]) or is_marine_industrial or is_heavy_infrastructure

        # Candidate materials explicitly mentioned in prompt
        specified_materials = []
        if "stainless" in prompt_lower or "316l" in prompt_lower:
            specified_materials.append("Stainless_Steel_316L")
        if "aluminium" in prompt_lower or "aluminum" in prompt_lower or "6061" in prompt_lower:
            specified_materials.append("Aluminium_6061_T6")
        if "titanium" in prompt_lower or "ti-6al-4v" in prompt_lower:
            specified_materials.append("Titanium_Ti6Al4V")
        if "copper" in prompt_lower:
            specified_materials.append("Copper_C11000")
        if "inconel" in prompt_lower or "718" in prompt_lower:
            specified_materials.append("Inconel_718")
        if "peek" in prompt_lower:
            specified_materials.append("PEEK")
        if "tpu" in prompt_lower:
            specified_materials.append("TPU_95A")
        if "delrin" in prompt_lower or "pom" in prompt_lower or "polyoxymethylene" in prompt_lower:
            specified_materials.append("POM_Delrin")
        if "cfrp" in prompt_lower or "carbon fiber prepreg" in prompt_lower:
            specified_materials.append("CFRP_Prepreg")
        if "alumina" in prompt_lower or "ceramic" in prompt_lower:
            specified_materials.append("Alumina_Ceramic")

        # Determine manufacturing route
        if is_explicit_3d_print and not is_explicit_cnc:
            mfg_process_label = "FDM Additive Manufacturing"
            fdm_only_preference = True
        elif is_explicit_cnc and not is_explicit_3d_print:
            mfg_process_label = "Conventional Subtractive/Machining"
            fdm_only_preference = False
        else:
            # Decentralized micro-hydro turbine blade baseline (capstone specification)
            is_micro_hydro_blade = (is_submerged or "river" in prompt_lower or "push water" in prompt_lower) and (
                component_type in ["turbine_blade_or_impeller", "turbomachine_blade"] or "spinning thing" in prompt_lower or "blade" in prompt_lower
            ) and not is_marine_industrial
            if is_micro_hydro_blade and not is_explicit_cnc:
                mfg_process_label = "FDM Additive Manufacturing (Decentralized Micro-Hydro)"
                fdm_only_preference = True
            else:
                # Universal Material Selection across all manufacturing routes
                mfg_process_label = "Universal Multi-Process Evaluation (Additive, Subtractive, Composites & Casting)"
                fdm_only_preference = False

        # 5. Extract Explicit Numerical Constraints if present
        target_yield_mpa = cls._extract_regex_float(prompt_clean, r'(\d+(?:\.\d+)?)\s*(?:mpa|megapascal)')
        target_velocity_ms = cls._extract_regex_float(prompt_clean, r'(\d+(?:\.\d+)?)\s*(?:m/s|meter(?:s)? per second)')
        target_chord_mm = cls._extract_regex_float(prompt_clean, r'(\d+(?:\.\d+)?)\s*(?:mm|millimeter)')
        target_temp_c = cls._extract_regex_float(prompt_clean, r'(-?\d+(?:\.\d+)?)\s*(?:°\s*c|celsius|deg\s*c|\bc\b)')
        if target_temp_c is None:
            if any(w in prompt_lower for w in ["thermal runaway", "fireproof", "battery pack fireproof"]):
                target_temp_c = 800.0
            elif is_refractory:
                if ("kiln" in prompt_lower and not any(k in prompt_lower for k in ["kiln-dried", "kiln dried"])) or any(w in prompt_lower for w in ["foundry", "crucible", "combustion", "1100", "1000", "900", "800"]):
                    target_temp_c = 1000.0
                elif any(w in prompt_lower for w in ["furnace", "hearth", "refractory", "wastegate", "700", "650"]):
                    target_temp_c = 650.0
                else:
                    target_temp_c = 450.0
            elif any(w in prompt_lower for w in ["autoclave", "boiling", "bleach liquor"]):
                target_temp_c = 134.0

        if target_temp_c is not None and target_temp_c > 65.0:
            is_high_temp = True
        is_cryogenic = any(w in prompt_lower for w in ["cryo", "liquid nitrogen", "liquid helium", "liquid oxygen", "liquid hydrogen", "dewar", "below zero", "-50", "-70", "-100", "-120", "-162", "-183", "-196", "-253", "-269", "4 kelvin"])
        if target_temp_c is not None and target_temp_c < -20.0:
            is_cryogenic = True
        is_dewar_strut = is_cryogenic and any(w in prompt_lower for w in ["strut", "dewar support", "dewar strut", "suspension strut"]) and not any(w in prompt_lower for w in ["busbar", "thermal anchor busbar", "conductor"])

        # 6. Deduce Ashby Performance Index based on Physical Domain Intent
        if is_speaker_cone:
            ashby_key = AshbyIndex.PLATE_STIFFNESS
            ashby_reasoning = "Acoustic speaker cone/diaphragm requiring maximum high-frequency flexural stiffness per unit mass: M = E^(1/3) / ρ."
        elif component_type in ["pressure_vessel_or_containment", "fluid_containment_vessel", "fluid_conduit_plumbing"]:
            if any(w in prompt_lower for w in ["stiffness", "rigidity", "deflection"]):
                ashby_key = AshbyIndex.PLATE_STIFFNESS
                ashby_reasoning = "Containment shell requiring minimum flexural deflection: M = E^(1/3) / ρ."
            else:
                ashby_key = AshbyIndex.TIE_STRENGTH
                ashby_reasoning = "Pressure containment shell / conduit governed by hoop stress and yield burst pressure per unit mass: M = σ_y / ρ."
        elif component_type == "thermal_insulation_barrier":
            ashby_key = AshbyIndex.THERMAL_INSULATION
            ashby_reasoning = "Thermal barrier and heat flow minimization: M = 1 / λ."
        elif component_type in ["thermal_management_heat_sink", "culinary_thermal_ware"]:
            ashby_key = AshbyIndex.THERMAL_CONDUCTIVITY
            ashby_reasoning = "Thermal conduction and rapid heat spreading (Fourier physics): M = λ."
        elif component_type in ["wear_cushion_footwear", "flexible_elastomeric_component", "elastic_suspension_or_damping"]:
            ashby_key = AshbyIndex.ELASTIC_ENERGY
            ashby_reasoning = "Elastic energy mitigation, impact damping, and maximum reversible deflection: M = σ_y^2 / E."
        elif component_type == "transparent_optical_component":
            ashby_key = AshbyIndex.PLATE_STRENGTH
            ashby_reasoning = "Optical transparency with shatter resistance: M = σ_y^(1/2) / ρ."
        elif component_type == "cutting_tool_or_blade":
            ashby_key = AshbyIndex.TIE_STRENGTH
            ashby_reasoning = "Cutting tool / blade requiring maximum edge yield strength and wear resistance: M = σ_y / ρ."
        elif component_type == "pure_tension_tie":
            if any(w in prompt_lower for w in ["stiff", "rigidity", "stretch", "elongat", "deflection", "modulus", "solar sail", "spoke", "tonal pitch", "acoustic"]):
                ashby_key = AshbyIndex.TIE_STIFFNESS
                ashby_reasoning = "Pure tensile chord or cable requiring maximum axial stiffness per unit mass: M = E / ρ."
            else:
                ashby_key = AshbyIndex.TIE_STRENGTH
                ashby_reasoning = "Pure tensile chord or cable resisting yielding or plastic rupture: M = σ_y / ρ."
        elif component_type == "rotational_drive_element" or (component_type == "turbine_blade_or_impeller" and any(w in prompt_lower for w in ["rpm", "centrifugal", "centrifuge", "flywheel", "disk", "runner wheel", "inducer", "pelton", "bilge", "propeller", "shear dispersion", "dispersion rotor", "ring gear", "drill turbine"])):
            ashby_key = AshbyIndex.FLYWHEEL_INERTIA
            ashby_reasoning = "High-speed rotational machinery governed by centrifugal burst limits: M = σ_y / ρ."
        elif component_type in ["ballistic_armor_plate", "structural_plate_or_shell"]:
            if any(w in prompt_lower for w in ["vacuum barrier", "cranial", "cranioplasty", "brain shield", "shielding brain", "micrometeoroid", "puncture", "burst", "bursting", "shatter", "rupture", "camera cover", "window cover", "hydrostatic bursting"]):
                ashby_key = AshbyIndex.PLATE_STRENGTH
                ashby_reasoning = "Shell or plate resisting out-of-plane fracture, puncture, or hydrostatic bursting pressure: M = σ_y^(1/2) / ρ."
            elif any(w in prompt_lower for w in ["fender", "body panel", "display lid", "laptop lid", "stiffness", "rigidity", "deflection", "rigid", "stiff", "flexural rigidity", "baffle", "drop plate", "reflector", "fairing", "nose cone", "lid", "buffeting"]):
                ashby_key = AshbyIndex.PLATE_STIFFNESS
                ashby_reasoning = "Thin plate/shell requiring maximum flexural rigidity per unit mass: M = E^(1/3) / ρ."
            else:
                ashby_key = AshbyIndex.PLATE_STRENGTH
                ashby_reasoning = "Shell or plate resisting out-of-plane flexure, puncture, or hydrostatic bursting pressure: M = σ_y^(1/2) / ρ."
        elif component_type == "structural_hardware_or_pivot":
            ashby_key = AshbyIndex.BEAM_STRENGTH
            ashby_reasoning = "High mechanical shear and bending strength under concentrated pivot/mounting loads: M = σ_y^(2/3) / ρ."
        elif is_submerged and high_load_intent and component_type in ["turbine_blade_or_impeller", "turbomachine_blade"]:
            ashby_key = AshbyIndex.BEAM_STRENGTH
            ashby_reasoning = "Submerged hydro-turbine blade subject to cantilever hydrodynamic thrust bending load. Governed by failure strength before yielding per unit mass: M = σ_y^(2/3) / ρ."
        elif component_type in ["structural_furniture_or_load_frame", "structural_frame_or_chassis", "structural_cantilever_beam", "heavy_duty_lifting_or_crane"]:
            if any(w in prompt_lower for w in ["stiffness", "rigidity", "deflection", "rigid", "stiff", "flutter", "sag", "aerodynamic downforce", "downforce", "per unit weight", "wind gust", "wind gusts", "solar tracking", "solar array", "solar boom", "competition road bicycle", "bicycle front fork"]):
                ashby_key = AshbyIndex.BEAM_STIFFNESS
                ashby_reasoning = "Load-bearing beam resisting bending deflection: M = E^(1/2) / ρ."
            else:
                ashby_key = AshbyIndex.BEAM_STRENGTH
                ashby_reasoning = "Load-bearing beam resisting bending plastic collapse: M = σ_y^(2/3) / ρ."
        elif component_type == "automotive_aerodynamic_wing_or_spoiler":
            if any(w in prompt_lower for w in ["spar", "high downforce", "downforce wing", "race car wing", "gt3"]):
                ashby_key = AshbyIndex.BEAM_STIFFNESS
                ashby_reasoning = "Aerodynamic downforce wing spar requiring maximum flexural rigidity per unit mass to prevent aerodynamic stall: M = E^(1/2) / ρ."
            else:
                ashby_key = AshbyIndex.PLATE_STIFFNESS
                ashby_reasoning = "Automotive aerodynamic spoiler/panel requiring maximum flexural stiffness per unit mass to resist aerodynamic buffeting: M = E^(1/3) / ρ."
        elif component_type == "wind_turbine_blade":
            if any(w in prompt_lower for w in ["fatigue", "cyclical", "alternating", "million cycles"]):
                ashby_key = AshbyIndex.FATIGUE_EFFICIENCY
                ashby_reasoning = "Wind turbine aerofoil blade governed by high-cycle aerodynamic cyclic fatigue efficiency: M = σ_fatigue / ρ."
            else:
                ashby_key = AshbyIndex.BEAM_STIFFNESS
                ashby_reasoning = "Wind turbine aerofoil blade requiring high specific spar stiffness to prevent tip-to-tower strike under gusts: M = E^(1/2) / ρ."
        else:
            guide = derive_selection_guide(prompt_lower)
            ashby_key = guide["index_key"]
            ashby_reasoning = guide["reasoning"]

        # 7. Identify Unknowns & Ambiguities (Guardrail Protection)
        detected_ambiguities = []
        is_blade_or_hydro = is_submerged or component_type in ["turbine_blade_or_impeller", "turbomachine_blade"]
        
        if is_blade_or_hydro:
            if ("exact weight" not in prompt_lower and not target_yield_mpa) or any(w in prompt_lower for w in ["don't know", "unknown weight", "not know"]):
                detected_ambiguities.append(
                    "Exact hydrodynamic load magnitude is unquantified by user. Estimated via typical Kenyan river flow conditions (velocity u = 2.0 to 3.0 m/s, dynamic pressure q = 2.0 to 4.5 kPa)."
                )
            if not target_chord_mm:
                detected_ambiguities.append(
                    "Blade geometric chord length unstated. Assumed micro-hydro baseline: c = 180 mm, span L = 450 mm."
                )
        elif is_outdoor_uv:
            detected_ambiguities.append(
                "Outdoor structural component: Solar UV irradiance ~1000 W/m² and diurnal thermal cycling assumed."
            )
        elif component_type == "structural_frame_or_chassis":
            detected_ambiguities.append(
                "Rider weight and terrain shock spectrum unstated. Assumed standard 85 kg dynamic payload with 3.0x dynamic impact safety factor."
            )
        elif component_type == "thermal_management_heat_sink":
            detected_ambiguities.append(
                "Electronic heat flux and fan air velocity unquantified. Optimization targets maximum solid thermal conductivity (Fourier conduction) and fin surface efficiency."
            )
        elif component_type == "biomedical_device_or_implant":
            detected_ambiguities.append(
                "In vivo physiological environment assumed: saline interstitial fluid (pH ~7.4), zero toxicity, and low Young's modulus to prevent bone stress shielding."
            )
        elif component_type == "rotational_drive_element":
            detected_ambiguities.append(
                "Rotor RPM / operating angular velocity unquantified. Optimization focuses on maximum burst-limited kinetic energy density M = σ_y / ρ."
            )

        # 8. Compile Synthesized Engineering Specification
        from src.ashby_engine import INDEX_DESCRIPTIONS
        derived_formula = INDEX_DESCRIPTIONS.get(ashby_key, {}).get("formula", "E^(1/2) / ρ")

        has_cushion_word = bool(re.search(r'\b(?:phone case|bumper case|protective case|rubber|squishy|soft|shoe sole|bumper|cushion|pad|pads|peristaltic|mounting foot|recoil|foam liner)\b', prompt_lower)) and not any(w in prompt_lower for w in ["paddle", "payload", "electronics", "instrument", "housing", "avionics", "springboard", "diving board", "pole vault", "vaulting pole"])
        is_rigid_housing = any(w in prompt_lower for w in ["payload housing", "electronics housing", "instrument housing", "avionics", "weather balloon payload", "balloon payload"])
        is_cushion = (
            (component_type in ["wear_cushion_footwear", "flexible_elastomeric_component", "elastic_suspension_or_damping"] or
             (component_type == "protective_housing_or_case" and not is_rigid_housing and any(w in prompt_lower for w in ["phone", "bumper", "shock", "rubber", "drop"]))) or
            has_cushion_word
        ) and not is_rigid_housing and not any(w in prompt_lower for w in ["springboard", "diving board", "paddle", "pole vault"])
        is_cutting = component_type == "cutting_tool_or_blade" or is_cutting_tool or any(w in prompt_lower for w in ["knife", "machete", "chisel", "saw blade", "scalpel", "chopping", "planer", "granulator", "shear tooth", "scoring wheel", "scribe"]) or ("blade" in prompt_lower and "blender" in prompt_lower)
        is_food = (
            component_type in ["culinary_thermal_ware", "food_contact_utensil", "fluid_containment_vessel"] or
            is_cookware or
            any(w in prompt_lower for w in ["food", "drink", "kitchen", "edible", "blender", "pressure cooker", "dairy", "cheese", "poultry", "meat", "baby food", "puree", "washdown"]) or
            ("bottle" in prompt_lower and not any(w in prompt_lower for w in ["shredder", "granulator", "recycling", "scrap"]))
        ) and not (is_cutting and any(w in prompt_lower for w in ["shredder", "granulator", "recycling", "scrap", "dirt", "grit"]))
        is_rapid = component_type == "rapid_prototyping_or_toy" or any(w in prompt_lower for w in ["test a model", "cheap model", "toy", "prototype", "figurine"])
        is_optical = (component_type == "transparent_optical_component" or any(w in prompt_lower for w in ["clear like glass", "transparent", "see-through", "viewport", "visor", "dome cover", "window cover", "face shield", "spectacle", "goggles"])) and not is_cutting
        is_biomed = component_type == "biomedical_device_or_implant" or is_dental or is_spinal or any(w in prompt_lower for w in ["implant", "biocompatible", "biomedical", "femoral", "in vivo", "human body", "prosthetic", "bone replacement", "hip replacement", "orthopedic", "spinal", "spine", "dental", "molar crown", "scalpel", "surgical", "microsurgery", "tissue toxicity", "catheter", "tumor", "hyperthermia", "cranioplasty", "cranial", "medical", "clinical"])

        return {
            "raw_prompt": prompt_clean,
            "synthesized_engineering_spec": {
                "component_classification": component_type,
                "primary_governing_ashby_index": ashby_key,
                "ashby_mathematical_formula": derived_formula,
                "ashby_selection_rationale": ashby_reasoning,
                "functional_objective": "Minimize component mass while satisfying mechanical stiffness, failure strength, and environmental longevity constraints."
            },
            "boundary_conditions_and_constraints": {
                "submerged_aquatic_exposure": is_submerged,
                "hydrolysis_resistance_required": is_submerged,
                "water_saturation_penalty_active": is_submerged,  # Disqualifies PLA
                "outdoor_uv_exposure": is_outdoor_uv,
                "chemical_or_saline_exposure": is_chem_exposure,
                "strong_acid_exposure": is_strong_acid,
                "marine_industrial_exposure": is_marine_industrial,
                "heavy_infrastructure": is_heavy_infrastructure,
                "spinal_cage": is_spinal,
                "dental_prosthetic": is_dental,
                "low_friction_dry_gear": is_gear_dry,
                "ballistic_armor": is_ballistic,
                "dewar_support_strut": is_dewar_strut,
                "brake_caliper_bridge": is_brake_caliper,
                "is_lox": is_lox,
                "pressure_vessel_certified": is_pressure_vessel_certified,
                "spoke_wire": is_spoke_wire,
                "balloon_tether": is_balloon_tether,
                "battery_shield": is_battery_shield,
                "speaker_cone": is_speaker_cone,
                "machine_spindle": is_machine_spindle,
                "high_temperature_threshold": is_high_temp,
                "is_cryogenic": is_cryogenic,
                "high_bending_strength_required": high_load_intent,
                "cyclical_fatigue_resistance_required": cyclical_fatigue_intent,
                "weight_minimization_priority": lightweight_intent,
                "cost_sensitivity": low_cost_intent or is_rapid or is_heavy_infrastructure,
                "manufacturing_process": mfg_process_label,
                "fdm_only_preference": fdm_only_preference,
                "specified_candidate_materials": specified_materials,
                "flexible_cushion_required": is_cushion,
                "food_contact_safe": is_food,
                "rapid_prototyping_priority": is_rapid,
                "optical_transparency_required": is_optical,
                "cutting_edge_hardness_required": is_cutting,
                "biocompatible_implant_required": is_biomed,
                "hardened_steel_nozzle_acceptable": True,
                "post_processing_surface_treatment": "Mandatory UV-curable/Epoxy smoothing to mitigate 40% FDM layer-line hydrodynamic drag penalty" if is_submerged else "Standard deburring / coating"
            },
            "numerical_parameters": {
                "estimated_flow_velocity_ms": target_velocity_ms or 2.4,
                "estimated_chord_m": (target_chord_mm / 1000.0) if target_chord_mm else 0.18,
                "target_yield_strength_min_mpa": target_yield_mpa or (45.0 if high_load_intent else 30.0),
                "target_service_temperature_c": target_temp_c
            },
            "guardrail_flags": {
                "has_ambiguity": len(detected_ambiguities) > 0,
                "ambiguities_noted": detected_ambiguities,
                "hallucination_safeguards": [
                    "Reject PLA for continuous aquatic submersion due to empirical 28.4% tensile strength loss and high fatigue creep.",
                    "Verify fiber reinforcement nozzle requirements: PETG-CF requires hardened steel / tungsten nozzle (0.4-0.6mm) to prevent brass bore enlargement.",
                    "Enforce hydraulic boundary layer smoothing directives (XTC-3D epoxy sealant) to prevent up to 40% lift-to-drag degradation."
                ]
            }
        }

    @staticmethod
    def _extract_regex_float(text: str, pattern: str) -> Optional[float]:
        """Utility to safely extract floating point values from regex matches."""
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                return None
        return None
