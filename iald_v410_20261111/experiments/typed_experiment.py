from pathlib import Path
import json,collections,re,hashlib
W=Path(__file__).resolve().parent.parent;s=(W/'app/packages/shared/prefix.md').read_bytes().decode();lines=s.splitlines(keepends=True);objs={};schemas=collections.Counter()
def dump(x):return json.dumps(x,ensure_ascii=False,separators=(',',':'))
def scan(x):
 if isinstance(x,dict):
  schemas[tuple(x)]+=1
  for v in x.values():scan(v)
 elif isinstance(x,list):
  for v in x:scan(v)
for i,l in enumerate(lines):
 try:v=json.loads(l)
 except ValueError:continue
 if isinstance(v,(dict,list)):objs[i]=v;scan(v)
lookup={k:'S'+str(i) for i,(k,n) in enumerate(schemas.items()) if len(k)>1 and n>1 and (n-1)*sum(len(x)+3 for x in k)>n*12+20}
columns={v:list(k) for k,v in lookup.items()};stats=collections.Counter()
def encode(x,top=False):
 if isinstance(x,dict):
  if not top and tuple(x) in lookup:return {'@row':[lookup[tuple(x)],*[encode(v) for v in x.values()]]}
  return {k:encode(v) for k,v in x.items()}
 if isinstance(x,list):
  if len(x)>3 and all(isinstance(v,str) and re.fullmatch(r'[\w./]+',v) for v in x):
   groups=[]
   for name in x:
    sep='.' if '.' in name else '/' if '/' in name else ''
    prefix=name.rsplit(sep,1)[0]+sep if sep else '';tail=name[len(prefix):]
    if groups and groups[-1][0]==prefix:groups[-1][1].append(tail)
    else:groups.append([prefix,[tail]])
   new={'@names':groups}
   if len(dump(new).encode())<len(dump(x).encode()):stats['names_saved']+=len(dump(x).encode())-len(dump(new).encode());return new
  return [encode(v) for v in x]
 return x
def decode(x):
 if isinstance(x,dict):
  if set(x)=={'@row'}:
   a=x['@row'];return {k:decode(v) for k,v in zip(columns[a[0]],a[1:],strict=True)}
  if set(x)=={'@names'}:return [p+t for p,ss in x['@names'] for t in ss]
  return {k:decode(v) for k,v in x.items()}
 if isinstance(x,list):return [decode(v) for v in x]
 return x
for i,v in objs.items():
 e=encode(v,True);assert decode(e)==v;lines[i]=dump(e)+'\n'
legend='TABELAS E NAMESPACES SEM PERDAS: {"@row":["Sn",v1,...]} representa objeto com chaves de Sn na ordem indicada e respectivos valores. {"@names":[[prefixo,[nomes]],...]} representa lista ordenada dos identificadores prefixo+nome; concatenação literal sem espaço, mantendo ordem dos grupos e dos nomes. Prefixos terminam em ponto ou barra e nomes finais ficam escritos integralmente. Não é lista de enunciados nem prova. Tipos e valores permanecem JSON; nenhuma coluna implícita.\nCOLUNAS\n'
out=legend+dump(columns)+'\n'+''.join(lines)
(W/'experiments/candidate_typed.txt').write_bytes(out.encode())
r=dict(status='EXPERIMENT_NOT_INTEGRATED',before=len(s.encode()),after=len(out.encode()),schemas=len(columns),stats=dict(stats),json_roundtrips=len(objs),full_residence=True)
(W/'experiments/TYPED_EXPERIMENT.json').write_bytes(json.dumps(r,indent=2).encode());print(json.dumps(r))
