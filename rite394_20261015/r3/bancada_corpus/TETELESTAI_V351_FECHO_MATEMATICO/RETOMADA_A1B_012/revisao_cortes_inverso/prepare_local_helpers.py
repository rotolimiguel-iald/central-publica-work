from pathlib import Path
import hashlib,json,os
R=Path(__file__).resolve().parent.parent;OUT=Path(__file__).resolve().parent;BASE=R/'revisao_escala_dual'
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
  old="'escala_dual':('revisao_escala_dual',['V351RegularGeneratorDualScaling'],7,['REAPROVEITAMENTO_A1B_ESCALA_DUAL_REGULAR','ADENDO_FICHA_ESCALA_DUAL'])}"
  new="'escala_dual':('revisao_escala_dual',['V351RegularGeneratorDualScaling'],7,['REAPROVEITAMENTO_A1B_ESCALA_DUAL_REGULAR','ADENDO_FICHA_ESCALA_DUAL']),\n 'cortes_inverso':('revisao_cortes_inverso',['V351InverseGeneratorCutoff'],8,['REAPROVEITAMENTO_A1B_CORTES_INVERSO','ADENDO_FICHA_INVERSO_BILATERAL'])}"
  guard="'revisao_potencias','revisao_afiliacao']"
  assert s.count(guard)==2
  s=s.replace(guard,"'revisao_potencias','revisao_afiliacao','revisao_escala_dual']")
 elif name=='finish_delta.py':
  old="'escala_dual':['dev_regular_dual_scaling/20260914_200033_241925/run.json']}[key]"
  new="'escala_dual':['dev_regular_dual_scaling/20260914_200033_241925/run.json'],\n  'cortes_inverso':['dev_inverse_cutoff/20260914_201442_615970/run.json']}[key]"
 else:
  old="'escala_dual':'AUDITORIA_ESCALA_DUAL_REGULAR_A1B.json'}"
  new="'escala_dual':'AUDITORIA_ESCALA_DUAL_REGULAR_A1B.json','cortes_inverso':'AUDITORIA_CORTES_INVERSO_A1B.json'}"
 assert s.count(old)==1
 s=s.replace(old,new);fresh(OUT/name,s.encode('utf8'))
 rows.append(dict(parent=pin(src),snapshot=pin(OUT/'helper_origins'/name),local=pin(OUT/name)))
fresh(OUT/'helper_provenance.json',(json.dumps(dict(scope='Only new inverse-cutoff configuration; previous sealed delta and helper bytes preserved',rows=rows),indent=2)+'\n').encode())
