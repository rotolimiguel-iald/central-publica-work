from pathlib import Path
import json,sys,collections
B=Path(__file__).resolve().parent;sys.path.insert(0,str(B));import haiku_codec as c
p=(B.parent/'memory_stage/haiku_prefix.md').read_text(encoding='utf-8');counts=collections.Counter();gain=0;names=('all_verified','does_not_gate_core','in_contour_roster_v314')
for b in p.split(c.MARKER)[0].split('\n### ')[1:]:
 for l in b.splitlines()[1:]:
  if not l.startswith('{'):continue
  try:v=json.loads(l)
  except ValueError:continue
  flags={k:v[k] for k in names if type(v.get(k)) is bool}
  if len(flags)>=2:counts[c.dump(flags)]+=1;gain+=len(c.dump(flags))-len('{"@FLAGS":"1"}')
print(json.dumps(dict(counts),ensure_ascii=False));print('bytegain',gain)