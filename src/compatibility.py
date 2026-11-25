"""Material-family membership, chemical-compatibility screening and advisory notes."""
import re
from typing import Dict, Iterable, List, Optional, Tuple

from src.materials_db import MATERIALS_DATABASE

FAMILY_LABELS = {
    "aluminium": "aluminium",
    "steel": "carbon and alloy steel",
    "stainless_steel": "stainless steel",
    "titanium": "titanium",
    "copper": "copper and brass",
    "magnesium": "magnesium",
    "nickel_alloy": "nickel alloy",
    "cast_iron": "cast iron",
    "polymer": "polymer",
    "composite": "composite",
    "ceramic": "ceramic",
}

_ALUMINIUM = re.compile(r"alumin(?:i)?um")


def _in_family(record: Dict, family: str) -> bool:
    name = str(record.get("name", "")).lower()
    fam = str(record.get("family", ""))
    fam_lc = fam.lower()
    if family == "aluminium":
        return fam == "Aluminum Alloy" or bool(_ALUMINIUM.search(name))
    if family == "stainless_steel":
        return "stainless" in fam_lc or "stainless" in name
    if family == "steel":
        return ("steel" in fam_lc or "steel" in name) and "stainless" not in fam_lc and "stainless" not in name
    if family == "titanium":
        return "titanium" in fam_lc or "titanium" in name or "ti-6al" in name
    if family == "copper":
        return "copper" in fam_lc or any(w in name for w in ("copper", "brass", "bronze"))
    if family == "magnesium":
        return "magnesium" in fam_lc or "magnesium" in name
    if family == "nickel_alloy":
        return "nickel" in fam_lc or any(w in name for w in ("inconel", "hastelloy", "monel", "nickel"))
    if family == "cast_iron":
        return "iron" in fam_lc and "cast" in fam_lc
    if family == "polymer":
        return any(w in fam_lc for w in ("polymer", "thermoplastic", "elastomer", "polyamide"))
    if family == "composite":
        return "composite" in fam_lc
    if family == "ceramic":
        return "ceramic" in fam_lc
    return False


def family_member_keys(family: str) -> List[str]:
    """Catalogue keys of every material belonging to the named family."""
    return [k for k, rec in MATERIALS_DATABASE.items() if _in_family(rec, family)]


def belongs_to_family(entry: Dict, family: str) -> bool:
    record = MATERIALS_DATABASE.get(entry.get("key"), entry)
    return _in_family(record, family)


_FAMILY_WORDS = {
    "aluminium": r"alumin(?:i)?um", "stainless_steel": r"stainless(?:\s+steel)?", "steel": r"steel",
    "titanium": r"titanium", "copper": r"copper|brass|bronze", "magnesium": r"magnesium",
    "nickel_alloy": r"nickel(?:\s+alloy)?|inconel|hastelloy", "cast_iron": r"cast\s+iron",
}


def detect_requested_family(prompt: str) -> Optional[str]:
    """Detect briefs that ask for a grade or alloy within a named family ("which aluminium alloy ...")."""
    text = (prompt or "").lower()
    for fam, words in _FAMILY_WORDS.items():
        patterns = (
            rf"\b(?:which|what)\s+(?:\w+\s+)?(?:grade|alloy|type|series|temper)s?\s+of\s+(?:{words})\b",
            rf"\b(?:which|what)\s+(?:{words})\s+(?:alloy|grade|type|series)\b",
            rf"\b(?:recommend|select|choose|suggest|pick|specify)\s+(?:an?\s+|the\s+)?(?:{words})\s+(?:alloy|grade)\b",
            rf"\b(?:{words})\s+(?:alloy|grade)\s+(?:is|would be|should be)\s+(?:best|better|suitable|appropriate)\b",
            rf"\bwhat\s+grade\s+of\s+(?:{words})\b",
        )
        if any(re.search(p, text) for p in patterns):
            return fam
    return None


# Chemical media that rapidly degrade particular families.
_MEDIA_RULES: Tuple[Tuple[Tuple[str, ...], Tuple[str, ...], str], ...] = (
    (("gallium", "galinstan"), ("aluminium", "copper", "magnesium"),
     "Liquid gallium penetrates aluminium grain boundaries (liquid-metal embrittlement) and alloys rapidly with copper "
     "and magnesium; aluminium, copper and magnesium grades were therefore excluded."),
    (("mercury",), ("aluminium", "copper"),
     "Mercury amalgamates with aluminium and copper alloys; these families were therefore excluded."),
)


