from pathlib import Path
import hashlib,json,os
OUT=Path(__file__).resolve().parent;R=OUT.parent;BASE=R/'revisao_limites_direita'
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
  old="'limites_direita':('revisao_limites_direita',['V351ScalarRightActionLimits'],2,['REAPROVEITAMENTO_A1B_LIMITES_ACAO_DIREITA'])}"
  new="'limites_direita':('revisao_limites_direita',['V351ScalarRightActionLimits'],2,['REAPROVEITAMENTO_A1B_LIMITES_ACAO_DIREITA']),\n 'algebra_direita':('revisao_algebra_direita',['V351ScalarRightActionAlgebra'],12,['REAPROVEITAMENTO_A1B_ALGEBRA_ACAO_DIREITA'])}"
  guard="'revisao_cortes_inverso','revisao_fechamento_gns']"
  assert s.count(guard)==2
  s=s.replace(guard,"'revisao_cortes_inverso','revisao_fechamento_gns','revisao_limites_direita']")
 elif name=='finish_delta.py':
  old="'limites_direita':['dev_right_action_limits/20260914_203706_719663/run.json']}[key]"
  new="'limites_direita':['dev_right_action_limits/20260914_203706_719663/run.json'],\n  'algebra_direita':['dev_right_action_algebra/20260914_210039_263478/run.json']}[key]"
 else:
  old="'limites_direita':'AUDITORIA_LIMITES_ACAO_DIREITA_A1B.json'}"
  new="'limites_direita':'AUDITORIA_LIMITES_ACAO_DIREITA_A1B.json','algebra_direita':'AUDITORIA_ALGEBRA_ACAO_DIREITA_A1B.json'}"
 assert s.count(old)==1
 s=s.replace(old,new);fresh(OUT/name,s.encode('utf8'))
 rows.append(dict(parent=pin(src),snapshot=pin(OUT/'helper_origins'/name),local=pin(OUT/name)))
fresh(OUT/'helper_provenance.json',(json.dumps(dict(scope='Only right-action algebra delta; sealed helpers unchanged',rows=rows),indent=2)+'\n').encode())
