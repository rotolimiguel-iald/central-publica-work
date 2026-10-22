from pathlib import Path
import hashlib,json,os
OUT=Path(__file__).resolve().parent;R=OUT.parent;BASE=R/'revisao_fechamento_gns'
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
  old="'fechamento_gns':('revisao_fechamento_gns',['V351ScalarGNSClosedness'],3,['REAPROVEITAMENTO_A1B_FECHAMENTO_GNS'])}"
  new="'fechamento_gns':('revisao_fechamento_gns',['V351ScalarGNSClosedness'],3,['REAPROVEITAMENTO_A1B_FECHAMENTO_GNS']),\n 'limites_direita':('revisao_limites_direita',['V351ScalarRightActionLimits'],2,['REAPROVEITAMENTO_A1B_LIMITES_ACAO_DIREITA'])}"
  guard="'revisao_escala_dual','revisao_cortes_inverso']"
  assert s.count(guard)==2
  s=s.replace(guard,"'revisao_escala_dual','revisao_cortes_inverso','revisao_fechamento_gns']")
 elif name=='finish_delta.py':
  old="'fechamento_gns':['dev_gns_closedness/20260914_203030_719820/run.json']}[key]"
  new="'fechamento_gns':['dev_gns_closedness/20260914_203030_719820/run.json'],\n  'limites_direita':['dev_right_action_limits/20260914_203706_719663/run.json']}[key]"
 else:
  old="'fechamento_gns':'AUDITORIA_FECHAMENTO_GNS_A1B.json'}"
  new="'fechamento_gns':'AUDITORIA_FECHAMENTO_GNS_A1B.json','limites_direita':'AUDITORIA_LIMITES_ACAO_DIREITA_A1B.json'}"
 assert s.count(old)==1
 s=s.replace(old,new);fresh(OUT/name,s.encode('utf8'))
 rows.append(dict(parent=pin(src),snapshot=pin(OUT/'helper_origins'/name),local=pin(OUT/name)))
fresh(OUT/'helper_provenance.json',(json.dumps(dict(scope='Only right-action limits delta; sealed helpers unchanged',rows=rows),indent=2)+'\n').encode())
