import re

with open('proposal.tex', 'r', encoding='utf-8') as f:
    text = f.read()

# Check begin/end balance
begins = re.findall(r'\\begin\{([^}]+)\}', text)
ends = re.findall(r'\\end\{([^}]+)\}', text)

print(f"Total \\begin: {len(begins)}, Total \\end: {len(ends)}")
if len(begins) != len(ends):
    print("Mismatch!")
    for b in set(begins):
        bc = begins.count(b)
        ec = ends.count(b)
        if bc != ec:
            print(f"  {b}: {bc} vs {ec}")
else:
    print("All environments match perfectly!")

# Check citations exist in bibitems
bibs = set(re.findall(r'\\bibitem\{([^}]+)\}', text))
cites = re.findall(r'\\cite\{([^}]+)\}', text)
all_cite_keys = []
for c in cites:
    for k in c.split(','):
        all_cite_keys.append(k.strip())

missing = [k for k in all_cite_keys if k not in bibs]
print(f"Total citations referenced: {len(all_cite_keys)}")
print(f"Missing citation keys: {missing}")

# Check for banned AI clichés in proposal.tex
banned_phrases = [
    "delve", "tapestry", "revolutionize", "game-changer", "beacon", "testament",
    "fosters", "pivotal", "paramount", "harnessing", "unveiling", "plethora",
    "furthermore, it is important to remember", "in conclusion, it is evident",
    "not only... but also", "a testament to", "rich tapestry"
]
found_cliches = [p for p in banned_phrases if p in text.lower()]
print(f"Banned AI clichés found: {found_cliches}")
