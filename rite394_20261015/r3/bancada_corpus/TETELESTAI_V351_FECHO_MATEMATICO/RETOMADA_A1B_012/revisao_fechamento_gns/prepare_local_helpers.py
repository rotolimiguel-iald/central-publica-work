from pathlib import Path
import hashlib,json,os
R=Path(__file__).resolve().parent.parent;OUT=Path(__file__).resolve().parent;BASE=R/'revisao_cortes_inverso'
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
  old="'cortes_inverso':('revisao_cortes_inverso',['V351InverseGeneratorCutoff'],8,['REAPROVEITAMENTO_A1B_CORTES_INVERSO','ADENDO_FICHA_INVERSO_BILATERAL'])}"
  new="'cortes_inverso':('revisao_cortes_inverso',['V351InverseGeneratorCutoff'],8,['REAPROVEITAMENTO_A1B_CORTES_INVERSO','ADENDO_FICHA_INVERSO_BILATERAL']),\n 'fechamento_gns':('revisao_fechamento_gns',['V351ScalarGNSClosedness'],3,['REAPROVEITAMENTO_A1B_FECHAMENTO_GNS'])}"
  guard="'revisao_afiliacao','revisao_escala_dual']"
  assert s.count(guard)==2
  s=s.replace(guard,"'revisao_afiliacao','revisao_escala_dual','revisao_cortes_inverso']")
 elif name=='finish_delta.py':
  old="'cortes_inverso':['dev_inverse_cutoff/20260914_201442_615970/run.json']}[key]"
  new="'cortes_inverso':['dev_inverse_cutoff/20260914_201442_615970/run.json'],\n  'fechamento_gns':['dev_gns_closedness/20260914_203030_719820/run.json']}[key]"
 else:
  old="'cortes_inverso':'AUDITORIA_CORTES_INVERSO_A1B.json'}"
  new="'cortes_inverso':'AUDITORIA_CORTES_INVERSO_A1B.json','fechamento_gns':'AUDITORIA_FECHAMENTO_GNS_A1B.json'}"
 assert s.count(old)==1
 s=s.replace(old,new);fresh(OUT/name,s.encode('utf8'))
 rows.append(dict(parent=pin(src),snapshot=pin(OUT/'helper_origins'/name),local=pin(OUT/name)))
fresh(OUT/'helper_provenance.json',(json.dumps(dict(scope='Only closed-GNS delta; sealed helpers unchanged, absent old suppliers copied as source only',rows=rows),indent=2)+'\n').encode())
