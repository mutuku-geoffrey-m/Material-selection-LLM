"""Language understanding with the local model.

The local model (Ollama) reads the design brief and returns a schema-constrained JSON object describing the
component, the governing load case, the service temperature and pressure, the environment and any family
restriction. Every field is validated against a closed vocabulary and, for numbers, against the text of the
brief before it is used; the rule-based parser remains the fallback and the physics screening remains
deterministic. The provenance of the interpretation is recorded in ``spec["understanding"]``.
"""
import json
import os
import re
import time
import urllib.request
from typing import Any, Dict, List, Optional

from src.ashby_engine import AshbyIndex, INDEX_DESCRIPTIONS
from src.compatibility import FAMILY_LABELS
from src.nlp_parser import NLPTranslationLayer

DEFAULT_MODEL = "llama3.2:3b"

COMPONENT_CLASSES: List[str] = [
    "aerospace_airframe_or_drone", "automotive_aerodynamic_wing_or_spoiler", "automotive_impact_component",
    "ballistic_armor_plate", "biomedical_device_or_implant", "culinary_thermal_ware", "cutting_tool_or_blade",
    "elastic_suspension_or_damping", "flexible_elastomeric_component", "fluid_conduit_plumbing",
    "fluid_containment_vessel", "food_contact_utensil", "heavy_duty_lifting_or_crane",
    "heavy_impact_crushing_or_abrasion_jaw", "high_temperature_thermal_barrier", "low_friction_gear_or_bushing",
    "marine_vessel_or_hull", "outdoor_architectural_structure", "pressure_vessel_or_containment",
    "protective_housing_or_case", "pure_tension_tie", "rapid_prototyping_or_toy", "rotational_drive_element",
    "structural_cantilever_beam", "structural_frame_or_chassis", "structural_furniture_or_load_frame",
    "structural_hardware_or_pivot", "structural_plate_or_shell", "thermal_insulation_barrier",
    "thermal_management_heat_sink", "transparent_optical_component", "turbine_blade_or_impeller",
    "wear_cushion_footwear", "wind_turbine_blade", "generic_mechanical_component",
]
INDEX_VALUES: List[str] = [v for k, v in vars(AshbyIndex).items() if not k.startswith("_") and isinstance(v, str)]
FAMILY_VALUES: List[str] = list(FAMILY_LABELS.keys())
ENVIRONMENT_VALUES = ["submerged_water", "marine_saltwater", "outdoor_uv", "cryogenic", "chemical_exposure", "food_contact"]

SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "component_class": {"type": "string", "enum": COMPONENT_CLASSES},
        "governing_index": {"type": "string", "enum": INDEX_VALUES},
        "service_temperature_c": {"type": "number"},
        "pressure_atm": {"type": "number"},
        "requested_material_family": {"type": "string", "enum": FAMILY_VALUES + ["none"]},
        "environment": {"type": "array", "items": {"type": "string", "enum": ENVIRONMENT_VALUES}},
        "chemical_media": {"type": "array", "items": {"type": "string"}},
        "rationale": {"type": "string"},
    },
    "required": ["component_class", "governing_index", "service_temperature_c", "pressure_atm",
                 "requested_material_family", "environment", "chemical_media", "rationale"],
}

_INSTRUCTIONS = """You extract engineering requirements from a design brief. Reply with one JSON object only.
Fields: component_class, governing_index, service_temperature_c (highest continuous temperature in degrees Celsius, or -999 if not stated),
pressure_atm (or -999 if not stated), requested_material_family (only when the brief asks which grade or alloy of a named material family, else \"none\"),
environment (list), chemical_media (fluids that touch the part), rationale (one short sentence).
governing_index: beam_stiffness = lightest part limited by bending deflection; beam_strength = limited by bending failure;
plate_stiffness / plate_strength = panels and shells; tie_strength / tie_stiffness = tensile members; shaft_torsion = twisting shafts;
flywheel_inertia = rotating parts limited by centrifugal burst; elastic_energy = springs and snap fits; thermal_conductivity = heat exchangers
and heat sinks; thermal_insulation = linings and insulation; fatigue_efficiency = cyclic loading; cost_normalized_tie = cheapest tension member.
Example brief: "Heat exchanger tube carrying seawater at 90 C".
Example answer: {"component_class":"thermal_management_heat_sink","governing_index":"thermal_conductivity","service_temperature_c":90,"pressure_atm":-999,"requested_material_family":"none","environment":["marine_saltwater"],"chemical_media":["seawater"],"rationale":"Heat transfer through a tube wall in a saline fluid."}
Example brief: "Which steel grade for a 40 mm drive shaft transmitting 500 Nm?"
Example answer: {"component_class":"rotational_drive_element","governing_index":"shaft_torsion","service_temperature_c":-999,"pressure_atm":-999,"requested_material_family":"steel","environment":[],"chemical_media":[],"rationale":"A shaft limited by torsional stiffness, restricted to steel grades."}
"""


