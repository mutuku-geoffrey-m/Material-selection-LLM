import re

# Load proposal.tex
with open('proposal.tex', 'r', encoding='utf-8') as f:
    text = f.read()

# Build citation number map from thebibliography
bib_matches = re.findall(r'\\bibitem\{([^}]+)\}', text)
cite_to_num = {key: i + 1 for i, key in enumerate(bib_matches)}
print(f"Loaded {len(cite_to_num)} bibliographic keys.")

# 1. Function to sort and separate multiple citations: \cite{a, b, c} -> \cite{a}, \cite{b}, \cite{c}
def fix_citations(match):
    raw_keys = match.group(1)
    keys = [k.strip() for k in raw_keys.split(',') if k.strip()]
    if not keys:
        return match.group(0)
    # Sort keys by their index in thebibliography
    keys_sorted = sorted(keys, key=lambda k: cite_to_num.get(k, 999))
    return ", ".join([f"\\cite{{{k}}}" for k in keys_sorted])

# Replace all \cite{...} that contain commas
fixed_cites_text = re.sub(r'\\cite\{([^}]+,[^}]+)\}', fix_citations, text)

# Write back temporarily to check diff
print("Fixed multi-cites into ascending numerical separate citations.")
with open('proposal.tex', 'w', encoding='utf-8') as f:
    f.write(fixed_cites_text)