def media_exclusions(prompt: str, media: Iterable[str] = ()) -> Tuple[List[str], List[str]]:
    """Return (families to exclude, explanatory notes) for the fluids named in the brief."""
    text = (prompt or "").lower() + " " + " ".join(str(m).lower() for m in media)
    families: List[str] = []
    notes: List[str] = []
    for keywords, excluded, note in _MEDIA_RULES:
        if any(k in text for k in keywords):
            for fam in excluded:
                if fam not in families:
                    families.append(fam)
            notes.append(note)
    return families, notes


def galvanic_advisory(prompt: str, requested_family: Optional[str]) -> Optional[str]:
    text = (prompt or "").lower()
    carbon = any(w in text for w in ("cfrp", "carbon fiber", "carbon fibre", "carbon-fiber", "carbon-fibre"))
    aluminium = bool(_ALUMINIUM.search(text)) or requested_family == "aluminium"
    marine = any(w in text for w in ("marine", "seawater", "salt", "coastal", "offshore"))
    if carbon and aluminium and marine:
        return ("Carbon fibre is strongly cathodic to aluminium, so a marine electrolyte drives galvanic corrosion of the "
                "aluminium at the joint. Isolate the interface with a glass-fibre ply or sealant, use isolating washers and "
                "sleeves under the fasteners, and prefer corrosion-resistant 5xxx or 6xxx grades.")
    return None


_HIGH_STRENGTH_SERIES = re.compile(r"(?:alloy|alclad)\s+(?:20)?[27]\d{3}\b")


_NEGATION = r"(?:no|not|without|free of|free from|never|zero)"


def negated_exposure(prompt: str) -> set:
    """Exposure categories the brief explicitly rules out (for example "no seawater exposure")."""
    text = (prompt or "").lower()
    ruled_out = set()
    if re.search(rf"\b{_NEGATION}\s+(?:\w+\s+){{0,3}}?(?:seawater|sea water|salt water|saltwater|marine|saline|coastal|brackish|submerg\w*)", text):
        ruled_out.add("marine")
    if re.search(rf"\b{_NEGATION}\s+(?:\w+\s+){{0,3}}?(?:uv|sunlight|solar|outdoor)", text):
        ruled_out.add("uv")
    return ruled_out


def parse_requirements(prompt: str) -> Dict[str, Optional[float]]:
    """Numerical requirements stated in the brief: cost limit (USD/kg), delivery limit (days) and batch size (kg)."""
    text = (prompt or "").lower().replace(",", "")
    cost = re.search(r"(?:under|below|less than|no more than|at most|maximum of|max\.?)\s*\$?\s*(\d+(?:\.\d+)?)\s*(?:dollars?|usd|us\$|\$)?\s*(?:per|/|a|each)\s*(?:kg|kilogram)", text)
    days = re.search(r"(?:within|in|inside|under|by)\s*(\d+)\s*(?:working\s*)?days?", text)
    batch = re.search(r"(\d+(?:\.\d+)?)\s*kg\s*(?:prototype\s*)?(?:batch|order|lot|quantity|run)|(?:batch|order|lot|quantity)\s*of\s*(\d+(?:\.\d+)?)\s*kg", text)
    return {"max_cost_usd_kg": float(cost.group(1)) if cost else None,
            "max_lead_days": float(days.group(1)) if days else None,
            "batch_kg": float(next(g for g in batch.groups() if g)) if batch else None}


_CONVENTIONAL_MACHINING = re.compile(r"\b(?:cnc|milling|turning|drilling|conventional machining|lathe)\b")


def commentary_contradicts_directive(commentary: str, record: Dict) -> bool:
    """A sintered ceramic is finished by diamond grinding; advice to mill, turn or drill it contradicts the fabrication directive."""
    family = str(record.get("family", "")).lower()
    text = (commentary or "").lower()
    return "ceramic" in family and bool(_CONVENTIONAL_MACHINING.search(text)) and "diamond" not in text


def marine_service(prompt: str) -> bool:
    if "marine" in negated_exposure(prompt):
        return False
    text = (prompt or "").lower()
    return any(w in text for w in ("marine", "seawater", "sea water", "saltwater", "salt water", "coastal", "offshore", "brackish"))


def is_high_strength_aluminium_series(entry: Dict) -> bool:
    """2xxx and 7xxx aluminium grades are prone to exfoliation and stress-corrosion cracking in seawater."""
    return bool(_HIGH_STRENGTH_SERIES.search(str(entry.get("name", "")).lower()))