def _base_url() -> str:
    return os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")


def model_status(base_url: Optional[str] = None, model: Optional[str] = None) -> Dict[str, Any]:
    """Report whether the Ollama daemon is reachable and whether the configured model is installed."""
    base_url = (base_url or _base_url()).rstrip("/")
    model = model or os.getenv("LOCAL_MODEL", DEFAULT_MODEL)
    status = {"daemon": False, "installed": False, "model": model, "installed_models": []}
    try:
        with urllib.request.urlopen(urllib.request.Request(base_url + "/api/tags"), timeout=3) as resp:
            tags = json.loads(resp.read().decode("utf-8")).get("models", [])
        status["daemon"] = True
        names = [m.get("name", "") for m in tags]
        status["installed_models"] = names
        wanted = model if ":" in model else model + ":latest"
        status["installed"] = wanted in names
    except Exception:
        pass
    return status


def _digits_in(prompt: str) -> set:
    return set(re.findall(r"\d+(?:\.\d+)?", prompt.replace(",", "")))


def _grounded_number(value: Any, prompt: str, lower: float, upper: float) -> Optional[float]:
    """Accept a numeric answer only when it lies in a physical range and is traceable to the brief."""
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if not lower <= number <= upper:
        return None
    candidates = {f"{number:g}", f"{abs(number):g}", str(int(round(abs(number))))}
    if number >= 0:  # a temperature may be stated in kelvin or Fahrenheit
        candidates |= {str(int(round(number + 273.15))), str(int(round(number * 9 / 5 + 32)))}
    return number if candidates & _digits_in(prompt) else None


def validate_hints(raw: Dict[str, Any], prompt: str) -> Dict[str, Any]:
    hints: Dict[str, Any] = {}
    if raw.get("component_class") in COMPONENT_CLASSES:
        hints["component_class"] = raw["component_class"]
    if raw.get("governing_index") in INDEX_VALUES:
        hints["governing_index"] = raw["governing_index"]
    temperature = _grounded_number(raw.get("service_temperature_c"), prompt, -273.0, 3500.0)
    if temperature is not None:
        hints["service_temperature_c"] = temperature
    pressure = _grounded_number(raw.get("pressure_atm"), prompt, 0.0, 5000.0)
    if pressure is not None:
        hints["pressure_atm"] = pressure
    if raw.get("requested_material_family") in FAMILY_VALUES:
        hints["requested_material_family"] = raw["requested_material_family"]
    hints["environment"] = [e for e in (raw.get("environment") or []) if e in ENVIRONMENT_VALUES]
    hints["chemical_media"] = [str(m)[:40] for m in (raw.get("chemical_media") or [])][:4]
    hints["rationale"] = str(raw.get("rationale", ""))[:240]
    return hints


