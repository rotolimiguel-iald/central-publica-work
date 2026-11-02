# -*- coding: utf-8 -*-
import ast, difflib, hashlib, sys, re
sys.stdout.reconfigure(encoding="utf-8")
R="C:/IALD/Central de Patentes/work/cadeia_de_selo/v405/"
b=open("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N\u00f3s/um.py",encoding="utf-8").read(); c=open(R+"um_v405_candidato.py",encoding="utf-8").read()
tb=ast.parse(b); tc=ast.parse(c)
def fn(t,s,n):
    for x in t.body:
        if isinstance(x,ast.FunctionDef) and x.name==n:
            return s.split("\n")[x.lineno-1:x.end_lineno]
for n in ("main","prove_external_ladder"):
    A=fn(tb,b,n); B=fn(tc,c,n)
    print("==",n,len(A),len(B))
    for l in difflib.unified_diff(A,B,lineterm="",n=0):
        if l.startswith(("---","+++","@@")): continue
        print(l[:210])
# embutidos
emb=None
for x in tc.body:
    if isinstance(x,ast.Assign) and getattr(x.targets[0],"id","")=="_EMBEDDED_KERNEL_FILES":
        emb=x
print(type(emb.value).__name__)
import json
vals={}
if isinstance(emb.value,ast.Dict):
    for k,v in zip(emb.value.keys,emb.value.values):
        kk=ast.literal_eval(k)
        if any(s in kk for s in ("PonteDaMassa","MassaTensaoPura","Identidade.lean","ObservadorTerminal","LeiDoDiminuto","TonicaDoHamiltoniano","DiscoDeEuler","PontoZeroDoPsion")):
            vals[kk]=ast.literal_eval(v)
for k,v in vals.items():
    f="C:/t/k405c/final/"+k
    print(k,hashlib.sha256(v.encode()).hexdigest()[:16],hashlib.sha256(open(f,"rb").read()).hexdigest()[:16],hashlib.sha256(open(R+"pedra/"+k.split("/")[-1],"rb").read()).hexdigest()[:16])
# atribuicoes em chaves do gate no bloco novo
blk=c[c.index("def _v405_guarda_frases"):]
blk=blk[:blk.index("_V405_NOMES_REGISTROS")+3000]
print([m for m in re.findall(r"core_?\[[\"']([a-z_0-9]+)[\"']\]\s*=",blk)][:30])
print(re.findall(r"qg_closure[^\n]{0,80}",blk)[:6])
