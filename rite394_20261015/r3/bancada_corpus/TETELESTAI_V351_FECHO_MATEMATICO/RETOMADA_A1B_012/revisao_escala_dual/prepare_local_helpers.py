from pathlib import Path
import hashlib,json,os
R=Path(__file__).resolve().parent.parent;OUT=Path(__file__).resolve().parent;BASE=R/'revisao_afiliacao'
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def fresh(p,b):
 assert p.resolve().is_relative_to(OUT.resolve()) and not p.exists(),p
 p.parent.mkdir(parents=True,exist_ok=True);t=p.with_name(p.name+'.tmp')
 with t.open('xb') as f:f.write(b)
 assert t.read_bytes()==b;os.replace(t,p)
rows=[]
for name in ['build_delta.py','finish_delta.py','read_author_controls.py']:
 src=BASE/name;b=src.read_bytes();fresh(OUT/'helper_origins'/name,b);s=b.decode('utf8')
 if name=='build_delta.py':
  old="'afiliacao':('revisao_afiliacao',['V351RegularGeneratorAffiliation'],3,['REAPROVEITAMENTO_A1B_AFILIACAO_REGULAR'])}"
  new="'afiliacao':('revisao_afiliacao',['V351RegularGeneratorAffiliation'],3,['REAPROVEITAMENTO_A1B_AFILIACAO_REGULAR']),\n 'escala_dual':('revisao_escala_dual',['V351RegularGeneratorDualScaling'],7,['REAPROVEITAMENTO_A1B_ESCALA_DUAL_REGULAR','ADENDO_FICHA_ESCALA_DUAL'])}"
 elif name=='finish_delta.py':
  old="'afiliacao':['dev_regular_affiliation/20260914_194034_466190/run.json']}[key]"
  new="'afiliacao':['dev_regular_affiliation/20260914_194034_466190/run.json'],\n  'escala_dual':['dev_regular_dual_scaling/20260914_200033_241925/run.json']}[key]"
 else:
  old="'afiliacao':'AUDITORIA_AFILIACAO_REGULAR_A1B.json'}"
  new="'afiliacao':'AUDITORIA_AFILIACAO_REGULAR_A1B.json','escala_dual':'AUDITORIA_ESCALA_DUAL_REGULAR_A1B.json'}"
 assert s.count(old)==1;(OUT/'helper_origins').mkdir(exist_ok=True)
 s=s.replace(old,new);fresh(OUT/name,s.encode('utf8'))
 rows.append(dict(parent=pin(src),snapshot=pin(OUT/'helper_origins'/name),local=pin(OUT/name)))
fresh(OUT/'helper_provenance.json',(json.dumps(dict(scope='Only new dual-scaling configuration; sealed helpers and reports unchanged',rows=rows),indent=2)+'\n').encode())
