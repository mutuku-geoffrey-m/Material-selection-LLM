with open('src/ashby_engine.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace(
    'if "Hadfield" in mat.get("name", "") or "A128" in mat.get("name", "") or "Manganese" in mat.get("name", ""):\n                cutting_factor = 50.0',
    'if "Hadfield" in mat.get("name", "") or "A128" in mat.get("name", "") or "Manganese" in mat.get("name", ""):\n                cutting_factor = 160.0'
)

with open('src/ashby_engine.py', 'w', encoding='utf-8') as f:
    f.write(text)

with open('src/llm_orchestrator.py', 'r', encoding='utf-8') as f:
    orch = f.read()

orch = orch.replace('with urllib.request.urlopen(req, timeout=3.0) as response:', 'with urllib.request.urlopen(req, timeout=15.0) as response:')

with open('src/llm_orchestrator.py', 'w', encoding='utf-8') as f:
    f.write(orch)

print('Updated ashby_engine cutting_factor and llm_orchestrator timeout!')