# Continuous service limits (degrees Celsius) applied when a catalogue record gives no explicit limit.
_FAMILY_SERVICE_LIMIT_C = (
    ("nickel_alloy", 700.0), ("titanium", 450.0), ("stainless_steel", 600.0), ("cast_iron", 400.0),
    ("steel", 450.0), ("copper", 350.0), ("aluminium", 180.0), ("magnesium", 150.0),
)


def service_limit_c(record: Dict) -> float:
    """Maximum continuous service temperature: catalogue value, else a family default, else the heat-deflection
    temperature, else 350 degrees Celsius."""
    explicit = record.get("max_service_temp_c")
    if explicit:
        return float(explicit)
    for family, limit in _FAMILY_SERVICE_LIMIT_C:
        if _in_family(record, family):
            return limit
    return float(record.get("heat_deflection_temp") or 350.0)


# ---------------------------------------------------------------------------------------------------------------------
# Molten media: melting point, families that are attacked, and families normally used for handling the melt.
# Entries are general engineering guidance and should be confirmed against supplier and handbook data.
# ---------------------------------------------------------------------------------------------------------------------
_REACTIVE_WITH_NOBLE_MELTS = ("aluminium", "magnesium", "copper", "nickel_alloy", "titanium", "polymer", "composite")
MELTS: Dict[str, Dict] = {
    "gold": {"mp": 1064.0, "unsuitable": _REACTIVE_WITH_NOBLE_MELTS, "preferred": ("ceramic",),
             "note": "Molten gold alloys with nickel, copper, aluminium and magnesium; refractory ceramics are the usual choice for stirrers and vessels."},
    "silver": {"mp": 962.0, "unsuitable": _REACTIVE_WITH_NOBLE_MELTS, "preferred": ("ceramic",),
               "note": "Molten silver dissolves oxygen and alloys with copper and nickel; refractory ceramics are the usual choice."},
    "platinum": {"mp": 1768.0, "unsuitable": _REACTIVE_WITH_NOBLE_MELTS + ("steel", "stainless_steel", "cast_iron"), "preferred": ("ceramic",),
                 "note": "Molten platinum exceeds the service limit of all common metals; only refractory ceramics are suitable."},
    "copper": {"mp": 1085.0, "unsuitable": ("aluminium", "magnesium", "copper", "polymer", "composite"), "preferred": ("ceramic",),
               "note": "Molten copper attacks aluminium and magnesium and oxidises uncoated ferrous parts; refractory ceramics are preferred."},
    "brass": {"mp": 930.0, "unsuitable": ("aluminium", "magnesium", "polymer", "composite"), "preferred": ("ceramic",),
              "note": "Molten brass loses zinc by volatilisation and attacks aluminium and magnesium; refractory ceramics are preferred."},
    "bronze": {"mp": 950.0, "unsuitable": ("aluminium", "magnesium", "polymer", "composite"), "preferred": ("ceramic",),
               "note": "Molten bronze attacks aluminium and magnesium; refractory ceramics are preferred."},
    "aluminium": {"mp": 660.0, "unsuitable": ("aluminium", "copper", "magnesium", "nickel_alloy", "steel", "stainless_steel",
                                              "titanium", "cast_iron", "polymer", "composite"), "preferred": ("ceramic",),
                  "note": "Molten aluminium dissolves iron, nickel and copper and wets most metals; non-wetting refractory ceramics are preferred."},
    "zinc": {"mp": 420.0, "unsuitable": ("aluminium", "copper", "magnesium", "polymer", "composite"),
             "preferred": ("steel", "stainless_steel", "cast_iron", "ceramic"),
             "note": "Molten zinc attacks aluminium and copper alloys; low-carbon steel, cast iron, stainless steel and ceramics are used."},
    "lead": {"mp": 327.0, "unsuitable": ("aluminium", "copper", "magnesium", "polymer", "composite"),
             "preferred": ("steel", "stainless_steel", "cast_iron", "ceramic"),
             "note": "Molten lead attacks aluminium, copper and magnesium; steels, cast iron and ceramics are used."},
    "tin": {"mp": 232.0, "unsuitable": ("aluminium", "copper", "magnesium", "polymer", "composite"),
            "preferred": ("stainless_steel", "steel", "cast_iron", "ceramic"),
            "note": "Molten tin alloys with copper and attacks aluminium; stainless steel, steel, cast iron and ceramics are used."},
    "magnesium": {"mp": 650.0, "unsuitable": ("aluminium", "copper", "nickel_alloy", "titanium", "polymer", "composite"),
                  "preferred": ("steel", "cast_iron", "ceramic"),
                  "note": "Molten magnesium attacks aluminium, copper, nickel and titanium; low-carbon steel and ceramics are used."},
    "glass": {"mp": 1400.0, "unsuitable": ("aluminium", "magnesium", "copper", "steel", "stainless_steel", "cast_iron", "titanium",
                                           "polymer", "composite"), "preferred": ("ceramic",),
              "note": "Molten glass attacks and oxidises most metals at working temperature; refractory ceramics are preferred."},
    "steel": {"mp": 1538.0, "unsuitable": ("aluminium", "magnesium", "copper", "nickel_alloy", "steel", "stainless_steel", "cast_iron",
                                           "titanium", "polymer", "composite"), "preferred": ("ceramic",),
              "note": "Molten steel exceeds the service limit of all common metals; only refractory ceramics are suitable."},
}
_MELT_NAMES = {"gold": "gold", "silver": "silver", "platinum": "platinum", "copper": "copper", "brass": "brass", "bronze": "bronze",
               "aluminium": "aluminium", "aluminum": "aluminium", "zinc": "zinc", "lead": "lead", "tin": "tin",
               "magnesium": "magnesium", "glass": "glass", "steel": "steel", "iron": "steel"}
