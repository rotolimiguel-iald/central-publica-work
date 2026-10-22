from pathlib import Path
import datetime,hashlib,json,os
R=Path(__file__).resolve().parent;K=R/'k'
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
    assert not p.exists() and p.is_relative_to(R)
    t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
specs=[('.lake/packages/mathlib/Mathlib/Topology/MetricSpace/UniformConvergence.lean',94,5),('.lake/packages/mathlib/Mathlib/Topology/MetricSpace/Lipschitz.lean',45,7),('.lake/packages/mathlib/Mathlib/Analysis/SpecificLimits/Basic.lean',69,7)]
providers=[]
for path,line,count in specs:
    p=K/path;rows=p.read_text(encoding='utf8').splitlines();providers.append(dict(source=pin(p),line=line,excerpt='\n'.join(rows[line-1:line-1+count])))
d=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),status='OPEN__ROUTE_BEFORE_DOMAIN_CUT_CODE',consultation=pin(R/'revisao_consulta_semifinitude_limite/CONSULTA_SEMIFINITUDE_LIMITE.md'),providers=providers,
    decision='Use q_delta directly. The first module supplies bounded contractions, membership/right action, inverse-product bound and strong convergence. The next consumer applies the existing right-perturbed weight comparison and WOT closure. This splits algebraic/operator estimates from the scalar finiteness proof, not duplicate definitions. No new root.')
put(R/'ADENDO_FICHA_CORTE_DOMINIO_ROTA.json',json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'))
s='[OPEN — rota e APIs antes do código]\n\n'+d['timestamp']+'\n\n'+d['decision']+'\n\nConsulta lida integralmente: '+d['consultation']['path']+'\n\n'
for q in providers:s+=q['source']['path']+':'+str(q['line'])+' — '+q['source']['sha256']+'\n\n```lean\n'+q['excerpt']+'\n```\n\n'
put(R/'ADENDO_FICHA_CORTE_DOMINIO_ROTA.md',s.encode('utf8'))
