from pathlib import Path
import re,json,collections,hashlib
W=Path(__file__).resolve().parent.parent
s=(W/'app/packages/shared/prefix.md').read_bytes().decode('utf8')
assert '~T' not in s
# Explicit textual references, definitions contain no references.
tokens=re.findall(r'[A-Za-z0-9À-ÿ]+|[^A-Za-z0-9À-ÿ]+',s)
c=collections.Counter()
for n in (1,2,4,8,16,32,64):
 for i in range(len(tokens)-n+1):
  p=''.join(tokens[i:i+n])
  if 8<=len(p)<=2400:c[p]+=1
candidates=sorted(((n-1)*len(p.encode())-n*6,p) for p,n in c.items() if n>1)
work=s;d={}
for _,piece in reversed(candidates[-100000:]):
 n=work.count(piece);tag='~T'+str(len(d))+'~'
 saved=(n-1)*len(piece.encode())-n*len(tag)-len(tag)-8
 if n>1 and saved>8:
  d[tag]=piece;work=work.replace(piece,tag)
legend='REFERÊNCIAS TEXTUAIS EXATAS: cada ~Tn~ no corpo representa o trecho literal definido no dicionário. Leia-o em seu lugar, sem acrescentar espaço. As definições não têm referências: substituição única, sem ciclos. Isto é reutilização de texto, não resumo; conteúdo, números, estatutos e ressalvas permanecem integrais.\nDICIONARIO_TEXTUAL\n'
out=legend+json.dumps(d,ensure_ascii=False,separators=(',',':'))+'\nCORPO_TEXTUAL\n'+work
recovered=re.sub(r'~T[0-9]+~',lambda m:d[m[0]],work)
assert recovered==s
p=W/'experiments/candidate_whole_fine.txt';p.write_bytes(out.encode())
r={'before':len(s.encode()),'after':len(out.encode()),'dictionary_entries':len(d),'dictionary_bytes':len(json.dumps(d,ensure_ascii=False).encode()),'roundtrip_equal':True,'source_sha256':hashlib.sha256(s.encode()).hexdigest(),'candidate_sha256':hashlib.sha256(out.encode()).hexdigest()}
(W/'experiments/WHOLE_FINE_EXPERIMENT.json').write_bytes(json.dumps(r,indent=2).encode());print(json.dumps(r))

