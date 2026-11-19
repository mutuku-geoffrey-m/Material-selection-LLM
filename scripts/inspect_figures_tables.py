import re

with open('proposal.tex', 'r', encoding='utf-8') as f:
    text = f.read()

figs = re.finditer(r'\\begin\{(figure|table)\*?\}(.*?)\\end\{\1\*?\}', text, re.DOTALL)
count = 0
for m in figs:
    count += 1
    env_type = m.group(1)
    content = m.group(2)
    cap = re.search(r'\\caption\{([^}]+)\}', content)
    cap_text = cap.group(1) if cap else "No caption"
    print(f"{count}. [{env_type}] {cap_text[:80]}")