_MELT_WORDS = "|".join(sorted(_MELT_NAMES, key=len, reverse=True))
_STIRRER_WORDS = ("stir", "agitat", "propeller", "impeller", "paddle", "rake", "mixer", "mixing rod", "stirrer", "rabble")


def detect_melt(prompt: str) -> Optional[str]:
    """Return the melt named in the brief (for example "gold" in "propeller to stir molten gold"), else None."""
    text = (prompt or "").lower()
    patterns = (
        rf"\b(?:molten|liquid|melted|melting|melt of|bath of|pool of)\s+(?:\w+\s+){{0,2}}?({_MELT_WORDS})\b",
        rf"\b({_MELT_WORDS})\s+(?:melt|melts|bath|baths|melting|crucible|furnace|foundry)\b",
    )
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return _MELT_NAMES[match.group(1)]
    return None


def is_stirring_duty(prompt: str) -> bool:
    text = (prompt or "").lower()
    return any(w in text for w in _STIRRER_WORDS)


def melt_assumptions(melt: str, stated_temperature_c: Optional[float]) -> Tuple[Optional[float], List[str]]:
    """Return the service temperature to use and explanatory notes, checking the stated value against the melting point."""
    info = MELTS[melt]
    mp = info["mp"]
    notes = [info["note"]]
    if stated_temperature_c is None:
        temperature = mp + 50.0
        notes.append(f"No temperature was stated; the bath was assumed to be {temperature:g} °C (melting point of {melt}, {mp:g} °C, plus 50 °C superheat).")
    elif stated_temperature_c < mp - 5.0:
        temperature = mp
        notes.append(f"The stated temperature ({stated_temperature_c:g} °C) is below the melting point of {melt} ({mp:g} °C), so the {melt} would be solid. "
                     f"The analysis assumes a molten bath at {mp:g} °C; state a temperature above {mp:g} °C if a hotter melt is intended.")
    else:
        temperature = stated_temperature_c
    return temperature, notes


_SCC_TEMPER = re.compile(r"(?:alloy|alclad)\s+(?:20)?[27]\d{3}-t6(?:51|511|2)?\b")
_SAFETY_CRITICAL_WORDS = ("suspension", "wishbone", "control arm", "steering", "brake", "chassis", "roll cage", "crane", "hoist",
                          "lifting", "rigging", "landing gear", "pushrod", "push rod", "racing", "aircraft", "aerospace", "cryogenic", "dewar", "pressure vessel")
_METAL_FAMILY_WORDS = ("metal", "alloy", "steel", "titanium", "iron", "copper", "brass", "nickel")


def is_scc_susceptible_temper(entry: Dict) -> bool:
    """2xxx and 7xxx aluminium in the peak-aged T6 family of tempers is prone to stress-corrosion cracking."""
    return bool(_SCC_TEMPER.search(str(entry.get("name", "")).lower()))


def safety_critical_duty(prompt: str) -> bool:
    text = (prompt or "").lower()
    return any(w in text for w in _SAFETY_CRITICAL_WORDS)


