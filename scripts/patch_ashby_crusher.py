# -*- coding: utf-8 -*-
import sys

with open('src/ashby_engine.py', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Filter out soft materials for crusher jaws
old_filter = """        # Check Chemical & Coolant Corrosion Filter (Disqualify reactive Magnesium in coolants/chemicals)
        if (chemical_exposure or "coolant" in prompt_lower) and ("Magnesium" in mat.get("family", "") or "Magnesium" in mat.get("name", "")):
            continue"""

new_filter = """        # Check Chemical & Coolant Corrosion Filter (Disqualify reactive Magnesium in coolants/chemicals)
        if (chemical_exposure or "coolant" in prompt_lower) and ("Magnesium" in mat.get("family", "") or "Magnesium" in mat.get("name", "")):
            continue

        # Heavy Rock Crushing / Stone Crusher Jaw Integrity Filter
        # Rock crushing involves severe compressive crushing loads, gouging impact, and rock abrasion (quartz/granite).
        # Soft alloys (Magnesium, Aluminum, Brass/Bronze) and unreinforced polymers suffer catastrophic crushing failure or severe smearing.
        is_rock_crushing = any(w in prompt_lower for w in ["crusher", "stone crusher", "jaw crusher", "crusher jaw", "crushing jaw", "rock crusher", "jaw plate", "crushing plate", "hammer mill"])
        if is_rock_crushing:
            fam = mat.get("family", "")
            if any(w in fam for w in ["Magnesium", "Aluminum", "Copper", "Brass", "Thermoplastic", "Polymer", "Elastomer"]):
                continue
            # Non-hardened mild structural steels without sufficient yield/toughness cannot sustain rock crushing
            if mat.get("yield_strength", 0) < 300.0:
                continue"""

assert old_filter in text, "old_filter not found"
text = text.replace(old_filter, new_filter, 1)

# 2. Add crushing wear scoring multiplier
old_factor = """        cutting_factor = 1.0
        if cutting_edge_hardness_required:"""

new_factor = """        cutting_factor = 1.0
        if is_rock_crushing:
            # Hadfield Austenitic Manganese Steel (ASTM A128) is the global gold standard for crusher jaws
            # because its austenitic matrix work-hardens dynamically under rock impact from 230 HB to 550+ HB
            if "Hadfield" in mat.get("name", "") or "A128" in mat.get("name", "") or "Manganese" in mat.get("name", ""):
                cutting_factor = 50.0
            elif "Hardox" in mat.get("name", ""):
                cutting_factor = 35.0
            elif "A532" in mat.get("name", "") or "High-Chromium" in mat.get("name", ""):
                crushing_factor = 30.0
            elif mat_key in ["AISI_S7_Shock_Resisting_Tool_Steel", "AISI_4340_Quenched_Tempered", "AISI_D2_Cold_Work_Tool_Steel"]:
                cutting_factor = 25.0
            elif any(w in mat.get("family", "") for w in ["Alloy Steel", "Tool Steel"]):
                cutting_factor = 15.0
            else:
                cutting_factor = 1.0
        elif cutting_edge_hardness_required:"""

assert old_factor in text, "old_factor not found"
text = text.replace(old_factor, new_factor, 1)

with open('src/ashby_engine.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("SUCCESS: ashby_engine.py updated with stone crusher jaw physics and Hadfield steel priority!")
