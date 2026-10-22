"""Read canonical Atlas without copying it; exact repeated paragraphs reference
their first occurrence. No summary or semantic deduplication is performed.
The caller must actually inspect each emitted unique paragraph before advancing.
"""
from pathlib import Path
import hashlib, re, sys
sys.stdout.reconfigure(encoding='utf8')
p = Path(r'C:\IALD\Central de Patentes\memory\TGL_ATLAS.md')
b = p.read_bytes(); s = b.decode('utf8').replace('\r\n','\n')
start = int(sys.argv[1]); budget = int(sys.argv[2]) if len(sys.argv)>2 else 22000
parts=[]; seen={}; pos=0; repeated=[]
for m in re.finditer(r'[^\n](?:[^\n]|\n(?!\s*\n))*', s):
    text=m.group(); first=s.count('\n',0,m.start())+1; last=first+text.count('\n')
    # Preserve exact paragraph text; only wholly repeated text is referenced.
    if last < start:
        seen.setdefault(text,(first,last)); continue
    if first < start:
        first=start; text='\n'.join(s.splitlines()[start-1:last])
    if text in seen:
        old=seen[text]
        repeated.append((first,last,old[0],old[1]))
        continue
    else:
        item=f'[{first}–{last}]\n{text}\n'
    if parts and pos+len(item)>budget:
        print(''.join(parts))
        print(f'EXACT_REPEATS={len(repeated)} (equality checked against preceding paragraphs)')
        print(f'NEXT_LINE={first}; SHA256={hashlib.sha256(b).hexdigest()}')
        break
    parts.append(item);pos+=len(item);seen.setdefault(text,(first,last))
else:
    print(''.join(parts));print(f'EXACT_REPEATS={len(repeated)} (equality checked against preceding paragraphs)')
    print(f'END_ATLAS; SHA256={hashlib.sha256(b).hexdigest()}')
