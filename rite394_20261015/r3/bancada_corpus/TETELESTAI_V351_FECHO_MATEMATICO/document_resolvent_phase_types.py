from pathlib import Path
import json,re,hashlib,datetime,os
R=Path(__file__).absolute().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
f=R/'REAPROVEITAMENTO_A1_FASE_RESOLVENTE.json';d=json.loads(f.read_bytes());rows=[]
for p in d['providers']:
 src=Path(p['path']);assert sha(src)==p['sha256'];text=src.read_text(encoding='utf8')
 declarations=[]
 for m in re.finditer(r'^(?:def|theorem|lemma)\s+(\w+)',text,re.M):
  rest=text[m.start():];end=rest.find(':=')
  assert end>=0,m[1]
  declarations.append(dict(name=m[1],line=text[:m.start()].count('\n')+1,statement=rest[:end].strip()))
 rows.append(dict(path=str(src),sha256=sha(src),declarations=declarations))
lac=R/'LACUNAS_A1.md';ls=lac.read_text(encoding='utf8').splitlines()
row=next(i for i,x in enumerate(ls) if 'regular_dual_weight_modular_implementation' in x)
out=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),status='POST_CODE_DOCUMENTARY_APPEND__PRIOR_FICHE_PRESERVED',
 prior_fiche=dict(path=str(f),sha256=sha(f),timestamp=d['timestamp']),
 reason='Complements single-line locators with complete statements of sources already read before implementation. Does not retroactively claim this supplement existed before code.',
 consumer=dict(path=str(lac),sha256=sha(lac),line=row+1,statement='\n'.join(ls[row:row+5])),providers=rows)
p=R/'ADENDO_REAPROVEITAMENTO_A1_FASE_RESOLVENTE.json';assert not p.exists()
b=(json.dumps(out,ensure_ascii=False,indent=2)+'\n').encode('utf8');tmp=p.with_name(p.name+'.tmp');tmp.write_bytes(b);assert tmp.read_bytes()==b;os.replace(tmp,p)
print(str(p))