def fails_safety_critical_screen(entry: Dict, minimum_elongation_percent: float = 8.0, minimum_yield_mpa: float = 200.0) -> bool:
    """Metals for safety-critical members must be wrought, strong enough, ductile and free of stress-corrosion susceptibility."""
    record = MATERIALS_DATABASE.get(entry.get("key"), entry)
    family = str(record.get("family", "")).lower()
    if not any(w in family or w in str(record.get("name", "")).lower() for w in _METAL_FAMILY_WORDS):
        return False  # polymers and composites are assessed by other criteria
    if re.search(r"\b(?:cast|casting|sand|die-cast|permanent mold)\b", str(record.get("name", "")).lower()):
        return True  # cast grades carry porosity and scatter in fatigue life; wrought grades are required for primary load paths
    yield_strength = record.get("yield_strength")
    if yield_strength is not None and float(yield_strength) < minimum_yield_mpa:
        return True  # stiffness indices do not depend on strength, so a strength floor is applied to load-bearing metals
    elongation = record.get("elongation_at_break")
    if elongation is not None and float(elongation) < minimum_elongation_percent:
        return True
    return is_scc_susceptible_temper(record)


def process_note(record: Dict) -> str:
    """Typical manufacturing route for a catalogue grade, by material family."""
    family = str(record.get("family", "")).lower()
    if "composite" in family:
        return "Laminated and cured (autoclave or vacuum bag); CNC trimming"
    if "ceramic" in family:
        return "Pressed and sintered; diamond grinding"
    if "elastomer" in family:
        return "Moulding or extrusion"
    if any(w in family for w in ("polymer", "thermoplastic", "polyamide")):
        return "Injection moulding, extrusion or machining from stock"
    return "CNC machining, casting or forming (grade-dependent)"


def load_modes(prompt: str) -> List[str]:
    """Load cases named in the brief (compression, torsion, bending, tension)."""
    text = (prompt or "").lower()
    modes = []
    for label, words in (("compression", ("compress", "axial load", "buckling")), ("torsion", ("torque", "torsion", "twist")),
                         ("bending", ("bending", "flexur", "cantilever", "deflection")), ("tension", ("tension", "tensile", "pull"))):
        if any(w in text for w in words):
            modes.append(label)
    return modes


_AUSTENITIC = re.compile(r"30[1-9]\d{0,2}|31\d{1,3}|32\d{1,3}|34\d{1,3}|austenitic|nitronic|a286")
_NON_AUSTENITIC_STAINLESS = re.compile(r"\b4[0-4]\d\b|17-4|\bph\b|ferritic|martensitic|duplex")
_CRYOGENIC_POLYMERS = re.compile(r"ptfe|teflon|pctfe|polyimide|kapton|peek|epoxy|g10|fr4")
_NINE_PERCENT_NICKEL = re.compile(r"9\s*%?\s*ni|a553|a353|invar|36\s*%?\s*ni")


def cryogenic_ductile(record: Dict) -> bool:
    """Whether a grade keeps useful ductility at liquid-nitrogen and liquid-helium temperature.

    Face-centred-cubic metals (aluminium, copper, nickel alloys, austenitic stainless steel) and titanium remain tough.
    Body-centred-cubic steels and cast irons, magnesium and glassy thermoplastics become brittle.
    """
    name = str(record.get("name", "")).lower()
    family = str(record.get("family", "")).lower()
    if "magnesium" in family or "magnesium" in name:
        return False
    if any(w in family for w in ("thermoplastic", "polymer", "elastomer", "polyamide")) and "composite" not in family:
        return bool(_CRYOGENIC_POLYMERS.search(name))
    if "composite" in family:
        return "continuous" in family  # continuous-fibre thermoset laminates; short-fibre thermoplastic composites embrittle
    if "stainless" in family or "stainless" in name:
        if _NON_AUSTENITIC_STAINLESS.search(name):
            return False
        return bool(_AUSTENITIC.search(name)) or "316" in name or "304" in name
    if "steel" in family or "steel" in name or ("iron" in family and "cast" in family):
        return bool(_NINE_PERCENT_NICKEL.search(name))
    density = record.get("density")
    if density and 7500.0 <= float(density) <= 7950.0 and not _NINE_PERCENT_NICKEL.search(name):
        return False  # ferritic steel by density where the grade name does not say so (for example national designations)
    return True


_WELDED_STRUCTURE_WORDS = ("weld", "vacuum jacket", "pressure vessel", "tank", "dewar", "boiler", "cryostat")


def welded_structure(prompt: str) -> bool:
    text = (prompt or "").lower()
    return any(w in text for w in _WELDED_STRUCTURE_WORDS)


def is_metal(record: Dict) -> bool:
    family = str(record.get("family", "")).lower()
    name = str(record.get("name", "")).lower()
    return any(w in family or w in name for w in _METAL_FAMILY_WORDS) and "composite" not in family and "polymer" not in family
