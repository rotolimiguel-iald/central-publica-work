# -*- coding: utf-8 -*-
"""Revisor terceiro: compara por AST e por fatia de fonte os intocados entre a base v404 e o candidato v405. So le; nada executa."""
import ast, hashlib, json, sys, time
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v405/"
BASE = "C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N\u00f3s/um.py"
CAND = R + "um_v405_candidato.py"
NOMES = ["evaluate_quantum_gravity_closure","prove_qg_closure_gate","prove_neutrino_mass_gravitational","ramo_b_preregistration_v386","ledger_errata_v386","prove_ga_mass_audit","prove_joint_coincidence_result_v3","GA_WINDOW_STATUS"]
def carrega(p):
    b = open(p,"rb").read(); s = b.decode("utf-8"); t = time.time(); tr = ast.parse(s); return b, s, tr, time.time()-t
def acha(tr, nome):
    out=[]
    for n in ast.walk(tr):
        if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name==nome: out.append(n)
        elif isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==nome for t in n.targets): out.append(n)
        elif isinstance(n,ast.AnnAssign) and isinstance(n.target,ast.Name) and n.target.id==nome: out.append(n)
    return out
bb,bs,bt,tb=carrega(BASE); cb,cs,ct,tc=carrega(CAND)
print("base sha16",hashlib.sha256(bb).hexdigest()[:16],len(bb),"parse",round(tb,1)); print("cand sha16",hashlib.sha256(cb).hexdigest()[:16],len(cb),"parse",round(tc,1))
bl=bs.split("\n"); cl=cs.split("\n")
res={}
for n in NOMES:
    a=acha(bt,n); b=acha(ct,n)
    r={"n_base":len(a),"n_cand":len(b)}
    if len(a)==len(b):
        r["ast_igual"]=all(ast.dump(x)==ast.dump(y) for x,y in zip(a,b))
        r["fonte_igual"]=all("\n".join(bl[x.lineno-1:x.end_lineno])=="\n".join(cl[y.lineno-1:y.end_lineno]) for x,y in zip(a,b))
        r["linhas_cand"]=[(y.lineno,y.end_lineno) for y in b]
    res[n]=r; print(n,r)
# nivel superior: o que mudou
def top(tr,src):
    d={}
    for n in tr.body:
        nm=None
        if isinstance(n,(ast.FunctionDef,ast.ClassDef,ast.AsyncFunctionDef)): nm=n.name
        elif isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name): nm=n.targets[0].id
        if nm: d.setdefault(nm,[]).append(hashlib.sha256(ast.dump(n).encode()).hexdigest()[:16])
    return d
tb_=top(bt,bs); tc_=top(ct,cs)
mud=[k for k in tb_ if k in tc_ and tb_[k]!=tc_[k]]; rem=[k for k in tb_ if k not in tc_]; nov=[k for k in tc_ if k not in tb_]
print("mudados",len(mud),mud); print("removidos",rem); print("novos",len(nov),nov)
json.dump({"res":res,"mudados":mud,"removidos":rem,"novos":nov},open(R+"revisao_terceiro/e_intocados_out.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
