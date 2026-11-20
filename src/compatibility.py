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


def marine_service(prompt: str) -> bool:
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
