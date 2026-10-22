from pathlib import Path
import sys,json,re,collections
B=Path(r'C:\IALD\Central de Patentes\work\iald_jev_v380_20261002\memory_build');sys.path.insert(0,str(B));import haiku_codec as c
S=B.parent/'memory_stage';p=(S/'haiku_prefix.md').read_text(encoding='utf-8');m=json.loads((S/'manifest_staged.json').read_bytes());source=json.loads(Path(m['published_evidence']['result']['path']).read_bytes());rows=[]
for block in p.split(c.MARKER)[0].split('\n### ')[1:]:
 topic,body=block.split('\n',1)
 if topic not in source['core']:continue
 for line in body.splitlines():
  if not line.startswith('{'):continue
  try:v=json.loads(line)
  except ValueError:continue
  checks=v.get('checks')
  if isinstance(checks,list) and checks and all(isinstance(x,list) and len(x)==2 and x[1] is True for x in checks):
   assert checks==source['core'][topic]['checks'];rows.append([topic,len(checks),len(c.dump(checks).encode())])
print('checks',json.dumps(rows), 'totalbytes',sum(x[2] for x in rows));print('tags',json.dumps({x:p.count(x) for x in ['@SOURCE_FIELDS','@SOURCE_ITEMS','@TGL_LITERAL','@EXPOSITION','@SUMMARY']}))
rows=[]
for block in p.split(c.MARKER)[0].split('\n### ')[1:]:
 topic,body=block.split('\n',1)
 if topic not in source['core']:continue
 for line in body.splitlines():
  if not line.startswith('{'):continue
  try:v=json.loads(line)
  except ValueError:continue
  for k,x in v.items():
   if len(c.dump(x).encode())>600:rows.append([len(c.dump(x).encode()),topic,k,type(x).__name__])
print('largestfields',json.dumps(sorted(rows,reverse=True)[:45]))
print('parts',len(p.split(c.MARKER)[0].encode()),len(p.split(c.MARKER)[1].encode()))