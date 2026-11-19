# -*- coding: utf-8 -*-
import sys

with open('src/nlp_parser.py', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add is_crusher_jaw
old_cutting = """        # Cutting tool / blade detection (Must precede bottle / optical glass detection)
        is_cutting_tool = bool(re.search("""

new_cutting = """        # Heavy rock crushing / stone crusher jaw / extreme gouging abrasion plate detection
        is_crusher_jaw = bool(re.search(
            r'\\b(?:crusher|stone crusher|jaw crusher|crusher jaw|crusher plate|jaw plate|crushing jaw|'
            r'rock crusher|impact crusher|crushing plate|hammer mill|ball mill liner|ore chute|mining wear plate|'
            r'grizzly bar|crushing tooth|quarry crusher)\\b',
            prompt_lower
        )) or (any(w in prompt_lower for w in ['crusher', 'crushing', 'stone crusher', 'jaw']) and any(w in prompt_lower for w in ['hardness', 'strength', 'impact', 'rock', 'stone', 'abrasion', 'wear']))

        # Cutting tool / blade detection (Must precede bottle / optical glass detection)
        is_cutting_tool = bool(re.search("""

assert old_cutting in text, "old_cutting not found"
text = text.replace(old_cutting, new_cutting, 1)

# 2. Add component_type mapping
old_comp = """        if is_cutting_tool:
            component_type = "cutting_tool_or_blade\""""

new_comp = """        if is_crusher_jaw:
            component_type = "heavy_impact_crushing_or_abrasion_jaw"
        elif is_cutting_tool:
            component_type = "cutting_tool_or_blade\""""

assert old_comp in text, "old_comp not found"
text = text.replace(old_comp, new_comp, 1)

# 3. Add ashby index deduction
old_index = """        elif component_type == "cutting_tool_or_blade":
            ashby_key = AshbyIndex.TIE_STRENGTH
            ashby_reasoning = "Cutting tool / blade requiring maximum edge yield strength and wear resistance: M = σ_y / ρ.\""""

new_index = """        elif component_type == "heavy_impact_crushing_or_abrasion_jaw":
            ashby_key = AshbyIndex.TIE_STRENGTH
            ashby_reasoning = "Heavy-duty stone crusher jaw plate subject to severe gouging rock impact and abrasive wear. Governed by high yield strength, impact toughness, and austenitic work-hardening capability (such as ASTM A128 Hadfield Manganese Steel): M = σ_y / ρ."
        elif component_type == "cutting_tool_or_blade":
            ashby_key = AshbyIndex.TIE_STRENGTH
            ashby_reasoning = "Cutting tool / blade requiring maximum edge yield strength and wear resistance: M = σ_y / ρ.\""""

assert old_index in text, "old_index not found"
text = text.replace(old_index, new_index, 1)

# 4. Add boundary condition flags
old_bnd = """                "marine_industrial_exposure": is_marine_industrial,"""
new_bnd = """                "marine_industrial_exposure": is_marine_industrial,
                "heavy_impact_crushing": is_crusher_jaw,
                "extreme_wear_abrasion_required": is_crusher_jaw,"""

assert old_bnd in text, "old_bnd not found"
text = text.replace(old_bnd, new_bnd, 1)

with open('src/nlp_parser.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("SUCCESS: nlp_parser.py updated with stone crusher jaw domain!")
