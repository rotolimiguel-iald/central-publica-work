from pathlib import Path
import json,collections,sys
W=Path(__file__).resolve().parent.parent
p=Path(sys.argv[1]);s=p.read_text(encoding='utf8');lines=s.splitlines(keepends=True);values={};schemas=collections.Counter();keys=collections.Counter()
def scan(x):
 if isinstance(x,dict):
  schemas[tuple(x)]+=1
  for k,v in x.items():keys[k]+=1;scan(v)
 elif isinstance(x,list):
  for v in x:scan(v)
for i,l in enumerate(lines):
 try:v=json.loads(l)
 except ValueError:continue
 if isinstance(v,(list,dict)):values[i]=v;scan(v)
lookup={k:'S'+str(i) for i,(k,n) in enumerate(schemas.items()) if len(k)>=2 and n>1 and (n-1)*sum(len(x)+3 for x in k)>n*15+20}
def encode(x,top=False):
 if isinstance(x,dict):
  schema=tuple(x)
  if not top and schema in lookup:return {'@ROW':[lookup[schema],*[encode(v) for v in x.values()]]}
  return {k:encode(v) for k,v in x.items()}
 if isinstance(x,list):return [encode(v) for v in x]
 return x
d={v:list(k) for k,v in lookup.items()}
for i,v in values.items():lines[i]=json.dumps(encode(v,True),ensure_ascii=False,separators=(',',':'))+'\n'
legend='TABELAS SEM PERDAS: um objeto {"@ROW":["Sn",v1,...]} tem as colunas, em ordem, de Sn no dicionário abaixo, com os valores v1,... na mesma ordem. Não inferir colunas ou valores ausentes; tipos são JSON.\nDICIONARIO DE COLUNAS\n'
out=legend+json.dumps(d,ensure_ascii=False,separators=(',',':'))+'\n'+''.join(lines)
(W/'experiments/candidate_tables.txt').write_text(out,encoding='utf8')
print(json.dumps({'before':len(s.encode()),'after':len(out.encode()),'schemas':len(d)}))
