"""Read every new exact line; repeated lines are byte-for-byte compared in memory.

The caller must have read the complete prefix before advancing start. The canonical
Atlas is never copied, rewritten or summarized. Context headings are always printed.
"""
from pathlib import Path
import hashlib
import sys

sys.stdout.reconfigure(encoding="utf8")
source = Path(r"C:\IALD\Central de Patentes\memory\TGL_ATLAS.md")
raw = source.read_bytes()
lines = raw.decode("utf8").splitlines()
start = int(sys.argv[1])
budget = int(sys.argv[2]) if len(sys.argv) > 2 else 26000
seen = {}
for i, line in enumerate(lines[:start - 1], 1):
    seen.setdefault(line, i)
size = 0
duplicates = 0
for i in range(start - 1, len(lines)):
    line = lines[i]
    if line in seen and not line.lstrip().startswith("#"):
        duplicates += 1
        continue
    text = f"{i+1}: {line}\n"
    if size and size + len(text) > budget:
        print(f"NEXT_LINE={i+1}")
        break
    print(text, end="")
    size += len(text)
    seen.setdefault(line, i + 1)
else:
    print("END_ATLAS")
print(f"EXACT_REPEATED_LINES={duplicates}; TOTAL_LINES={len(lines)}; SHA256={hashlib.sha256(raw).hexdigest()}")