def extract_hints(prompt: str, base_url: Optional[str] = None, model: Optional[str] = None,
                  timeout_s: Optional[float] = None) -> Dict[str, Any]:
    """Ask the local model to read the brief. Returns ``{"hints": dict | None, "error": str | None, "latency_s": float}``."""
    base_url = (base_url or _base_url()).rstrip("/")
    model = model or os.getenv("LOCAL_MODEL", DEFAULT_MODEL)
    timeout_s = timeout_s or float(os.getenv("EMS_UNDERSTANDING_TIMEOUT_S", "120"))
    payload = {
        "model": model,
        "prompt": f"{_INSTRUCTIONS}\nBrief: \"{prompt.strip()}\"\nAnswer:",
        "stream": False,
        "format": SCHEMA,
        "keep_alive": "30m",
        "options": {"temperature": 0, "num_predict": 220, "num_ctx": 2048, "num_thread": 4},
    }
    started = time.time()
    last_error = "no response"
    for response_format in (SCHEMA, "json"):  # schema-constrained decoding first, then loose JSON mode
        payload["format"] = response_format
        try:
            request = urllib.request.Request(base_url + "/api/generate", data=json.dumps(payload).encode("utf-8"),
                                             headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(request, timeout=timeout_s) as resp:
                body = json.loads(resp.read().decode("utf-8"))
            text = (body.get("response") or "").strip()
            start, end = text.find("{"), text.rfind("}")
            if start < 0 or end <= start:
                raise ValueError(f"no JSON object in model output: {text[:60]!r}")
            raw = json.loads(text[start:end + 1])
            return {"hints": validate_hints(raw, prompt), "error": None, "latency_s": time.time() - started}
        except Exception as exc:
            code = getattr(exc, "code", None)
            if code == 404:
                return {"hints": None, "error": f"model '{model}' is not installed (run: ollama pull {model})",
                        "latency_s": time.time() - started}
            last_error = f"{type(exc).__name__}: {str(exc)[:100]}"
    return {"hints": None, "error": last_error, "latency_s": time.time() - started}


def apply_hints(spec: Dict[str, Any], hints: Dict[str, Any], prompt: str) -> List[str]:
    """Merge validated model output into the rule-based specification. Returns notes describing what changed."""
    notes: List[str] = []
    synth = spec["synthesized_engineering_spec"]
    boundary = spec["boundary_conditions_and_constraints"]
    numerical = spec.setdefault("numerical_parameters", {})

    rule_class = synth.get("component_classification")
    if rule_class == "generic_mechanical_component" and hints.get("governing_index"):
        index = hints["governing_index"]
        info = INDEX_DESCRIPTIONS.get(index, {})
        synth["primary_governing_ashby_index"] = index
        synth["ashby_mathematical_formula"] = info.get("formula", synth.get("ashby_mathematical_formula"))
        synth["ashby_selection_rationale"] = hints.get("rationale") or "Governing index taken from the language-model reading of the brief."
        if hints.get("component_class") and hints["component_class"] != "generic_mechanical_component":
            synth["component_classification"] = hints["component_class"]
        notes.append(f"The rule-based parser could not classify the brief; the language model assigned '{index}'.")
    elif hints.get("governing_index") and hints["governing_index"] != synth.get("primary_governing_ashby_index"):
        notes.append(f"The language model suggested '{hints['governing_index']}'; the rule-based classification "
                     f"'{synth.get('primary_governing_ashby_index')}' was retained.")

    if numerical.get("target_service_temperature_c") is None and "service_temperature_c" in hints:
        numerical["target_service_temperature_c"] = hints["service_temperature_c"]
        notes.append(f"Service temperature {hints['service_temperature_c']:g} °C was read from the brief by the language model.")
    if numerical.get("target_pressure_atm") is None and "pressure_atm" in hints:
        numerical["target_pressure_atm"] = hints["pressure_atm"]

    if not boundary.get("requested_material_family") and hints.get("requested_material_family"):
        boundary["requested_material_family"] = hints["requested_material_family"]
        notes.append(f"Candidates were restricted to the {FAMILY_LABELS[hints['requested_material_family']]} family requested in the brief.")

    flags = {"submerged_water": "submerged_aquatic_exposure", "marine_saltwater": "marine_industrial_exposure",
             "outdoor_uv": "outdoor_uv_exposure", "cryogenic": "is_cryogenic", "chemical_exposure": "chemical_or_saline_exposure",
             "food_contact": "food_contact_safe"}
    molten = any(w in prompt.lower() for w in ("molten", "melt", "crucible", "furnace", "smelt", "foundry", "slag"))
    for env in hints.get("environment", []):
        if molten and env in ("submerged_water", "marine_saltwater"):
            continue
        boundary[flags[env]] = True
    if "marine_saltwater" in hints.get("environment", []):
        boundary["chemical_or_saline_exposure"] = True
    if hints.get("chemical_media"):
        existing = boundary.setdefault("chemical_media", [])
        existing.extend(m for m in hints["chemical_media"] if m not in existing)
    return notes


def understand(prompt: str, use_llm: bool = True, base_url: Optional[str] = None,
               model: Optional[str] = None) -> Dict[str, Any]:
    """Interpret a design brief: local model first, rule-based parser as validator and fallback."""
    spec = NLPTranslationLayer.parse_engineering_prompt(prompt)
    model = model or os.getenv("LOCAL_MODEL", DEFAULT_MODEL)
    understanding: Dict[str, Any] = {"source": "Rule-based parser", "model": None, "latency_s": 0.0, "notes": [], "hints": None}
    if use_llm:
        result = extract_hints(prompt, base_url, model)
        understanding["latency_s"] = round(result["latency_s"], 2)
        if result["hints"] is not None:
            understanding.update(source=f"Local language model ({model}) with rule-based validation", model=model,
                                 hints=result["hints"])
            understanding["notes"] = apply_hints(spec, result["hints"], prompt)
            # Chemical-media and family rules may now apply to terms contributed by the model.
            NLPTranslationLayer.refresh_compatibility(spec, prompt)
        else:
            understanding["notes"] = [f"The language model could not be used ({result['error']}); the rule-based parser was applied."]
    spec["understanding"] = understanding
    return spec
