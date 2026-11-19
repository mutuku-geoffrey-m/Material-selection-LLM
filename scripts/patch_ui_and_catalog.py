import sys, os, re
sys.path.insert(0, os.path.abspath("."))

# 1. Patch src/ashby_engine.py to be defensive on fdm_printability
with open('src/ashby_engine.py', 'r', encoding='utf-8') as f:
    ashby_code = f.read()

# Replace mat["fdm_printability"]["ease_of_printing"] with safe get
ashby_code = re.sub(
    r'is_fdm\s*=\s*mat\["fdm_printability"\]\["ease_of_printing"\]\s*!=\s*"Not FDM Printable"',
    'fdm_info = mat.get("fdm_printability") or {}\n        is_fdm = fdm_info.get("ease_of_printing", "Not FDM Printable") != "Not FDM Printable"',
    ashby_code
)

with open('src/ashby_engine.py', 'w', encoding='utf-8') as f:
    f.write(ashby_code)

print("Patched ashby_engine.py with safe fdm_printability check")

# 2. Ensure all materials in MATERIALS_DATABASE and materials_catalog.json have fdm_printability and cost_per_kg_usd
import src.materials_db as db
import json

default_fdm = {
    'ease_of_printing': 'Not FDM Printable',
    'nozzle_temperature_min': 0,
    'nozzle_temperature_max': 0,
    'bed_temperature_min': 0,
    'bed_temperature_max': 0,
    'enclosure_required': False,
    'warping_tendency': 'N/A',
    'abrasive_nozzle_required': False,
    'recommended_nozzle_type': 'N/A (Foundry casting / Forging / Wrought)',
    'layer_adhesion_quality': 'Isotropic',
    'hygroscopic_sensitivity': 'None',
    'filament_drying_temp': 0,
    'filament_drying_hours': 0
}

# Read materials_db.py source and patch any missing fdm_printability
with open('src/materials_db.py', 'r', encoding='utf-8') as f:
    db_source = f.read()

for k, v in list(db.MATERIALS_DATABASE.items()):
    cost = v.get('cost_per_kg_usd')
    if cost is None and 'techno_economics' in v and 'raw_cost_usd_per_kg' in v['techno_economics']:
        v['cost_per_kg_usd'] = float(v['techno_economics']['raw_cost_usd_per_kg'])
    if 'fdm_printability' not in v or not isinstance(v.get('fdm_printability'), dict):
        v['fdm_printability'] = default_fdm

# Check catalog
with open('data/materials_catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

for k, m in (catalog.items() if isinstance(catalog, dict) else enumerate(catalog)):
    cost = m.get('cost_per_kg_usd')
    if (cost is None or cost == 0) and 'techno_economics' in m and 'raw_cost_usd_per_kg' in m['techno_economics']:
        m['cost_per_kg_usd'] = float(m['techno_economics']['raw_cost_usd_per_kg'])
    if 'fdm_printability' not in m or not isinstance(m.get('fdm_printability'), dict):
        m['fdm_printability'] = default_fdm
    if 'ANSI Magnesium Alloy AM100A' in m.get('name', ''):
        m['cost_per_kg_usd'] = 8.50
        if 'techno_economics' not in m:
            m['techno_economics'] = {'raw_cost_usd_per_kg': 8.50}

with open('data/materials_catalog.json', 'w', encoding='utf-8') as f:
    json.dump(catalog, f, indent=2)

print("Synchronized data/materials_catalog.json")

# 3. Patch app.py lines for stat-value score and cost
with open('app.py', 'r', encoding='utf-8') as f:
    app_code = f.read()

# Replace score stat-value
old_score_pattern = '<div class="stat-value">{top_mat.get(\'score\', 0):.2f}</div>'
new_score_replacement = '<div class="stat-value">{top_mat.get(\'final_metric\', top_mat.get(\'raw_score\', top_mat.get(\'score\', 0.0))):.2f}</div>'
if old_score_pattern in app_code:
    app_code = app_code.replace(old_score_pattern, new_score_replacement)
    print("Replaced score stat-value in app.py")

# Replace cost stat-value
old_cost_pattern = '<div class="stat-value">${top_mat_data.get(\'cost_per_kg_usd\', 0):.2f} <span style="font-size: 11px;">/ kg</span></div>'
new_cost_replacement = '<div class="stat-value">${(top_mat_data.get(\'cost_per_kg_usd\') or top_mat_data.get(\'techno_economics\', {}).get(\'raw_cost_usd_per_kg\', 0.0)):.2f} <span style="font-size: 11px;">/ kg</span></div>'
if old_cost_pattern in app_code:
    app_code = app_code.replace(old_cost_pattern, new_cost_replacement)
    print("Replaced cost stat-value in app.py")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(app_code)
