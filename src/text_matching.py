"""Boundary-aware keyword matching for free-text engineering prompts.

Plain substring tests mis-fire on short stems ("pan" in "panel", "toy" in "toyota").
``KeywordText`` behaves like ``str`` but its ``in`` operator applies two rules:

* keywords of up to three characters must match a whole word (optionally plural);
* longer keywords match anywhere, so compounds such as "sailboat", "gearbox" and
  "driveshaft" are still recognised, except in a short list of known collisions
  (for example "race" inside "trace" or "table" inside "stable").
"""
import re
from functools import lru_cache

# keyword -> left contexts in which the keyword must NOT match
_COLLISIONS = {
    "race": ("t", "b", "g", "br", "emb"),
    "wing": ("s", "t", "sw"),
    "table": ("s", "unst", "vege", "ins", "suit", "port", "comput", "compat"),
    "plate": ("tem", "com"),
    "pipe": (),
    "boat": (),
}


@lru_cache(maxsize=None)
def _pattern(needle: str):
    escaped = re.escape(needle)
    stripped = needle.strip()
    if 0 < len(stripped) <= 3 and stripped.isalnum():
        return re.compile(r"(?<![a-z0-9])" + escaped + r"s?(?![a-z0-9])")
    guards = _COLLISIONS.get(stripped, ())
    lookbehind = "".join(f"(?<!{g})" for g in guards)
    return re.compile(lookbehind + escaped)


class KeywordText(str):
    """Lower-cased prompt text whose ``in`` operator is boundary-aware."""

    def __contains__(self, needle) -> bool:
        if not isinstance(needle, str) or not needle:
            return False
        return _pattern(needle).search(self) is not None


def as_keyword_text(text: str) -> "KeywordText":
    return KeywordText((text or "").lower())
