import os
import json
import urllib.request
from typing import Optional

def ollama_semantic_classifier(prompt: str) -> Optional[str]:
    """
    Uses the local Ollama LLM to semantically classify the user's prompt 
    into our strict Ashby engineering categories without relying on hardcoded regex.
    Configured with low-latency constraints (num_predict: 20, 3s timeout).
    """
    categories = [
        "aerospace_airframe_or_drone",
        "automotive_aerodynamic_wing_or_spoiler",
        "automotive_impact_component",
        "ballistic_armor_plate",
        "biomedical_device_or_implant",
        "culinary_thermal_ware",
        "cutting_tool_or_blade",
        "elastic_suspension_or_damping",
        "flexible_elastomeric_component",
        "fluid_conduit_plumbing",
        "fluid_containment_vessel",
        "food_contact_utensil",
        "generic_mechanical_component",
        "heavy_duty_lifting_or_crane",
        "high_temperature_thermal_barrier",
        "low_friction_gear_or_bushing",
        "marine_vessel_or_hull",
        "outdoor_architectural_structure",
        "pressure_vessel_or_containment",
        "protective_housing_or_case",
        "pure_tension_tie",
        "rapid_prototyping_or_toy",
        "rotational_drive_element",
        "structural_cantilever_beam",
        "structural_frame_or_chassis",
        "structural_furniture_or_load_frame",
        "structural_hardware_or_pivot",
        "structural_plate_or_shell",
        "thermal_insulation_barrier",
        "thermal_management_heat_sink",
        "transparent_optical_component",
        "turbine_blade_or_impeller",
        "wear_cushion_footwear",
        "wind_turbine_blade",
    ]
    
    system_prompt = f"""You are a strict text classification router. 
Classify the user's mechanical engineering part into EXACTLY ONE of the following categories:
{', '.join(categories)}

If it's a mouse panel, drone body, or laptop case, it is a structural_plate_or_shell.
If it holds high pressure air or gas (like a scuba tank), it is a pressure_vessel_or_containment.
If you are unsure, default to generic_mechanical_component.

Respond with ONLY the exact string of the category. Do not add any other words or punctuation."""

    try:
        model_name = os.getenv("LOCAL_MODEL_NAME", "llama3.2")
        req_data = json.dumps({
            "model": model_name,
            "prompt": f"User part: {prompt}",
            "system": system_prompt,
            "stream": False,
            "keep_alive": "15m",
            "options": {
                "num_predict": 20,
                "temperature": 0.0,
                "num_ctx": 512,
                "num_thread": 4
            }
        }).encode("utf-8")
        
        base_url = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
        req = urllib.request.Request(
            f"{base_url}/api/generate",
            data=req_data,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=3.0) as response:
            result = json.loads(response.read().decode("utf-8"))
            answer = result.get("response", "").strip()
            
            # Validate output is strictly in our list
            for cat in categories:
                if cat in answer:
                    return cat
        return None
    except Exception:
        return None
