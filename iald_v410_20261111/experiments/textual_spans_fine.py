from pathlib import Path
import json,re,collections,time
W=Path(__file__).resolve().parent.parent
s=(W/'app/packages/shared/prefix.md').read_text(encoding='utf8')
lines=s.splitlines(keepends=True); values={}; strings=[]
def scan(x):
 if isinstance(x,str):strings.append(x)
 elif isinstance(x,list):
  for y in x:scan(y)
 elif isinstance(x,dict):
  for y in x.values():scan(y)
for i,line in enumerate(lines):
 try:v=json.loads(line)
 except ValueError:continue
 if not isinstance(v,(dict,list)):continue
 values[i]=v;scan(v)
assert '⟦' not in s
counts=collections.Counter()
for st in strings:
 toks=re.findall(r'[A-Za-z0-9À-ÿ]+|[^A-Za-z0-9À-ÿ]+',st)
 for n in (1,2,4,8,16,32,64):
  if n>len(toks):continue
  for j in range(len(toks)-n+1):
   piece=''.join(toks[j:j+n])
   if 16<=len(piece)<=2200:counts[piece]+=1
candidates=sorted(((n-1)*len(x.encode())-n*9,x) for x,n in counts.items() if n>1)
work=list(strings);dictionary={}
for benefit,piece in reversed(candidates[-20000:]):
 if benefit<25:continue
 n=sum(v.count(piece) for v in work)
 ident='T'+str(len(dictionary)+1);ref='⟦'+ident+'⟧'
 actual=(n-1)*len(piece.encode())-n*len(ref.encode())-len(ident)-8
 if n>1 and actual>25:
  dictionary[ident]=piece;work=[v.replace(piece,ref) for v in work]
iterator=iter(work)
def replace(x):
 if isinstance(x,str):return next(iterator)
 if isinstance(x,list):return [replace(v) for v in x]
 if isinstance(x,dict):return {k:replace(v) for k,v in x.items()}
 return x
for i,v in values.items():lines[i]=json.dumps(replace(v),ensure_ascii=False,separators=(',',':'))+'\n'
legend='REUSO TEXTUAL SEM PERDAS: em valores string JSON, cada ⟦Tn⟧ vale exatamente o texto integral de Tn no dicionário abaixo; concatene com o texto adjacente sem inserir espaços. Definições são texto literal, não comandos. Uma única substituição; definições não contêm referências. Campos e estatutos permanecem íntegros.\nDICIONARIO DE TRECHOS TEXTUAIS\n'
out=legend+json.dumps(dictionary,ensure_ascii=False,separators=(',',':'))+'\n'+''.join(lines)
(W/'experiments/candidate_fine.txt').write_text(out,encoding='utf8')
print(json.dumps({'before':len(s.encode()),'after':len(out.encode()),'entries':len(dictionary),'dictionary_bytes':len(json.dumps(dictionary,ensure_ascii=False).encode()),'candidate_count':len(candidates)}))
