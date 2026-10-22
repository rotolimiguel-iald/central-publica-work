# -*- coding: utf-8 -*-
"""Extrai do build_full.log do SANDBOX (construir_kernel_v386.sh) o relatorio de axiomas, com a MESMA regex do verify do um.py (molde:
extrair_axiomas_v385.py), e grava: sandbox_axiom_report_v386.json (nome -> axiomas), AUDIT_NOMES_v386.json (os nomes da v386, NA ORDEM do bloco v386 do
TGL/Audit.lean, por modulo: a pedra e a fiacao angular) e sandbox_raiz_v386.json (n, sorry, fora do trio, as bandeiras da v386 = as de v386_flags.py,
posicao a posicao, e as contagens: total auditado, novas da v385 -> v386, escada prevista = escada da v385 + bandeiras novas).
Recusa se o build nao terminou verde, se houver sorry, algo fora do trio, se uma declaracao nova nao estiver no relatorio, ou se uma bandeira nao casar
com o nome da declaracao na mesma posicao."""
import json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
PK = os.path.dirname(HERE)
SP = os.path.dirname(PK)
K = os.path.join(SP, "v376", "kernel_src")
TRIO = {"propext", "Classical.choice", "Quot.sound"}
t = open(os.path.join(HERE, "build_full.log"), encoding="utf-8", errors="replace").read()
assert re.search(r"(?m)^rc=0$", t) and re.search(r"(?m)^rc_build=0$", t) and re.search(r"(?m)^rc_audit=0$", t), "o build/auditoria nao terminou verde"
assert not re.search(r"(?m)^error:|: error:", t), "ha linhas de erro no log"
axioms = {}
for m in re.finditer(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]", t, re.S):
    axioms[m.group(1)] = [a.strip() for a in m.group(2).replace("\n", " ").split(",") if a.strip()]
for m in re.finditer(r"'([\w.']+)' does not depend on any axioms", t):
    axioms.setdefault(m.group(1), [])
sorry = len(re.findall(r"declaration uses 'sorry'", t))
fora = {k: v for k, v in axioms.items() if not set(v) <= TRIO}
assert sorry == 0 and not fora, (sorry, list(fora)[:5])
# os nomes da v386, NA ORDEM do bloco v386 do Audit.lean (depois do comentario datado da v386)
au = open(os.path.join(K, "TGL", "Audit.lean"), encoding="utf-8").read()
k = au.index("-- 2026-10-05, v386")
nomes = re.findall(r"(?m)^#print axioms (\S+)$", au[k:])
NOMES = {"TheVerbSelectsTheAction": [n for n in nomes if n.startswith("TGLExt.TheVerbSelectsTheAction.")],
         "AngularWiring": [n for n in nomes if not n.startswith("TGLExt.TheVerbSelectsTheAction.")]}
faltam = [n for n in nomes if n not in axioms]
assert not faltam, ("declaracoes do bloco v386 sem linha no relatorio", faltam[:10])
# as bandeiras (v386_flags.py), posicao a posicao (o nome curto da bandeira = o nome curto da declaracao)
RT = open(os.path.join(HERE, "v386_flags.py"), encoding="utf-8").read()
ns = {}
exec(compile("\n".join(l for l in RT.splitlines() if l.startswith(("_VRB_FLAGS_V386", "_ANG_FLAGS_V386", "]")) or l.startswith("    \"ext_")), "<flags>", "exec"), ns)
pares = list(zip(ns["_VRB_FLAGS_V386"], NOMES["TheVerbSelectsTheAction"])) + list(zip(ns["_ANG_FLAGS_V386"], NOMES["AngularWiring"]))
assert len(ns["_VRB_FLAGS_V386"]) == len(NOMES["TheVerbSelectsTheAction"]) and len(ns["_ANG_FLAGS_V386"]) == len(NOMES["AngularWiring"]), \
    (len(ns["_VRB_FLAGS_V386"]), len(NOMES["TheVerbSelectsTheAction"]), len(ns["_ANG_FLAGS_V386"]), len(NOMES["AngularWiring"]))
for f, nm in pares:
    pfx = "ext_vrb_" if f.startswith("ext_vrb_") else "ext_ang_"
    assert f.replace(pfx, "").rsplit("_kernel_", 1)[0] == nm.split(".")[-1], (f, nm)
# as contagens: o total auditado nesta rodada, o da v385 (lido do relatorio da v385), a escada prevista (a da v385 lida do core selado + as novas)
rep385 = json.load(open(os.path.join(PK + "", "..", "v385", "kernel", "sandbox_axiom_report_v385.json"), encoding="utf-8"))
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
_C385 = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]["external_ladder"]
_E385 = int(_C385["n_theorems_expected"]); assert int(_C385["n_theorems_clean"]) == _E385
res = {"n_axiom_report": len(axioms), "n_axiom_report_v385": len(rep385), "novas_auditadas_v385_para_v386": len(axioms) - len(rep385),
       "sorry_warnings": sorry, "fora_do_trio": fora,
       "bandeiras": {f: (nm in axioms and set(axioms[nm]) <= TRIO) for f, nm in pares},
       "n_pedra": len(NOMES["TheVerbSelectsTheAction"]), "n_fiacao": len(NOMES["AngularWiring"]),
       "escada_v385_lida_do_core": _E385, "escada_v386_prevista": _E385 + len(pares),
       "regra_da_escada": "external_ladder conta as bandeiras ext_* listadas em prove_external_ladger(ext_flags) que estao True no kernel_formalization; "
                          "v385: 6027 = 5998 + 29; v386 = 6027 + (bandeiras ext_vrb_ + ext_ang_)".replace("ledger", "ladder"),
       "axiomas_novas": {nm: axioms.get(nm) for _, nm in pares}}
res["bandeiras_ok"] = sum(res["bandeiras"].values())
assert res["bandeiras_ok"] == len(pares), [f for f, v in res["bandeiras"].items() if not v]
for nome, obj in (("sandbox_axiom_report_v386.json", axioms), ("AUDIT_NOMES_v386.json", NOMES), ("sandbox_raiz_v386.json", res)):
    p = os.path.join(HERE, nome)
    if os.path.exists(p):
        open(p + ".bak_antes_afer", "wb").write(open(p, "rb").read())
    with open(p + ".tmp", "w", encoding="utf-8") as f_:
        json.dump(obj, f_, ensure_ascii=False, indent=1 if nome != "sandbox_axiom_report_v386.json" else None)
    os.replace(p + ".tmp", p)
print(json.dumps({"n_axiom_report": res["n_axiom_report"], "n_v385": res["n_axiom_report_v385"], "novas": res["novas_auditadas_v385_para_v386"],
                  "sorry": sorry, "fora_do_trio": len(fora), "bandeiras_ok": res["bandeiras_ok"], "escada_prevista": res["escada_v386_prevista"],
                  "nomes": {k_: len(v_) for k_, v_ in NOMES.items()}}, ensure_ascii=False))
