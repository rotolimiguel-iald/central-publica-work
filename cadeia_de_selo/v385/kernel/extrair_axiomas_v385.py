# -*- coding: utf-8 -*-
"""Extrai do build_full.log do SANDBOX (construir_kernel_v385.sh) o relatorio de axiomas, com a MESMA regex do verify do um.py (molde:
extrair_axiomas_v376.py), e grava: sandbox_axiom_report_v385.json (nome -> axiomas), AUDIT_NOMES_v385.json (os nomes da v385, NA ORDEM do bloco v385 do
TGL/Audit.lean, por modulo) e sandbox_raiz_v385.json (n, sorry, fora do trio, as bandeiras da v385 = as do v385_runtime.py, posicao a posicao).
Recusa se o build nao terminou verde, se houver sorry, algo fora do trio, ou se uma bandeira nao casar com o nome da declaracao na mesma posicao."""
import json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
PK = os.path.dirname(HERE)
K = os.path.join(os.path.dirname(PK), "v376", "kernel_src")
TRIO = {"propext", "Classical.choice", "Quot.sound"}
t = open(os.path.join(HERE, "build_full.log"), encoding="utf-8", errors="replace").read()
assert re.search(r"(?m)^rc=0$", t) and re.search(r"(?m)^rc_build=0$", t) and re.search(r"(?m)^rc_audit=0$", t), "o build/auditoria nao terminou verde"
axioms = {}
for m in re.finditer(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]", t, re.S):
    axioms[m.group(1)] = [a.strip() for a in m.group(2).replace("\n", " ").split(",") if a.strip()]
for m in re.finditer(r"'([\w.']+)' does not depend on any axioms", t):
    axioms.setdefault(m.group(1), [])
sorry = len(re.findall(r"declaration uses 'sorry'", t))
fora = {k: v for k, v in axioms.items() if not set(v) <= TRIO}
assert sorry == 0 and not fora, (sorry, list(fora)[:5])
# os nomes da v385, NA ORDEM do bloco v385 do Audit.lean (depois do comentario datado da v385)
au = open(os.path.join(K, "TGL", "Audit.lean"), encoding="utf-8").read()
k = au.index("-- 2026-10-05, v385")
nomes = re.findall(r"(?m)^#print axioms (\S+)$", au[k:])
NOMES = {"TheAxiomAndTheFalseWitness": [n for n in nomes if n.startswith("TGLExt.TheAxiomAndTheFalseWitness.")],
         "TheDarkSplit": [n for n in nomes if not n.startswith("TGLExt.TheAxiomAndTheFalseWitness.")]}
# as bandeiras do runtime, posicao a posicao (o nome curto da bandeira = o nome curto da declaracao)
RT = open(os.path.join(PK, "v385_runtime.py"), encoding="utf-8").read()
ns = {}
exec(compile("\n".join(l for l in RT.splitlines() if l.startswith(("_AXM_FLAGS_V385", "_DKS_FLAGS_V385", "]")) or l.startswith("    \"ext_")), "<flags>", "exec"), ns)
pares = list(zip(ns["_AXM_FLAGS_V385"], NOMES["TheAxiomAndTheFalseWitness"])) + list(zip(ns["_DKS_FLAGS_V385"], NOMES["TheDarkSplit"]))
assert len(ns["_AXM_FLAGS_V385"]) == len(NOMES["TheAxiomAndTheFalseWitness"]) and len(ns["_DKS_FLAGS_V385"]) == len(NOMES["TheDarkSplit"]), \
    (len(ns["_AXM_FLAGS_V385"]), len(NOMES["TheAxiomAndTheFalseWitness"]), len(ns["_DKS_FLAGS_V385"]), len(NOMES["TheDarkSplit"]))
for f, nm in pares:
    pfx = "ext_axm_" if f.startswith("ext_axm_") else "ext_dks_"
    assert f.replace(pfx, "").rsplit("_kernel_", 1)[0] == nm.split(".")[-1], (f, nm)
res = {"n_axiom_report": len(axioms), "sorry_warnings": sorry, "fora_do_trio": fora,
       "bandeiras": {f: (nm in axioms and set(axioms[nm]) <= TRIO) for f, nm in pares}}
res["bandeiras_ok"] = sum(res["bandeiras"].values())
assert res["bandeiras_ok"] == len(pares), [f for f, v in res["bandeiras"].items() if not v]
for nome, obj in (("sandbox_axiom_report_v385.json", axioms), ("AUDIT_NOMES_v385.json", NOMES), ("sandbox_raiz_v385.json", res)):
    p = os.path.join(HERE, nome)
    if os.path.exists(p):
        open(p + ".bak_antes_afer2", "wb").write(open(p, "rb").read())
    with open(p + ".tmp", "w", encoding="utf-8") as f_:
        json.dump(obj, f_, ensure_ascii=False, indent=1 if nome != "sandbox_axiom_report_v385.json" else None)
    os.replace(p + ".tmp", p)
print(json.dumps({"n_axiom_report": res["n_axiom_report"], "sorry": sorry, "fora_do_trio": len(fora), "bandeiras_ok": res["bandeiras_ok"],
                  "nomes": {k_: len(v_) for k_, v_ in NOMES.items()}}, ensure_ascii=False))
