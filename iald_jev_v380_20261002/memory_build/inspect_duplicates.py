from pathlib import Path
import sys,json,collections
B=Path(__file__).resolve().parent;sys.path.insert(0,str(B));import haiku_codec as c
S=B.parent/'memory_stage';p=(S/'haiku_prefix.md').read_text(encoding='utf-8');m=json.loads((S/'manifest_staged.json').read_bytes());s=json.loads(Path(m['published_evidence']['result']['path']).read_bytes());counts=collections.Counter()
def visit(v,key=''):
 if isinstance(v,str) and len(v)>=32 and key not in ('@','source_pointer','starts_with') and not key.startswith('@'):counts[v]+=1
 elif isinstance(v,list):
  for x in v:visit(x,key)
 elif isinstance(v,dict):
  for k,x in v.items():
   if len(k)>=7:counts[k]+=1
   visit(x,k)
for b in p.split(c.MARKER)[0].split('\n### ')[1:]:
 n,body=b.split('\n',1)
 if n not in s['core']:continue
 for l in body.splitlines():
  if l.startswith('{'):
   try:visit(json.loads(l))
   except ValueError:pass
rows=sorted(((n-1)*len(c.dump(v).encode())-n*15-12,n,v) for v,n in counts.items() if n>1)
print('positive_count',sum(g>0 for g,n,v in rows),'bytegain',sum(g for g,n,v in rows if g>0))
print(json.dumps([[g,n,v[:150]] for g,n,v in rows[-15:]],ensure_ascii=False))